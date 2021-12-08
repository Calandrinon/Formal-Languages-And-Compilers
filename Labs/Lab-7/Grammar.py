class Grammar:
    def __init__(self, filename):
        self.__filename = filename
        self.__filelines_with_productions = None
        self.read_grammar()
        self.__nonterminals = self.get_set_of_nonterminals()
        self.__terminals = self.get_set_of_terminals()
        self.__productions = self.__analyze_file_for_productions()
        self.__start_symbol = self.__nonterminals[0]

    def get_start_symbol(self):
        return self.__start_symbol

    def read_grammar(self):
        file_handler = open(self.__filename, "r")
        self.__filelines_with_productions = list(map(lambda line: line.strip(), file_handler.readlines()))
        self.__nonterminals = self.__filelines_with_productions[0].split(" ")
        self.__terminals = self.__filelines_with_productions[1].split(" ")
        self.__filelines_with_productions = list(map(lambda production: production.split(":="), self.__filelines_with_productions[2:]))
        return self.__filelines_with_productions

    def remove_empty_character_from_list(self, input_list):
        return list(filter(lambda x: x != '', input_list))

    def get_set_of_nonterminals(self):
        return self.__nonterminals

    def get_set_of_terminals(self):
        return self.__terminals

    def get_set_of_productions(self):
        return self.__productions

    def __analyze_file_for_productions(self):
        productions = {}

        for production in self.__filelines_with_productions:
            if production == ['']:
                continue
            production[0] = production[0].replace(" ", "")
            split_right_hand_side = production[1].strip().split("|")
            production[1] = list(map(lambda x: self.remove_empty_character_from_list(x.split(" ")), split_right_hand_side))
            productions[production[0]] = production[1]

        return productions

    def get_productions_of_a_nonterminal(self, nonterminal):
        if nonterminal not in self.__nonterminals:
            return None
        return self.__productions[nonterminal]

    def check_if_context_free(self):
        file_handler = open(self.__filename, "r")
        file_productions = list(map(lambda line: line.strip(), file_handler.readlines()[2:]))

        for file_production in file_productions:
            if file_production == "":
                continue
            left_hand_side = file_production.split(":=")[0]
            left_hand_side_tokens = self.remove_empty_character_from_list(left_hand_side.split(" "))
            if len(left_hand_side_tokens) != 1 or left_hand_side_tokens[0] not in self.__nonterminals:
                return False

        return True

