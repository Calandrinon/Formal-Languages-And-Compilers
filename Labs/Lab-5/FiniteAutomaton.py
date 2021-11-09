class FiniteAutomaton:
    def __init__(self, filename):
        self.__filename = filename
        self.__file = None
        self.__graph_of_states = {}
        self.__automata_as_tuple = None

    def read_file(self):
        file_handler = open(self.__filename, "r")
        self.__file = file_handler.readlines()
        return self.__process_file_content()

    def build_graph_of_states(self):
        for state in self.__automata_as_tuple[0]:
            self.__graph_of_states[state] = []

        for transition in self.__automata_as_tuple[2]:
            first_state, second_state, symbol = transition
            self.__graph_of_states[first_state].append((second_state, symbol))

        return self.__graph_of_states

    def check_sequence(self, sequence):
        current_state = self.__automata_as_tuple[3]
        for symbol in sequence:
            transition_performed = False
            for transition in self.__graph_of_states[current_state]:
                if transition[1] == symbol:
                    current_state = transition[0]
                    transition_performed = True

            if not transition_performed:
                return False

        if current_state in self.__automata_as_tuple[4]:
            return True

    def __process_file_content(self):
        self.__file = list(map(lambda x: x.strip(), self.__file))
        self.__file = list(map(lambda x: x.replace("{", "").replace("}", ""), self.__file))
        set_of_states_as_string, alphabet_as_string, transitions_as_string, initial_state, set_of_final_states_as_string = self.__file
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

        self.__automata_as_tuple = (set_of_states, alphabet, transitions, initial_state, set_of_final_states)
        return self.__automata_as_tuple


finite_automaton = FiniteAutomaton("FA.in")
print(finite_automaton.read_file())
print(finite_automaton.build_graph_of_states())
print(finite_automaton.check_sequence("000000111"))
