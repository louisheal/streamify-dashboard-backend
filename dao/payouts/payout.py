class Payout:
    def __init__(self, amount: float):
        self.amount = amount

    def to_json(self):
        return {
            "amount": self.amount
        }

    @classmethod
    def from_json(cls, data):
        return cls(data["amount"])
