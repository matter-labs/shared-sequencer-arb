class Pool:
    def __init__(
        self, reserve_x: float, reserve_y: float, fee: float, type: str = "CPMM"
    ) -> None:
        self.reserve_x = reserve_x
        self.reserve_y = reserve_y
        self.fee = fee
        self.type = type
        self.liquidity = reserve_x * reserve_y

    def get_reserve_x(self) -> float:
        return self.reserve_x

    def get_reserve_y(self) -> float:
        return self.reserve_y

    def get_fee(self) -> float:
        return self.fee

    def get_price_in_y_units(self) -> float:
        return self.reserve_y / self.reserve_x
