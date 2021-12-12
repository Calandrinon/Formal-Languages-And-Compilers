from ParseException import ParseException


class RecursiveDescentParser:
    def __init__(self, grammar, configuration):
        self.__grammar = grammar
        self.__all_productions = grammar.get_set_of_productions()
        self.__configuration = configuration
        self.__sequence = None
        self.__parse_tree = []
        self.__last_applied_production = None
        self.__final_working_stack = None

    def run(self, sequence):
        step = 0
        self.__sequence = sequence
        while self.__configuration.get_state() != 'f' and self.__configuration.get_state() != 'e':
            step += 1
            head_of_the_input_stack = self.__configuration.get_input_stack()[-1]
            head_of_the_working_stack = self.__configuration.get_working_stack()[-1]
            print("Step {} -> State: {}; Current position: {}; Working stack: {}; Input stack: {}".format(
                step,
                self.__configuration.get_state(), self.__configuration.get_current_position(),
                self.__configuration.get_working_stack(), self.__configuration.get_input_stack()))
            if head_of_the_working_stack == '$' and self.__configuration.get_state() == 'b':
                self.__configuration.set_state('e')

            if self.__configuration.get_state() == 'q':
                if self.__configuration.get_current_position() == len(sequence) and head_of_the_input_stack == '$':
                    self.success()
                elif head_of_the_input_stack in self.__grammar.get_set_of_nonterminals():
                    self.expand()
                elif self.__configuration.get_current_position() < len(sequence) and head_of_the_input_stack == sequence[self.__configuration.get_current_position()]:
                    self.advance()
                else:
                    self.momentary_insuccess()
            elif self.__configuration.get_state() == 'b':
                if head_of_the_working_stack in self.__grammar.get_set_of_terminals():
                    self.back()
                else:
                    self.another_try()

        if self.__configuration.get_state() == 'e':
            raise ParseException("An error has been detected in the sequence {}.".format(''.join(sequence)))
        print("Sequence {} accepted.".format(''.join(sequence)))
        self.__final_working_stack = self.__configuration.get_working_stack()
        del self.__final_working_stack[0]
        return self.__configuration.get_working_stack()

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
        print("advance -> head input: {};".format(head_of_the_input_stack))
        self.__configuration.push_to_working_stack(head_of_the_input_stack)

    def momentary_insuccess(self):
        self.__configuration.set_state('b')
        print("momentary insuccess")

    def back(self):
        terminal = self.__configuration.pop_from_working_stack()
        current_position = self.__configuration.get_current_position()
        self.__configuration.set_current_position(current_position - 1)
        self.__configuration.push_to_input_stack(terminal)
        print("back -> current position: {}; symbol in sequence: {}".format(current_position, self.__sequence[current_position - 1]))

    def another_try(self):
        print("another try")
        head_of_the_working_stack = self.__configuration.get_working_stack()[-1]
        print("Head of the working stack: {}".format(head_of_the_working_stack))
        productions = self.__grammar.get_productions_of_a_nonterminal(head_of_the_working_stack[0])
        print("Productions of the non-terminal '{}': {}".format(head_of_the_working_stack[0], productions))

        if head_of_the_working_stack[1] + 1 < len(productions):
            self.__configuration.set_state('q')
            new_input_stack_content = productions[head_of_the_working_stack[1] + 1]
            for _ in productions[head_of_the_working_stack[1]]:
                self.__configuration.pop_from_input_stack()

            self.__configuration.pop_from_working_stack()
            self.__configuration.push_to_working_stack((head_of_the_working_stack[0], head_of_the_working_stack[1] + 1))

            for index in range(len(new_input_stack_content) - 1, -1, -1):
                self.__configuration.push_to_input_stack(new_input_stack_content[index])
        elif self.__configuration.get_current_position() == 0 and self.__configuration.get_working_stack()[-1] == self.__grammar.get_start_symbol():
            self.__configuration.set_state('e')
        else:
            self.__configuration.set_state('b')
            old_head_of_the_working_stack = self.__configuration.pop_from_working_stack()
            for _ in productions[old_head_of_the_working_stack[1]]:
                self.__configuration.pop_from_input_stack()
            self.__configuration.push_to_input_stack(old_head_of_the_working_stack[0])

    def success(self):
        self.__configuration.set_state('f')
        print("success")

    def get_string_of_productions(self):
        return list(filter(lambda element: type(element) is tuple, self.__final_working_stack))

    def print_parse_representation(self):
        print(self.get_string_of_productions())

