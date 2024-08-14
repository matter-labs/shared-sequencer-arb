def compute_arb_cost_under_shared_seq(
    failure_outcome_A: int,
    failure_outcome_B: int,
    gas_cost_A_success: float,
    gas_cost_B_success: float,
    gas_cost_A_fail: float,
    gas_cost_B_fail: float,
) -> float:
    if failure_outcome_A == 0 and failure_outcome_B == 0:
        arb_cost = gas_cost_A_success + gas_cost_B_success
    else:
        arb_cost = gas_cost_A_fail + gas_cost_B_fail
    return arb_cost


def compute_arb_cost_under_indep_seq(
    failure_outcome_A: int,
    failure_outcome_B: int,
    gas_cost_A_success: float,
    gas_cost_B_success: float,
    gas_cost_A_fail: float,
    gas_cost_B_fail: float,
) -> float:
    arb_cost = (
        gas_cost_A_success * (1 - failure_outcome_A)
        + gas_cost_A_fail * failure_outcome_A
        + gas_cost_B_success * (1 - failure_outcome_B)
        + gas_cost_B_fail * failure_outcome_B
    )
    return arb_cost
