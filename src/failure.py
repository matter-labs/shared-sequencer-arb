from scipy.stats import bernoulli
from typing import List


def generate_bernoulli_failure_outcomes(fail_rate: float, n_outcomes: int) -> List[int]:
    outcomes = bernoulli.rvs(fail_rate, size=n_outcomes)
    return outcomes
