from ParseException import ParseException


class RecursiveDescentParser:
    def __init__(self, grammar, configuration):
        self.__grammar = grammar
        self.__configuration = configuration

    def run(self, sequence):
        step = 0
        while self.__configuration.get_state() != 'f' and self.__configuration.get_state() != 'e':
            step += 1
            head_of_the_input_stack = self.__configuration.get_input_stack()[-1]
            head_of_the_working_stack = self.__configuration.get_working_stack()[-1]
            print("Step {} -> State: {}; Current position: {}; Working stack: {}; Input stack: {}".format(
                step,
                self.__configuration.get_state(), self.__configuration.get_current_position(),
                self.__configuration.get_working_stack(), self.__configuration.get_input_stack()))

            if self.__configuration.get_state() == 'q':
                if self.__configuration.get_current_position() == len(sequence) and head_of_the_input_stack == '$':
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
        for index in range(len(first_production) - 1, -1, -1):
            self.__configuration.push_to_input_stack(first_production[index])
        self.__configuration.push_to_working_stack((head_of_the_input_stack, 0))
        print("expand -> head input: {}".format(head_of_the_input_stack))

    def advance(self):
        self.__configuration.set_current_position(self.__configuration.get_current_position() + 1)
        head_of_the_input_stack = self.__configuration.pop_from_input_stack()
        self.__configuration.push_to_working_stack(head_of_the_input_stack)
        print("advance -> head input: {}; current position: {}".format(head_of_the_input_stack, self.__configuration.get_current_position()))

    def momentary_insuccess(self):
        self.__configuration.set_state('b')
        print("momentary insuccess")

    def back(self):
        terminal = self.__configuration.pop_from_working_stack()
        current_position = self.__configuration.get_current_position()
        self.__configuration.set_current_position(current_position - 1)
        self.__configuration.push_to_input_stack(terminal)
        print("back -> current position: {}".format(current_position))

    def another_try(self):
        print("another try")
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
        elif self.__configuration.get_current_position() == 0 and self.__configuration.get_working_stack()[-1] == self.__grammar.get_start_symbol():
            self.__configuration.set_state('e')
        else:
            self.__configuration.pop_from_working_stack()
            for _ in productions:
                self.__configuration.pop_from_input_stack()
            self.__configuration.push_to_input_stack(head_of_the_working_stack[0])

    def success(self):
        self.__configuration.set_state('f')
        print("success")
