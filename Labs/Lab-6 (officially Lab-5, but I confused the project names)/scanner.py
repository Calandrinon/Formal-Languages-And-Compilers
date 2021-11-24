import functools

from SymbolTable import SymbolTable
import re

class Scanner:
    def __init__(self, input_filename):
        self.__separators = [' ', ';', ':', '{', '}', '[', ']', '(', ')', ',']
        self.__separators_for_regex_pattern = [' ', ';', ':', '\{', '\}', '\[', '\]', '\(', '\)']
        self.__operators = ['+', '-', '*', '/', '%', '=', '==', '<', '>', '<=', '>=', '+=', '**']
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
        for index in range(0, len(self.__file)):
            self.__file[index] = (self.__file[index], index)
        self.__space_tokenized_code = list(map(lambda line: (list(map(lambda token: (token, line[1]), re.findall(tokenization_pattern, line[0])))), self.__file))
        self.__space_cleared_code = list(map(lambda row: list(map(lambda token: (token[0].replace(' ', ''), token[1]), row)), self.__space_tokenized_code))
        self.__space_cleared_code = [item for sublist in self.__space_cleared_code for item in sublist]
        self.__separator_tokenized_code = list(map(lambda token: (self.extract_token_with_separators(token[0]), token[1]), self.__space_cleared_code))

        final_result = []
        line_number = 0

        for item in self.__separator_tokenized_code:
            if isinstance(item[0], str):
                if len(item[0]) > 1 and item[0][0] == '-':
                    final_result.append(('-', item[1]))
                    final_result.append((item[0][1:], item[1]))
                else:
                    final_result.append((item[0], item[1]))
            else:
                final_result += list(map(lambda x: (x, item[1]), item[0]))

        return list(filter(lambda x: x[0] != '', final_result))

    def scan(self):
        file_content = self.read_file()
        tokens = self.split_in_tokens()

        for token in tokens:
            if self.is_separator(token[0]):
                self.__program_internal_form.append((token, -1, 0))
            elif self.is_operator(token[0]):
                self.__program_internal_form.append((token, -1, 1))
            elif self.is_keyword(token[0]):
                self.__program_internal_form.append((token, -1, 2))
            elif self.is_identifier(token[0]):
                self.__symbol_table.add_element(token[0])
                position_in_symbol_table = self.__symbol_table.search_element(token[0])
                self.__program_internal_form.append((token, position_in_symbol_table, 3))
            elif self.is_constant(token[0]):
                self.__symbol_table.add_element(token[0])
                position_in_symbol_table = self.__symbol_table.search_element(token[0])
                self.__program_internal_form.append((token, position_in_symbol_table, 4))
            else:
                print("Lexical error -> Token: {}; Line: {};".format(token[0], token[1]+1))
                return (self.__symbol_table, self.__program_internal_form, "Lexical error -> Token: {}; Line: {};".format(token[0], token[1]+1))

        return (self.__symbol_table, self.__program_internal_form)
