import math

class shpitzer:
    def __init__(self, loan, months, r):
        self.color = 'blue'
        self.loan = loan
        self.madad = 106.2 #TODO where it should be count?
        self.months = months
        self.r = r
        self.monthly_ret = []
        self.monthly_fee = []
        self.monthly_total = []
        self.loan_left = []

    def build_table(self, loan, months, ribit):
        self.loan = loan
        self.months = months
        if self.months == 0:
            print("warning [build_table] period can't be 0, setting to months to 1 year")
            self.months = 12
        if ribit == 0:
            print("warning [build_table] ribit is 0, setting to ribit to 0.001")
            ribit = 0.001

        self.r = ribit
        rate = self.r / 100
        R = rate / 12
        cur_monthly_tot = ((R) / (1 - (1 / math.pow(1 + R, self.months)))) * self.loan

        self.monthly_ret = []
        self.monthly_fee = []
        self.monthly_total = []
        self.loan_left = []
        self.loan_left.append(self.loan)

        for i in range(0, int(self.months)):
            self.monthly_total.append(cur_monthly_tot)
            cur_monthly_fee = (self.loan_left[-1] * R)
            cur_monthly_ret = cur_monthly_tot - cur_monthly_fee

            self.monthly_ret.append(cur_monthly_ret)
            self.monthly_fee.append(cur_monthly_fee)
            if i < self.months - 1:
                self.loan_left.append(self.loan_left[-1] - cur_monthly_ret)

    def print_params(self):
        print("monthly return: ", self.monthly_ret)
        print("----------------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("monthly fee: ", self.monthly_fee)
        print("----------------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("monthly total: ", self.get_monthly_total())
        print("----------------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("left loan: ", self.loan_left)

    def get_monthly_return(self):
        return self.monthly_ret

    def get_monthly_fee(self):
        return self.monthly_fee

    def get_monthly_total(self):
        return self.monthly_total
        # return [x+y for x, y in zip(self.monthly_fee,self.monthly_ret)]

    def get_left_loan(self):
        return self.loan_left
