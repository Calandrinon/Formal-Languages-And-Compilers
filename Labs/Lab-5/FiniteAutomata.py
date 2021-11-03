class FiniteAutomata:
    def __init__(self, filename):
        self.__filename = filename
        self.__file = None

    def read_file(self):
        file_handler = open(self.__filename, "r")
        self.__file = file_handler.readlines()
        return self.__process_file_content()

    def __process_file_content(self):
        self.__file = list(map(lambda x: x.strip(), self.__file))
        self.__file = list(map(lambda x: x.replace("{", "").replace("}", ""), self.__file))
        set_of_states_as_string, alphabet_as_string, transitions_as_string, set_of_final_states_as_string = self.__file
        set_of_states = set_of_states_as_string.replace(" ", "").split(',')
        alphabet = alphabet_as_string.replace(" ", "").split(",")
        transitions_as_list_of_strings = transitions_as_string.replace("(", "").replace(")", "").replace(" ", "").split(
            ",")
        transitions = []
        for index in range(0, len(transitions_as_list_of_strings), 3):
            transitions.append((transitions_as_list_of_strings[index], transitions_as_list_of_strings[index + 1],
                                transitions_as_list_of_strings[index + 2]))
        set_of_final_states = set_of_final_states_as_string.replace("{", "").replace("}", "").replace(" ", "").split(
            ",")

        return (set_of_states, alphabet, transitions, set_of_final_states)


finite_automata = FiniteAutomata("FA.in")
finite_automata_as_tuple = finite_automata.read_file()
print(finite_automata_as_tuple)
