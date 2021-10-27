from scanner import Scanner

scanner = Scanner("p2.txt")
symbol_table, program_internal_form = scanner.scan()
print("Symbol table: {}".format(symbol_table))
print("PIF: {}".format(program_internal_form))


