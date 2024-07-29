def compute_arb_revenue(failure_outcome_A: int, failure_outcome_B: int) -> float:
    sucess_arb_revenue = 1.0
    arb_revenue = sucess_arb_revenue * (1 - failure_outcome_A) * (1 - failure_outcome_B)
    return arb_revenue
