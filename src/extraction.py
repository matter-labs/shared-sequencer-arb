import pandas as pd

import cost
import failure
from rollup import Rollup
from gas import GasPriceModel
from pool import Pool
from revenue import compute_arb_revenue


def run_arb_profit_simulation(
    n_iter: int,
    rollup_A: Rollup,
    rollup_B: Rollup,
    pool_1: Pool,
    pool_2: Pool,
) -> pd.DataFrame:
    # Generate failure outcomes
    failure_outcomes_A = failure.generate_bernoulli_failure_outcomes(
        rollup_A.get_fail_rate(), n_iter
    )
    failure_outcomes_B = failure.generate_bernoulli_failure_outcomes(
        rollup_B.get_fail_rate(), n_iter
    )
    # Generate gas prices
    gas_prices_A = rollup_A.generate_gas_prices(n_iter)
    gas_prices_B = rollup_B.generate_gas_prices(n_iter)
    # Compute profit under each regime - shared and independent sequencing
    arb_sim_df = pd.DataFrame()
    for i in range(n_iter):
        i_arb_revenue = compute_arb_revenue(
            pool_1, pool_2, failure_outcomes_A[i], failure_outcomes_B[i]
        )
        i_arb_cost_under_shared_seq = cost.compute_arb_cost_under_shared_seq(
            failure_outcomes_A[i],
            failure_outcomes_B[i],
            gas_prices_A[i] * rollup_A.get_gas_units_swap(),  # gas cost if sucess
            gas_prices_B[i] * rollup_B.get_gas_units_swap(),  # gas cost if sucess
            gas_prices_A[i] * rollup_A.get_gas_units_fail(),  # gas cost if failure
            gas_prices_B[i] * rollup_B.get_gas_units_fail(),  # gas cost if failure
        )

        i_arb_cost_under_indep_seq = cost.compute_arb_cost_under_indep_seq(
            failure_outcomes_A[i],
            failure_outcomes_B[i],
            gas_prices_A[i] * rollup_A.get_gas_units_swap(),  # gas cost if sucess
            gas_prices_B[i] * rollup_B.get_gas_units_swap(),  # gas cost if sucess
            gas_prices_A[i] * rollup_A.get_gas_units_fail(),  # gas cost if failure
            gas_prices_B[i] * rollup_B.get_gas_units_fail(),  # gas cost if failure
        )
        i_profit_under_shared_seq = i_arb_revenue - i_arb_cost_under_shared_seq
        i_profit_under_indep_seq = i_arb_revenue - i_arb_cost_under_indep_seq
        iter_df = pd.DataFrame(
            {
                "iter": [i],
                "arb_revenue": [i_arb_revenue],
                "profit_under_shared_seq": [i_profit_under_shared_seq],
                "profit_under_indep_seq": [i_profit_under_indep_seq],
                "shared_sequencing_gain": [
                    i_profit_under_shared_seq - i_profit_under_indep_seq
                ],
            }
        )
        arb_sim_df = pd.concat([arb_sim_df, iter_df], ignore_index=True)
    return arb_sim_df


if __name__ == "__main__":
    # Define rollup settings -> based on data
    gas_price_model_A = GasPriceModel(
        model_type="gaussian", gas_price_mean=0.01, gas_price_std=0.0001
    )
    rollup_A = Rollup(
        fail_rate=0.3,
        gas_price_model=gas_price_model_A,
        gas_units_swap=10.0,
        gas_units_fail=1.0,
    )
    gas_price_model_B = GasPriceModel(
        model_type="gaussian", gas_price_mean=0.01, gas_price_std=0.0001
    )
    rollup_B = Rollup(
        fail_rate=0.3,
        gas_price_model=gas_price_model_B,
        gas_units_swap=10.0,
        gas_units_fail=1.0,
    )
    # Define pool settings -> based on data
    pool_1 = Pool(reserve_x=1000, reserve_y=1000, fee=0.005)
    pool_2 = Pool(reserve_x=1050, reserve_y=1000, fee=0.005)
    # Run simulation
    n_iter = 10
    arb_sim_df = run_arb_profit_simulation(n_iter, rollup_A, rollup_B, pool_1, pool_2)
    arb_sim_df.to_csv("./data/test_arb_sim_df.csv")
