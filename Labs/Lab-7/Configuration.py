class Configuration:
    def __init__(self, state, current_position, working_stack, input_stack):
        self.__state = state
        self.__current_position = current_position
        self.__working_stack = working_stack
        self.__input_stack = input_stack

    @staticmethod
    def create_default_configuration_for_grammar(grammar):
        configuration = Configuration('q', 0, [], [])
        configuration.push_to_working_stack('$')
        configuration.push_to_input_stack('$')
        configuration.push_to_input_stack(grammar.get_start_symbol())
        return configuration

    def push_to_working_stack(self, element):
        self.__working_stack.append(element)

    def pop_from_working_stack(self):
        return self.__working_stack.pop()

    def push_to_input_stack(self, element):
        self.__input_stack.append(element)

    def pop_from_input_stack(self):
        return self.__input_stack.pop()

    def get_state(self):
        return self.__state

    def set_state(self, state):
        self.__state = state

    def get_current_position(self):
        return self.__current_position

    def set_current_position(self, current_position):
        self.__current_position = current_position

    def get_working_stack(self):
        return self.__working_stack

    def set_working_stack(self, working_stack):
        self.__working_stack = working_stack

    def get_input_stack(self):
        return self.__input_stack

    def set_input_stack(self, input_stack):
        self.__input_stack = input_stack

