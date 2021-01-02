import sys
from os import listdir
from os.path import join

from compilation_engine import CompilationEngine
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
        ce = CompilationEngine(JackTokenizer(jack_file), jack_file.split(".jack")[0] + "Nisarg.xml")
        ce.compile()


if __name__ == "__main__":
    main()
