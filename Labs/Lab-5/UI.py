
class UI:
    def __init__(self, finite_automaton):
        self.__finite_automaton = finite_automaton
        self.__finite_automaton_as_tuple = self.__finite_automaton.read_file()
        self.__running = True

    def __print_menu(self):
        print("""
        Display:
            1. the states of the FA
            2. the alphabet
            3. the transitions
            4. the set of final states
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

    def __print_set_of_final_states(self):
        print(self.__finite_automaton_as_tuple[3])

    def __clear_terminal(self):
        print("\n"*100)

    def run(self):
        options = [self.__exit_loop, self.__print_states, self.__print_alphabet,
                   self.__print_transitions, self.__print_set_of_final_states]

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

