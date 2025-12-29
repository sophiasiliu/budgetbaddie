# models/envelopes.py

class Envelope:
    def __init__(self, name, category, budget, emoji, recurrence, spent=0, balance=0):
        self.name = name
        self.category = category
        self.budget = budget      # goal amount
        self.emoji = emoji
        self.recurrence = recurrence
        self.spent = spent
        self.balance = balance    # current cash in envelope

    def progress(self):
        # Use spent vs budget to show usage percentage
        if self.budget == 0:
            return 0
        return min(self.balance / self.budget, 1)
    
def apply_recurrence(envelopes: list[Envelope]):
    for env in envelopes:
        if env.recurrence == "monthly":
            if env.category == "fixed":
                env.balance = 0  # refill budget
            elif env.category == "variable":
                if env.balance == env.category: #if all money was spent, else carry over to next month
                    env.balance = 0
        elif env.recurrence == "none":
            pass  # lifetime, do nothing

def apply_clear(envelopes: list[Envelope]):
    for env in envelopes:
        env.balance = 0
        env.spent = 0
    
