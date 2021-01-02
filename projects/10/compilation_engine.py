from jack_tokenizer import TokenType

subroutine_dec_markers = ["constructor", "function", "method"]
types = ["int", "char", "boolean"]
statement_markers = ["let", "if", "while", "do", "return"]
ops = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
keyword_constants = ["true", "false", "null", "this"]
unary_ops = ["-", "~"]


class CompilationEngine(object):
    def __init__(self, tokenizer, output_file_name):
        self.tokenizer = tokenizer
        self.output_file_name = output_file_name
        self.tags = []

    def compile(self):
        self.compile_class()
        self._write_tags()

    def compile_class(self):
        self._store_opening_tag("class")

        # class
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat('class')

        # className
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat(self.tokenizer.get_current_token())

        # {
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat("{")

        # classVarDec* (0 or many)
        while self.tokenizer.get_current_token() not in subroutine_dec_markers:
            self.compile_class_var_dec()

        # subroutineDec* (0 or many)
        while self.tokenizer.get_current_token() != "}":
            self.compile_subroutine_dec()

        # }
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat("}")

        self._store_closing_tag("class")

    def compile_class_var_dec(self):
        self._store_opening_tag("classVarDec")

        # static | field
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat(self.tokenizer.get_current_token())

        # type
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat(self.tokenizer.get_current_token())

        # one or more variables
        while self.tokenizer.get_current_token() != ";":
            self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
            self._eat(self.tokenizer.get_current_token())

        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat(";")

        self._store_closing_tag("classVarDec")

    def compile_subroutine_dec(self):
        self._store_opening_tag("subroutineDec")

        # constructor | function | method
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat(self.tokenizer.get_current_token())

        # void | type
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat(self.tokenizer.get_current_token())

        # subRoutineName
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat(self.tokenizer.get_current_token())

        # (
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat(self.tokenizer.get_current_token())

        self.compile_parameter_list()

        # )
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat(self.tokenizer.get_current_token())

        self.compile_subroutine_body()

        self._store_closing_tag("subroutineDec")

    def compile_parameter_list(self):
        self._store_opening_tag("parameterList")

        while self.tokenizer.get_current_token() != ")":
            self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
            self._eat(self.tokenizer.get_current_token())

        self._store_closing_tag("parameterList")

    def compile_subroutine_body(self):
        self._store_opening_tag("subroutineBody")

        # {
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat(self.tokenizer.get_current_token())

        # Until we hit a statement we need to deal with varDec*
        while self.tokenizer.get_current_token() not in statement_markers:
            self.compile_var_dec()

        # statements
        self.compile_statements()

        # }
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat(self.tokenizer.get_current_token())

        self._store_closing_tag("subroutineBody")

    def compile_var_dec(self):
        self._store_opening_tag("varDec")

        # var
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat("var")

        # type
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat(self.tokenizer.get_current_token())

        # one or more variables
        while self.tokenizer.get_current_token() != ";":
            self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
            self._eat(self.tokenizer.get_current_token())

        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat(";")

        self._store_closing_tag("varDec")

    def compile_statements(self):
        self._store_opening_tag("statements")

        while self.tokenizer.get_current_token() != "}":
            current_token = self.tokenizer.get_current_token()
            if current_token == "let":
                self.compile_let_statement()
            elif current_token == "if":
                self.compile_if_statement()
            elif current_token == "while":
                self.compile_while_statement()
            elif current_token == "do":
                self.compile_do_statement()
            elif current_token == "return":
                self.compile_return_statement()
            else:
                import pdb;
                pdb.set_trace()
                raise Exception("compile_statements(): {} not a valid statement. Valid statements are {}".format(current_token, statement_markers))

        self._store_closing_tag("statements")

    def compile_let_statement(self):
        self._store_opening_tag("letStatement")

        # let
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat("let")

        # varName
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat(self.tokenizer.get_current_token())

        # If the current token is [ it implies this is an array access.
        # We thus need to add expression support here
        if self.tokenizer.get_current_token() == "[":
            self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
            self._eat("[")

            self.compile_expression()

            self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
            self._eat("]")

        # =
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat("=")

        # expression
        self.compile_expression()

        # ;
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat(";")

        self._store_closing_tag("letStatement")

    def compile_if_statement(self):
        self._store_opening_tag("ifStatement")

        # if
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat("if")

        # (
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat("(")

        self.compile_expression()

        # )
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat(")")

        # {
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat("{")

        # statements
        self.compile_statements()

        # }
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat(self.tokenizer.get_current_token())

        if self.tokenizer.get_current_token() == "else":
            # else
            self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
            self._eat(self.tokenizer.get_current_token())

            # {
            self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
            self._eat("{")

            # statements
            self.compile_statements()

            # }
            self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
            self._eat(self.tokenizer.get_current_token())

        self._store_closing_tag("ifStatement")

    def compile_while_statement(self):
        self._store_opening_tag("whileStatement")

        # while
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat("while")

        # (
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat("(")

        self.compile_expression()

        # )
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat(")")

        # {
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat("{")

        self.compile_statements()

        # }
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat("}")

        self._store_closing_tag("whileStatement")

    def compile_do_statement(self):
        self._store_opening_tag("doStatement")

        # do
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat("do")

        # subroutineName | className | varName
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat(self.tokenizer.get_current_token())

        # Method from the same class
        if self.tokenizer.get_current_token() == "(":
            self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
            self._eat("(")

            self.compile_expression_list()

            self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
            self._eat(")")
        # Method from another class
        else:
            # .
            self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
            self._eat(".")

            # subroutine name
            self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
            self._eat(self.tokenizer.get_current_token())

            # (
            self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
            self._eat(self.tokenizer.get_current_token())

            self.compile_expression_list()

            # )
            self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
            self._eat(")")

        # ;
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat(";")

        self._store_closing_tag("doStatement")

    def compile_return_statement(self):
        self._store_opening_tag("returnStatement")

        # return
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat("return")

        if self.tokenizer.get_current_token() != ";":
            self.compile_expression()

        # ;
        self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
        self._eat(";")

        self._store_closing_tag("returnStatement")

    def compile_expression_list(self):
        self._store_opening_tag("expressionList")

        while self.tokenizer.get_current_token() != ")":
            self.compile_expression()

            if self.tokenizer.get_current_token() == ",":
                self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
                self._eat(",")

        self._store_closing_tag("expressionList")

    def compile_expression(self):
        self._store_opening_tag("expression")
        self.compile_term()

        while self.tokenizer.get_current_token() in ops:
            # op
            self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_token_value())
            self._eat(self.tokenizer.get_current_token())

            self.compile_term()

        self._store_closing_tag("expression")

    def compile_term(self):
        self._store_opening_tag("term")

        current_token_type = self.tokenizer.get_token_type()
        current_token = self.tokenizer.get_current_token()

        if current_token_type in [TokenType.INT_CONST, TokenType.STRING_CONST]:
            self._store_complete_tag(current_token_type.value, self.tokenizer.get_token_value())
            self._eat(current_token)
        elif current_token in keyword_constants:
            self._store_complete_tag(TokenType.KEYWORD.value, current_token)
            self._eat(current_token)
        elif current_token == "(":
            self._store_complete_tag(self.tokenizer.get_token_type().value, current_token)
            self._eat("(")

            self.compile_expression()

            self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
            self._eat(")")
        elif current_token in unary_ops:
            self._store_complete_tag(self.tokenizer.get_token_type().value, current_token)
            self._eat(current_token)

            self.compile_term()
        else:
            # Could be one of varName, varName[expression] or subRoutineCall
            self._store_complete_tag(self.tokenizer.get_token_type().value, current_token)
            self._eat(current_token)

            # varName[expression]
            if self.tokenizer.get_current_token() == "[":
                self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
                self._eat("[")

                self.compile_expression()

                self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
                self._eat("]")

            # subroutineCall
            if self.tokenizer.get_current_token() in ["(", "."]:
                # Method from the same class
                if self.tokenizer.get_current_token() == "(":
                    self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
                    self._eat("(")

                    self.compile_expression_list()

                    self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
                    self._eat(")")
                # Method from another class
                else:
                    # .
                    self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
                    self._eat(".")

                    # subroutine name
                    self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
                    self._eat(self.tokenizer.get_current_token())

                    # (
                    self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
                    self._eat(self.tokenizer.get_current_token())

                    self.compile_expression_list()

                    # )
                    self._store_complete_tag(self.tokenizer.get_token_type().value, self.tokenizer.get_current_token())
                    self._eat(")")

        self._store_closing_tag("term")

    def _eat(self, val):
        if self.tokenizer.get_current_token() != val:
            self._write_tags()
            raise Exception("_eat(): {} != {}".format(self.tokenizer.get_current_token(), val))
        self.tokenizer.advance()

    def _store_complete_tag(self, name, value):
        self.tags.append("<{}> {} </{}>\n".format(name, value, name))

    def _store_opening_tag(self, name):
        self.tags.append("<{}>\n".format(name))

    def _store_closing_tag(self, name):
        self.tags.append("</{}>\n".format(name))

    def _write_tags(self):
        with open(self.output_file_name, "w") as f:
            for tag in self.tags:
                f.write(tag)
