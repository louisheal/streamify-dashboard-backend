from flask import jsonify

class User:
    def __init__(self, username, display_name, avatar_url, discount_code, discount_amount, orders, withdrawals):
        self.username        = username
        self.display_name    = display_name
        self.avatar_url      = avatar_url
        self.discount_code   = discount_code
        self.discount_amount = discount_amount
        self.orders          = orders
        self.withdrawals     = withdrawals
        self.balance         = self.__calculate_balance(orders)
        self.sales           = len(orders)
    
    # TODO: Add withdrawals to calculation
    def __calculate_balance(self, orders):
        prices = [order['price_gbp'] for order in orders]
        return sum(prices)
    
    def toJson(self):
        return jsonify(
            username=self.username,
            displayName=self.display_name,
            avatarUrl=self.avatar_url,
            discountCode=self.discount_code,
            discountAmount=self.discount_amount,
            orders=self.orders,
            withdrawals=self.withdrawals,
            balance=self.balance,
            sales=self.sales
        )
