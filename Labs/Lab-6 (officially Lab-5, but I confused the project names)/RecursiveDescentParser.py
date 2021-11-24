from ParseException import ParseException

class RecursiveDescentParser:
    def __init__(self, grammar, configuration):
        self.__grammar = grammar
        self.__configuration = configuration

    def run(self, sequence):
        while self.__configuration.get_state() != 'f' and self.__configuration.get_state() != 'e':
            head_of_the_input_stack = self.__configuration.get_input_stack()[-1]
            head_of_the_working_stack = self.__configuration.get_working_stack()[-1]

            if self.__configuration.get_state() == 'q':
                if self.__configuration.get_current_position() == len(sequence) + 1 and head_of_the_input_stack == '$':
                    self.success()
                elif head_of_the_input_stack in self.__grammar.get_set_of_nonterminals():
                    self.expand()
                elif head_of_the_input_stack == sequence[self.__configuration.get_current_position()]:
                    self.advance()
                else:
                    self.momentary_insuccess()
            elif self.__configuration.get_state() == 'b':
                if head_of_the_working_stack in self.__grammar.get_set_of_terminals():
                    self.back()
                else:
                    self.another_try()

        if self.__configuration.get_state() == 'e':
            raise ParseException("An error has been detected.")
        print("Sequence accepted.")

    def expand(self):
        head_of_the_input_stack = self.__configuration.pop_from_input_stack()
        first_production = self.__grammar.get_productions_of_a_nonterminal(head_of_the_input_stack)[0]
        for symbol in first_production:
            self.__configuration.push_to_input_stack(symbol)
        self.__configuration.push_to_working_stack((head_of_the_input_stack, 0))

    def advance(self):
        self.__configuration.set_current_position(self.__configuration.get_current_position() + 1)
        head_of_the_input_stack = self.__configuration.pop_from_input_stack()
        self.__configuration.push_to_working_stack(head_of_the_input_stack)

    def momentary_insuccess(self):
        self.__configuration.set_state('b')

    def back(self):
        terminal = self.__configuration.pop_from_working_stack()
        current_position = self.__configuration.get_current_position()
        self.__configuration.set_current_position(current_position - 1)
        self.__configuration.push_to_input_stack(terminal)

    def another_try(self):
        head_of_the_working_stack = self.__configuration.get_working_stack()[-1]
        productions = self.__grammar.get_productions_of_a_nonterminal(head_of_the_working_stack[0])

        if head_of_the_working_stack[1] + 1 < len(productions):
            self.__configuration.set_state('q')
            new_head_of_the_working_stack = productions[head_of_the_working_stack[1] + 1]
            for _ in productions:
                self.__configuration.pop_from_input_stack()

            self.__configuration.pop_from_working_stack()
            self.__configuration.push_to_working_stack(new_head_of_the_working_stack)

            self.__grammar.get_productions_of_a_nonterminal()
        elif self.__configuration.get_current_position() == 0  and self.__configuration.get_working_stack()[-1] == self.__grammar.get_start_symbol():
            self.__configuration.set_state('e')
        else:
            self.__configuration.pop_from_working_stack()
            for _ in productions:
                self.__configuration.pop_from_input_stack()
            self.__configuration.push_to_input_stack(head_of_the_working_stack[0])

    def success(self):
        self.__configuration.set_state('f')
