from Grammar import Grammar
from RecursiveDescentParser import RecursiveDescentParser
from Configuration import Configuration

def main():
    grammar = Grammar("g2.txt")
    print("Grammar file content: {}".format(grammar.read_grammar()))
    print("Non-terminals: {}".format(grammar.get_set_of_nonterminals()))
    print("Terminals: {}".format(grammar.get_set_of_terminals()))
    print("Set of productions:")
    productions = grammar.get_set_of_productions()
    for key in productions:
        print("LHS: {}; RHS: {}".format(key, productions[key]))
    nonterminal = 'compound_statement'
    print("Set of productions for non-terminal {}: {}".format(nonterminal, grammar.get_productions_of_a_nonterminal(nonterminal)))
    print("Is the grammar context-free? {}\n\n\n".format("Yes" if grammar.check_if_context_free() else "No"))

    parser = RecursiveDescentParser(grammar, Configuration.create_default_configuration_for_grammar(grammar))

main()