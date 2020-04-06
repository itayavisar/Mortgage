class CONSTANTS:
    def __init__(self):
        self.early_return_functional_fee = 60 # Always have this fee
        self.early_notice_return_fee_period_in_days = 10 # early notice return fee won't pay if noted more then this days in advance
        self.early_notice_return_fee_percentage = 0.1 # fee is the percentage from the return amount
        self.tzmuda_fee = 0  # TODO ITAY ? if return is before 15 to month, we pay half of monthly madad, average over year
        # self.hivun_fee = 0 not constant