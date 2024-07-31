import math
from pool import Pool


def compute_arb_revenue(
    pool_1: Pool, pool_2: Pool, failure_outcome_A: int, failure_outcome_B: int
) -> float:
    if pool_1.get_price_in_y_units() <= pool_2.get_price_in_y_units():
        raise Exception("The first pool must have a high price than the second pool!")
    sucess_arb_revenue = compute_arb_profit_when_sucess(pool_1, pool_2)
    arb_revenue = sucess_arb_revenue * (1 - failure_outcome_A) * (1 - failure_outcome_B)
    return arb_revenue


def compute_arb_profit_when_sucess(pool_1: Pool, pool_2: Pool) -> float:
    # Note that we are assuming that the first pool will have a higher price than the second!
    reserve_x_1 = pool_1.get_reserve_x()
    reserve_y_1 = pool_1.get_reserve_y()
    fee_1 = pool_1.get_fee()
    reserve_x_2 = pool_2.get_reserve_x()
    reserve_y_2 = pool_2.get_reserve_y()
    fee_2 = pool_2.get_fee()
    # Compute auxliary variables (check derivation on overleaf)
    a = reserve_x_2 * reserve_y_1 * (1 - fee_1) * (1 - fee_2)
    b = reserve_x_1 * reserve_y_2
    c = reserve_x_1 * (1 - fee_2) + reserve_x_2 * (1 - fee_1) * (1 - fee_2)
    # Compute optimal trade size
    delta_y_2 = (math.sqrt(a * b) - b) / c
    # Compute profit
    profit = a * delta_y_2 / (b + c * delta_y_2) - delta_y_2
    return profit
