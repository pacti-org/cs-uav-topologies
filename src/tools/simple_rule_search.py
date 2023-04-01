from src.grammar.grammar import Grammar
from src.grammar.grid import LocalState
from src.grammar.rule import Rule


def set_rules_search(local_state: LocalState, grammar: Grammar, rules_allowed: list[str]) -> list[Rule]:
    rules_compatible: list[Rule] = []

    for r_name, rule in grammar.rules.items():
        if r_name not in rules_allowed:
            continue

        if local_state.matches(rule):
            rules_compatible.append(rule)

    return rules_compatible
