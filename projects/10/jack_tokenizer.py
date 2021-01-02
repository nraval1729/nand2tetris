from enum import Enum


class TokenType(Enum):
    KEYWORD = "keyword"
    SYMBOL = "symbol"
    INT_CONST = "integerConstant"
    STRING_CONST = "stringConstant"
    IDENTIFIER = "identifier"


keywords = ["class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void", "true", "false", "null",
            "this", "let", "do", "if", "else", "while", "return"]
symbols = ["{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"]


class JackTokenizer(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.current_token_idx = 0
        self.tokens = _tokenize(self.file_name)

    def has_more_tokens(self):
        return self.current_token_idx < len(self.tokens)

    def advance(self):
        self.current_token_idx += 1

    def get_token_type(self):
        curr_token = self.get_current_token()

        if curr_token in keywords:
            return TokenType.KEYWORD
        elif curr_token in symbols:
            return TokenType.SYMBOL
        elif curr_token.isdigit() and int(curr_token) <= 32767:
            return TokenType.INT_CONST
        elif curr_token.startswith("\""):
            return TokenType.STRING_CONST
        else:
            return TokenType.IDENTIFIER

    def get_token_value(self):
        current_token = self._escape_current_token_if_necessary(self.get_current_token())
        if self.get_token_type() == TokenType.INT_CONST:
            return int(current_token)
        elif self.get_token_type() == TokenType.STRING_CONST:
            return "".join(current_token[1:-1])
        else:
            return current_token

    def get_current_token(self):
        return self.tokens[self.current_token_idx]

    def _escape_current_token_if_necessary(self, token):
        if token == ">":
            return "&gt;"
        elif token == "<":
            return "&lt;"
        elif token == "&":
            return "&amp;"
        else:
            return token


def _tokenize(file_name):
    tokens = []

    for line in _filter_inline_comments(_filter_block_comments(_get_content(file_name))):
        is_quote_seen = False
        curr_token = ""
        for c in line:
            if c == "\"":
                if is_quote_seen:
                    tokens.append(curr_token + "\"")
                    curr_token = ""
                    is_quote_seen = False
                else:
                    if curr_token != "":
                        tokens.append(curr_token)
                    is_quote_seen = True
                    curr_token = c
            elif is_quote_seen:
                curr_token += c
            elif curr_token in symbols:
                tokens.append(curr_token)
                curr_token = c if c != " " else ""
            elif c == " ":
                if curr_token != "":
                    tokens.append(curr_token)
                curr_token = ""
            elif c in symbols:
                if curr_token != "":
                    tokens.append(curr_token)
                curr_token = c
            else:
                curr_token += c

        if curr_token and curr_token != " "   :
            tokens.append(curr_token)
    return tokens


def _print_content(content):
    for line in content:
        print(line)


def _get_content(file_name):
    with open(file_name, 'r') as f:
        content = [l.strip() for l in f if l != "\n"]
    return content


def _filter_block_comments(content):
    return [line for line in content if not (line.startswith("//") or line.startswith("/**") or line.startswith("*"))]


def _filter_inline_comments(content):
    filtered_content = []

    for line in content:
        if "//" in line:
            filtered_line = "".join(line[:line.index("//")]).strip()
            filtered_content.append(filtered_line)
        else:
            filtered_content.append(line)

    return filtered_content
