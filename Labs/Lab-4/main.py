from scanner import Scanner

files = ['p1', 'p2', 'p3', 'p1err']

for file in files:
    print("=====================================================================")
    print("File {}:".format(file+".txt"))
    scanner = Scanner(file+".txt")
    scanner_output = scanner.scan()
    symbol_table, program_internal_form = scanner_output[0], scanner_output[1]
    print("Symbol table: {}".format(symbol_table))
    print("PIF: {}".format(program_internal_form))
    symbol_table_file_handler = open(file+"_st.txt", "w")
    program_internal_form_file_handler = open(file+"_pif.txt", "w")
    symbol_table_file_handler.write(str(symbol_table))

    for tuple in program_internal_form:
        if tuple[-1] == 3:
            program_internal_form_file_handler.write("(id, {})".format(tuple[1])+"\n")
        elif tuple[-1] == 4:
            program_internal_form_file_handler.write("(const, {})".format(tuple[1])+"\n")
        else:
            program_internal_form_file_handler.write("('{}', 0)".format(tuple[0][0])+"\n")

    if len(scanner_output) > 2:
        program_internal_form_file_handler.write(scanner_output[2])

    print("=====================================================================")


