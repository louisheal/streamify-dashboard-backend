from datetime import date, timedelta, datetime


class Order:
    def __init__(self, amount: float, order_date: date):
        self.amount = amount
        self.order_date = order_date

    def to_json(self):
        return {
            "amount": self.amount,
            "order_date": self.order_date
        }

    @classmethod
    def from_json(cls, data):
        return cls(
            data["amount"],
            data["order_date"]
        )


def orders_to_structure(orders):
    structure = __initialise_structure()

    for order in orders:
        month_year_key = order.order_date.strftime("%B %Y")
        if month_year_key in structure:
            day_index = order.order_date.day - 1
            structure[month_year_key]["data"][day_index] += (order.amount / 100.0)

    order_data = []
    for key, value in structure.items():
        order_data.append({
            'month': key,
            'labels': value['labels'],
            'data': value['data']
        })

    return order_data


def __initialise_structure():
    months = {}
    current_date = datetime.now()

    for _ in range(0, 3):
        months[current_date.strftime("%B %Y")] = __initialize_month(current_date)
        current_date = current_date - timedelta(days=current_date.day)

    return months


def __initialize_month(order_date):
    last_day = __last_day_of_month(order_date).day
    labels = [(order_date.replace(day=i)).strftime('%b %d') for i in range(1, last_day + 1)]
    data = [0.0] * last_day
    return {"labels": labels, "data": data}


def __last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)
