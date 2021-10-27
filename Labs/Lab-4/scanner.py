import functools

from SymbolTable import SymbolTable
import re

class Scanner:
    def __init__(self, input_filename):
        self.__separators = [' ', ';', ':', '{', '}', '[', ']', '(', ')', ',']
        self.__separators_for_regex_pattern = [' ', ';', ':', '\{', '\}', '\[', '\]', '\(', '\)']
        self.__operators = ['+', '-', '*', '/', '%', '=', '==', '<', '>', '<=', '>=']
        self.__keywords = ["defvar", "deflist", "and", "or", "not", "if", "else", "loop", "input", "print", "int", "str", "char", "bool", "double"]
        self.__input_filename = input_filename
        self.__file = None
        self.__symbolTable = SymbolTable()
        self.__programInternalForm = []
        self.__space_tokenized_code = None

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
        self.__space_cleared_code = list(map(lambda row: list(map(lambda token: token.replace(' ', ''), row)), self.__space_tokenized_code))
        self.__space_cleared_code = [item for sublist in self.__space_cleared_code for item in sublist]
        self.__separator_tokenized_code = list(map(lambda token: self.extract_token_with_separators(token), self.__space_cleared_code))

        final_result = []
        for item in self.__separator_tokenized_code:
            if isinstance(item, str):
                if len(item) > 1 and item[0] == '-':
                    final_result.append('-')
                    final_result.append(item[1:])
                else:
                    final_result.append(item)
            else:
                final_result += item

        return list(filter(lambda x: x != '', final_result))

    def scan(self):
        file_content = self.read_file()
        print(file_content)
        tokens = self.split_in_tokens()
        print(tokens)
        for token in tokens:
            print("Token {}".format(token))
        return tokens
