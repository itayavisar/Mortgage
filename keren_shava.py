
class keren_shava:
    def __init__(self, loan, months, r):
        self.color = 'green'
        self.loan = loan
        self.madad = 106.2
        self.months = months
        self.r = r
        self.rate = self.r / 100
        self.monthly_ret = []
        self.monthly_fee = []
        self.monthly_total = []
        self.loan_left = []

    def build_table(self, loan, months, ribit):
        self.loan = loan
        self.months = months
        if self.months == 0:
            print("warning period can't be 0, setting to months to 1 year")
            self.months = 12

        self.r = ribit
        self.rate = self.r / 100
        self.loan_left = []
        self.monthly_ret = []
        self.monthly_fee = []
        self.monthly_total = []
        self.loan_left = []
        self.loan_left.append(self.loan)

        for i in range(0, int(self.months)):
            cur_monthly_ret = (self.loan / self.months)
            cur_monthly_fee = (self.loan_left[-1] * (self.rate / 12))
            cur_monthly_tot = cur_monthly_ret + cur_monthly_fee
            self.monthly_total.append(cur_monthly_tot)
            self.monthly_ret.append(cur_monthly_ret)
            self.monthly_fee.append(cur_monthly_fee)
            if i < self.months - 1:
                self.loan_left.append(self.loan_left[-1] - cur_monthly_ret)

    def print_params(self):
        print("monthly return: ", self.monthly_ret)
        print("----------------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("monthly fee: ", self.monthly_fee)
        print("----------------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("monthly total: ", self.monthly_total)
        print("----------------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("left loan: ", self.loan_left)

    def get_monthly_return(self):
        return self.monthly_ret

    def get_monthly_fee(self):
        return self.monthly_fee

    def get_monthly_total(self):
        return self.monthly_total

    def get_left_loan(self):
        return self.loan_left

