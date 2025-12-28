# controllers/budget_controller.py

from utils.storage import save_envelopes, load_envelopes
from models.envelopes import Envelope, apply_recurrence

class BudgetController:
    def __init__(self):
        self.envelopes = load_envelopes()
        self.cash_on_hand = 0  # your account / wallet money

    def set_cash_on_hand(self, amount):
        self.cash_on_hand = float(amount)

    def add_envelope(self, name, category, budget, emoji, recurrence):
        self.envelopes.append(
            Envelope(
                name=name,
                category=category,
                budget=float(budget),
                emoji=emoji,
                recurrence=recurrence
            )
        )
        save_envelopes(self.envelopes)

    def delete_envelope(self, name):
        self.envelopes = [e for e in self.envelopes if e.name != name]
        save_envelopes(self.envelopes)

    def spend(self, name, amount):
        """Take money from envelope."""
        for e in self.envelopes:
            if e.name == name:
                e.balance -= float(amount)   # reduce current cash
                e.spent += float(amount)     # record spending
                break
        save_envelopes(self.envelopes)

    def add_cash(self, name, amount):
        """Stuff money from cash_on_hand into envelope."""
        amount = float(amount)
        if amount > self.cash_on_hand:
            raise ValueError("Not enough cash to stuff envelope!")
        for e in self.envelopes:
            if e.name == name:
                e.balance += amount
                break
        self.cash_on_hand -= amount  # subtract from cash_on_hand
        save_envelopes(self.envelopes)

    def reset_all(self):
        apply_recurrence(self.envelopes)
        save_envelopes(self.envelopes)
