from dao.orders.order import Order
import dao.orders.order as order_dao


class User:
    def __init__(self, user_id: str, display_name: str, avatar_url: str, discount_code: str, discount_amount: float,
                 orders: [Order], payouts: [object], is_affiliate: bool):
        self.user_id = user_id
        self.display_name = display_name
        self.avatar_url = avatar_url
        self.discount_code = discount_code
        self.discount_amount = discount_amount
        self.orders = orders
        self.payouts = payouts
        self.is_affiliate = is_affiliate

    def __calculate_balance(self) -> str:
        amount = sum(order.amount for order in self.orders)
        dollars, cents = divmod(amount, 100)
        return f"${dollars}.{cents:02}"

    def __calculate_sales(self) -> int:
        return len(self.orders)

    def __create_order_data(self):
        return order_dao.orders_to_structure(self.orders)

    def jsonify(self):
        return {
            "user_id": self.user_id,
            "displayName": self.display_name,
            "avatarUrl": self.avatar_url,
            "discountCode": self.discount_code,
            "orders": self.__create_order_data(),
            "balance": self.__calculate_balance(),
            "sales": self.__calculate_sales(),
            "status": 'logged_in' if self.is_affiliate else 'login_failed'
        }
