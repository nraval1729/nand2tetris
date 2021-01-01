import sys
from os import listdir
from os.path import join

from jack_tokenizer import JackTokenizer


def main():
    if len(sys.argv) != 2:
        print("Expected 1 argument (either the .jack file or a directory containing .jack files). Exiting!")
        return

    is_file_arg = sys.argv[1].endswith(".jack")

    if is_file_arg:
        jack_files = [sys.argv[1]]
    else:
        jack_files = [join(sys.argv[1], f) for f in listdir(sys.argv[1]) if f.endswith(".jack")]
    for jack_file in jack_files:
        tokenizer = JackTokenizer(jack_file)
        # test_file_name = jack_file.split("/")[-1].split(".")[0] + "TNisarg" + ".xml"
        test_file_name = jack_file.split(".jack")[0] + "TNisarg" + ".xml"
        with open(test_file_name, "w") as tf:
            tf.write(construct_opening_tag())
            while tokenizer.has_more_tokens():
                token_type, token_value = tokenizer.get_token_type(), tokenizer.get_token_value()
                tf.write(construct_xml_tag(token_type.value, token_value))
                tokenizer.advance()

            tf.write(construct_closing_tag())


def construct_xml_tag(tag_name, content):
    return "<{}> {} </{}>\n".format(tag_name, content, tag_name)


def construct_opening_tag(name="tokens"):
    return "<{}>\n".format(name)


def construct_closing_tag(name="tokens"):
    return "</{}>\n".format(name)


if __name__ == "__main__":
    main()
