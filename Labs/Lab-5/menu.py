from UI import UI
from FiniteAutomaton import FiniteAutomaton


def main():
    finite_automaton = FiniteAutomaton("FA.in")
    ui = UI(finite_automaton)
    ui.run()


main()
