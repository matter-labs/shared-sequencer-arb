class Rollup:
    def __init__(
        self,
        fail_rate: float,
        gas_price_mean: float,
        gas_price_std: float,
        gas_units_swap: float,
        gas_units_fail: float,
    ) -> None:
        self.fail_rate = fail_rate
        self.gas_price_mean = gas_price_mean
        self.gas_price_std = gas_price_std
        self.gas_units_swap = gas_units_swap
        self.gas_units_fail = gas_units_fail

    def get_fail_rate(self) -> float:
        return self.fail_rate

    def get_gas_price_mean(self) -> float:
        return self.gas_price_mean

    def get_gas_price_std(self) -> float:
        return self.gas_price_std

    def get_gas_units_swap(self) -> float:
        return self.gas_units_swap

    def get_gas_units_fail(self) -> float:
        return self.gas_units_fail
