from datetime import timedelta


class Order:
    def __init__(self, amount: float):
        self.amount = amount

    def to_json(self):
        return {
            "amount": self.amount
        }

    @classmethod
    def from_json(cls, data):
        return cls(data["amount"])


def orders_to_structure(orders):
    structure = {}

    for order in orders:
        month_year_key = order.date.strftime("%B %Y")

        if month_year_key not in structure:
            structure[month_year_key] = __initialize_month(order.date)

        day_index = order.date.day - 1
        structure[month_year_key]["data"][day_index] += order.amount

    return structure


def __last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)


def __initialize_month(date):
    last_day = __last_day_of_month(date).day
    labels = [str(i).zfill(2) for i in range(1, last_day + 1)]
    data = [0.0] * last_day
    return {"labels": labels, "data": data}
