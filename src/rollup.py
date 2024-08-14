from gas import GasPriceModel
from numpy.typing import NDArray


class Rollup:
    def __init__(
        self,
        fail_rate: float,
        gas_price_model: GasPriceModel,
        gas_units_swap: float,
        gas_units_fail: float,
    ) -> None:
        self.fail_rate = fail_rate
        self.gas_price_model = gas_price_model
        self.gas_units_swap = gas_units_swap
        self.gas_units_fail = gas_units_fail

    def get_fail_rate(self) -> float:
        return self.fail_rate

    def get_gas_price_model(self) -> GasPriceModel:
        return self.gas_price_model

    def get_gas_units_swap(self) -> float:
        return self.gas_units_swap

    def get_gas_units_fail(self) -> float:
        return self.gas_units_fail

    def generate_gas_prices(self, n_samples: int) -> NDArray:
        return self.gas_price_model.generate_gas_prices(n_samples)
