import functools

from SymbolTable import SymbolTable
import re

class Scanner:
    def __init__(self, input_filename):
        self.__separators = [' ', ';', ':', '{', '}', '[', ']', '(', ')', ',']
        self.__separators_for_regex_pattern = [' ', ';', ':', '\{', '\}', '\[', '\]', '\(', '\)']
        self.__operators = ['+', '-', '*', '/', '%', '=', '==', '<', '>', '<=', '>=', '+=']
        self.__keywords = ["defvar", "deflist", "and", "or", "not", "if", "else", "loop", "input", "print", "int", "str", "char", "bool", "double"]
        self.__input_filename = input_filename
        self.__file = None
        self.__symbol_table = SymbolTable()
        self.__program_internal_form = []
        self.__space_tokenized_code = None

    def is_separator(self, token):
        return token in self.__separators

    def is_operator(self, token):
        return token in self.__operators

    def is_keyword(self, token):
        return token in self.__keywords

    def is_identifier(self, token):
        pattern_match = re.findall("[a-zA-Z_][a-zA-Z0-9_]*", token)
        return len(pattern_match) > 0 and pattern_match[0] == token

    def is_constant(self, token):
        return (token[0] == "\"" and token[-1] == "\"") or (re.findall("[0-9]*", token)[0] == token)

    def extract_token_with_separators(self, token):
        final_token_list = []
        found_separators = False

        for index in range(0, len(token)):
            if token[index] in self.__separators:
                final_token_list.append(token[:index])
                final_token_list.append(token[index])
                token = token[index+1:]
                found_separators = True

        return final_token_list if found_separators else token

    def read_file(self):
        file_handler = open(self.__input_filename, "r")
        self.__file = file_handler.readlines()
        self.__file = list(map(lambda line: re.sub("\t", "", line), self.__file))
        return self.__file

    def split_in_tokens(self):
        separators_as_string = ""
        for separator in self.__separators_for_regex_pattern:
            separators_as_string += separator
        tokenization_pattern = '.*?[' + separators_as_string + ']'
        self.__space_tokenized_code = list(map(lambda line: re.findall(tokenization_pattern, line), self.__file))
        print("Space tokenized code: {}".format(self.__space_tokenized_code))
        self.__space_cleared_code = list(map(lambda row: list(map(lambda token: token.replace(' ', ''), row)), self.__space_tokenized_code))
        self.__space_cleared_code = [item for sublist in self.__space_cleared_code for item in sublist]
        print("Space cleared code: {}".format(self.__space_cleared_code))
        self.__separator_tokenized_code = list(map(lambda token: self.extract_token_with_separators(token), self.__space_cleared_code))

        final_result = []
        line_number = 0

        for item in self.__separator_tokenized_code:
            if isinstance(item, str):
                if len(item) > 1 and item[0] == '-':
                    final_result.append('-')
                    final_result.append(item[1:])
                else:
                    final_result.append(item)

                if item == '\n':
                    line_number += 1
                    print(item, line_number)
            else:
                final_result += item

        return list(filter(lambda x: x != '', final_result))

    def scan(self):
        file_content = self.read_file()
        print(file_content)
        tokens = self.split_in_tokens()
        print(tokens)
        for token in tokens:
            #print("Token {}".format(token))
            if self.is_separator(token):
                self.__program_internal_form.append((token, -1, 0))
            elif self.is_operator(token):
                self.__program_internal_form.append((token, -1, 1))
            elif self.is_keyword(token):
                self.__program_internal_form.append((token, -1, 2))
            elif self.is_identifier(token):
                self.__symbol_table.add_element(token)
                position_in_symbol_table = self.__symbol_table.get_element_position(token)
                self.__program_internal_form.append((token, position_in_symbol_table, 3))
            elif self.is_constant(token):
                self.__symbol_table.add_element(token)
                position_in_symbol_table = self.__symbol_table.get_element_position(token)
                self.__program_internal_form.append((token, position_in_symbol_table, 4))
            else:
                print("Lexical error:{}".format(token))
                return (-1, -1)

        return (self.__symbol_table, self.__program_internal_form)
