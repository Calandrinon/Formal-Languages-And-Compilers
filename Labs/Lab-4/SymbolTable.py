
class SymbolTable:
    def __init__(self):
        self.__table = {}

    def ascii_hash(self, input):
        if not isinstance(input, str):
            raise Exception("The stored values of the hash table have to be strings.")

        ascii_codes_sum = 0
        for character in input:
            ascii_codes_sum += ord(character)

        return ascii_codes_sum

    def is_key_in_table(self, key):
        try:
            dummy_assignment = self.__table[key]
            return True
        except KeyError as ke:
            return False

    def add_element(self, element):
        key = self.ascii_hash(element)
        if not self.is_key_in_table(key):
            self.__table[key] = [element]
            return (key, 0)
        elif element not in self.__table[key]:
            self.__table[key].append(element)
            return (key, len(self.__table[key]) - 1)
        return -1

    def search_element(self, element):
        key = self.ascii_hash(element)
        if self.is_key_in_table(key):
            return (key, self.__table[key].index(element))
        return False

    def __str__(self):
        return str(self.__table)

"""
symbol_table = SymbolTable()
print("Adding \"some_identifier\" to the symbol table... Returned value from add_element: {}".format(symbol_table.add_element("some_identifier")))
print("Adding \"some_constant\" to the symbol table... Returned value from add_element: {}".format(symbol_table.add_element("some_constant")))
print("Adding \"a\" to the symbol table... Returned value from add_element: {}".format(symbol_table.add_element("a")))
print("Adding \"a\" to the symbol table... Returned value from add_element: {}".format(symbol_table.add_element("a")))
print("Is a in the table? {}".format(symbol_table.search_element("a")))
print("Is b in the table? {}".format(symbol_table.search_element("b")))
print("\nHash collision example:")
print("Adding \"ac\" to the symbol table... Returned value from add_element: {}".format(symbol_table.add_element("ac")))
print("Adding \"bb\" to the symbol table... Returned value from add_element: {}".format(symbol_table.add_element("bb")))
print("Is ac in the table? {}".format(symbol_table.search_element("ac")))
print("Is bb in the table? {}".format(symbol_table.search_element("bb")))
print(str(symbol_table))
"""