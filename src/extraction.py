import pandas as pd

import cost
import failure
from rollup import Rollup
from pool import Pool
from revenue import compute_arb_revenue


def run_arb_profit_simulation(
    n_iter: int, rollup_A: Rollup, rollup_B: Rollup
) -> pd.DataFrame:
    # Generate failure outcomes
    failure_outcomes_A = failure.generate_bernoulli_failure_outcomes(
        rollup_A.get_fail_rate(), n_iter
    )
    failure_outcomes_B = failure.generate_bernoulli_failure_outcomes(
        rollup_B.get_fail_rate(), n_iter
    )
    # Generate gas prices
    gas_prices_A = cost.generate_normal_gas_prices(
        rollup_A.get_gas_price_mean(), rollup_A.get_gas_price_std(), n_iter
    )
    gas_prices_B = cost.generate_normal_gas_prices(
        rollup_B.get_gas_price_mean(), rollup_B.get_gas_price_std(), n_iter
    )
    # Compute profit under each regime - shared and independent sequencing
    arb_sim_df = pd.DataFrame()
    for i in range(n_iter):
        i_profit_under_shared_seq = compute_arb_profit_under_shared_seq(
            failure_outcomes_A[i],
            failure_outcomes_B[i],
            gas_prices_A[i] * rollup_A.get_gas_units_swap(),  # gas cost if sucess
            gas_prices_B[i] * rollup_B.get_gas_units_swap(),  # gas cost if sucess
            gas_prices_A[i] * rollup_A.get_gas_units_fail(),  # gas cost if failure
            gas_prices_B[i] * rollup_B.get_gas_units_fail(),  # gas cost if failure
        )
        i_profit_under_indep_seq = compute_arb_profit_under_indep_seq(
            failure_outcomes_A[i],
            failure_outcomes_B[i],
            gas_prices_A[i] * rollup_A.get_gas_units_swap(),  # gas cost if sucess
            gas_prices_B[i] * rollup_B.get_gas_units_swap(),  # gas cost if sucess
            gas_prices_A[i] * rollup_A.get_gas_units_fail(),  # gas cost if failure
            gas_prices_B[i] * rollup_B.get_gas_units_fail(),  # gas cost if failure
        )
        iter_df = pd.DataFrame(
            {
                "iter": [i],
                "profit_under_shared_seq": [i_profit_under_shared_seq],
                "profit_under_indep_seq": [i_profit_under_indep_seq],
                "shared_sequencing_gain": [
                    i_profit_under_shared_seq - i_profit_under_indep_seq
                ],
            }
        )
        arb_sim_df = pd.concat([arb_sim_df, iter_df], ignore_index=True)
    return arb_sim_df


def compute_arb_profit_under_shared_seq(
    failure_outcome_A: int,
    failure_outcome_B: int,
    gas_cost_A_success: float,
    gas_cost_B_success: float,
    gas_cost_A_fail: float,
    gas_cost_B_fail: float,
) -> float:
    arb_revenue = compute_arb_revenue(failure_outcome_A, failure_outcome_B)
    arb_cost = cost.compute_arb_cost_under_shared_seq(
        failure_outcome_A,
        failure_outcome_B,
        gas_cost_A_success,
        gas_cost_B_success,
        gas_cost_A_fail,
        gas_cost_B_fail,
    )
    arb_profit = arb_revenue - arb_cost
    return arb_profit


def compute_arb_profit_under_indep_seq(
    failure_outcome_A: int,
    failure_outcome_B: int,
    gas_cost_A_success: float,
    gas_cost_B_success: float,
    gas_cost_A_fail: float,
    gas_cost_B_fail: float,
) -> float:
    arb_revenue = compute_arb_revenue(failure_outcome_A, failure_outcome_B)
    arb_cost = cost.compute_arb_cost_under_indep_seq(
        failure_outcome_A,
        failure_outcome_B,
        gas_cost_A_success,
        gas_cost_B_success,
        gas_cost_A_fail,
        gas_cost_B_fail,
    )
    arb_profit = arb_revenue - arb_cost
    return arb_profit


if __name__ == "__main__":
    # Define rollup settings -> based on data
    rollup_A = Rollup(
        fail_rate=0.3,
        gas_price_mean=0.01,
        gas_price_std=0.0001,
        gas_units_swap=10.0,
        gas_units_fail=1.0,
    )
    rollup_B = Rollup(
        fail_rate=0.3,
        gas_price_mean=0.01,
        gas_price_std=0.0001,
        gas_units_swap=10.0,
        gas_units_fail=1.0,
    )
    # Run simulation
    n_iter = 10
    arb_sim_df = run_arb_profit_simulation(n_iter, rollup_A, rollup_B)
    arb_sim_df.to_csv("./data/test_arb_sim_df.csv")
