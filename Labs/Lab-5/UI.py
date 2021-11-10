
class UI:
    def __init__(self, finite_automaton):
        self.__finite_automaton = finite_automaton
        self.__finite_automaton_as_tuple = self.__finite_automaton.read_file()
        self.__running = True

    def __print_menu(self):
        print("""
            1. Display the states of the FA
            2. Display the alphabet
            3. Display the transitions
            4. Display the initial state
            5. Display the set of final states
            6. Check if a sequence is accepted by the finite automaton (which has to be deterministic)
          or ...
            0. Exit
        """)

    def __exit_loop(self):
        self.__running = False

    def __print_states(self):
        print(self.__finite_automaton_as_tuple[0])

    def __print_alphabet(self):
        print(self.__finite_automaton_as_tuple[1])

    def __print_transitions(self):
        print(self.__finite_automaton_as_tuple[2])

    def __print_initial_state(self):
        print(self.__finite_automaton_as_tuple[3])

    def __print_set_of_final_states(self):
        print(self.__finite_automaton_as_tuple[4])

    def __check_sequence_validity(self):
        if not self.__finite_automaton.is_a_deterministic_finite_automaton():
            print("The automaton has to be deterministic.")
            return

        sequence = input("Enter the sequence: ")
        is_accepted = self.__finite_automaton.check_sequence(sequence)
        print("The automaton {} the sequence {}".format("accepts" if is_accepted else "doesn't accept", sequence))

    def __clear_terminal(self):
        print("\n"*100)

    def run(self):
        options = [self.__exit_loop, self.__print_states, self.__print_alphabet,
                   self.__print_transitions, self.__print_initial_state, self.__print_set_of_final_states,
                   self.__check_sequence_validity]

        while self.__running:
            self.__print_menu()
            try:
                option = int(input("Enter an option:"))
                self.__clear_terminal()
                options[option]()
            except IndexError as ie:
                print(ie)
                print("The number entered should be between {} and {}.".format(0, len(options) - 1))
            except ValueError as ve:
                print(ve)
                print("The value entered should be a number.")

