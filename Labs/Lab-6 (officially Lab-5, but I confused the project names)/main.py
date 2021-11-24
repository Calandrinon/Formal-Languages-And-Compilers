from Grammar import Grammar
from RecursiveDescentParser import RecursiveDescentParser
from Configuration import Configuration


def main():
    grammar = Grammar("g2.txt")
    print("=" * 150)
    print("Grammar file content: {}".format(grammar.read_grammar()))
    print("=" * 150)
    print("Non-terminals: {}".format(grammar.get_set_of_nonterminals()))
    print("=" * 150)
    print("Terminals: {}".format(grammar.get_set_of_terminals()))
    print("=" * 150)
    print("Set of productions:")
    productions = grammar.get_set_of_productions()
    for key in productions:
        print("{} := {}".format(key, productions[key]))
    print("=" * 150)
    nonterminal = 'compound_statement'
    print("Set of productions for non-terminal {}: {}".format(nonterminal,
                                                              grammar.get_productions_of_a_nonterminal(nonterminal)))
    print("=" * 150)
    print("Is the grammar context-free? {}".format("Yes" if grammar.check_if_context_free() else "No"))
    print("=" * 150)

    parser = RecursiveDescentParser(grammar, Configuration.create_default_configuration_for_grammar(grammar))


main()
