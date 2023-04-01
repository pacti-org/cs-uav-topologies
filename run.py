import random
import numpy as np
import matplotlib.pyplot as plt
from src.tools.plotting import create_gif
from src.contracts_utils.union import ContractsUnions
from src.grammar.grammar import Grammar
from src.grammar.grid import GridBuilder
from src.shared import DirectionsAssignment, SymbolType
from src.shared.paths import rules_path
from src.tools.refinement_checking import rule_matching


grid_half_size = 3
max_num_wings = 2
max_num_rotors = 4

if __name__ == "__main__":
    grammar = Grammar.from_json(rules_json_path=rules_path)
    directions_assignment = DirectionsAssignment()
    directions_assignment.set_direction_assignment(grammar.get_directions_assignment())
    print(f"Direction assignment: {directions_assignment.data}")
    rule_contracts: dict[SymbolType, list[ContractsUnions]] = grammar.to_contracts()
    grid = GridBuilder.generate(half_size=grid_half_size)
    step = 0
    figures: list[plt.Figure] = []
    while len(grid.points_to_visit) > 0:
        # print(f"STEP {step}")
        # print(f"{len(grid.points_to_visit)} POINTS LEFT:\t{grid.points_to_visit}")
        grid.update_current_point()
        current_state = grid.local_state()
        if step > 0 and not current_state.has_non_empty_symbols():
            continue
        forbidden_symbols = set()
        if grid.n_wings == max_num_wings and grid.n_rotors == max_num_rotors:
            break
        if grid.n_wings >= max_num_wings:
            forbidden_symbols.add(SymbolType.WING)
        if grid.n_rotors >= max_num_rotors:
            forbidden_symbols.add(SymbolType.ROTOR)
        rules_allowed_contracts = list({k: v for k, v in rule_contracts.items() if k not in forbidden_symbols}.values())
        rules_allowed_contracts = [item for sublist in rules_allowed_contracts for item in sublist]
        if step > 0:
            rules_allowed_contracts = list(filter(lambda x: x.name != "r0", rules_allowed_contracts))
        rule_names_allowed = [r.name for r in rules_allowed_contracts]
        if step == 0:
            rules_compatible_contracts = [grammar.rules["r0"]]
        else:
            rules_compatible_contracts = rule_matching(current_state.contract, rules_allowed_contracts)
        r_id_from_contracts = [rc.name for rc in rules_compatible_contracts]
        r_id_from_contracts_str = "-".join(sorted(r_id_from_contracts))
        # print(f"R_C: {r_id_from_contracts_str}")
        if len(list(rules_compatible_contracts)) > 0:
            chosen_rule = random.choice(list(rules_compatible_contracts))
            grid.apply_rule(grammar.rules[chosen_rule.name])
        else:
            grid.apply_rule(grammar.rules["r19"])
        fig: plt.Figure = grid.figure_with_edges
        figures.append(fig)
        # Increase step counter
        step += 1

    grid.cleanup()
    figures.append(grid.figure_with_edges)
    gif_path = create_gif(figures=figures, filename="uav_design_process.gif")
