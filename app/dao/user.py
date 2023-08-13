class User:
    def __init__(self, username, discount_code, discount_amount, orders, withdrawals):
        self.username        = username
        self.discount_code   = discount_code
        self.discount_amount = discount_amount
        self.orders          = orders
        self.withdrawals     = withdrawals
        self.balance         = self.__calculate_balance(orders)
        self.sales           = len(orders)
    
    def __calculate_balance(self, orders):
        prices = [order['price_gbp'] for order in orders]
        return sum(prices)
