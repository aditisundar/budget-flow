"""
Data structure to hold flowchart and cards.
"""

from types import *


USER_RENT = 10
USER_HEALTHCARE = 10
USER_ERA = 10
USER_HSA = 10

ML_FOOD = 10
ML_ESSENTIALS = 10
ML_IEE = 10
ML_NONESSENTIALS = ML_ESSENTIALS



default_cards = [{'name': 'Rent', 'description': 'Rent, mortgage and renter/homeowner insurance.',
                   'category': 'expenses', 'compute': USER_RENT},
                 {'name': 'Food', 'description': 'Food and groceries.',
                   'category': 'expenses', 'compute': ML_FOOD},
                 {'name': 'Essentials', 'description': 'Utilities such as power, water, heat and toiletries.',
                    'category': 'expenses', 'compute': ML_ESSENTIALS},
                 {'name': 'Income-Earning Expenses', 'description': 'Expenses necessary to maintain an income, e.g. transportation and possibly phone/Internet bills.',
                    'category': 'expenses', 'compute': ML_IEE},
                 {'name': 'Healthcare', 'description': 'Healthcare and health insurance.',
                    'category': 'expenses', 'compute': USER_HEALTHCARE},

                 {'name': 'Loan Minimum Payments', 'description': 'Minimum monthly payments on all debts and loans.',
                    'category': 'debts', 'compute': 'minimums'},
                 {'name': 'Minimum Emergency Fund', 'description': '$1000 or one month\'s expenses, whichever is greater.',
                    'category': 'emergency', 'compute': max(1000, USER_RENT + ML_FOOD + ML_ESSENTIALS + ML_IEE + USER_HEALTHCARE)},
                 {'name': 'Non-Essential Bills', 'description': 'Cable, Internet and phone bills.',
                    'category': 'expenses', 'compute': ML_NONESSENTIALS},
                 {'name': 'Employer Retirement Account', 'description': 'If employer offers a retirement account with an employer match, pay the amount needed to get the full employer match (but nothing more than that).',
                    'category': 'retirement', 'compute': USER_ERA},

                 {'name': 'High-Interest Debts', 'description': 'For debts with high interest (>10%), pay back in full using either the Avalanche or Snowball method.',
                    'category': 'debts', 'compute': 'hi_loans'},
                 {'name': 'Full Emergency Fund', 'description': 'Increase emergency fund to 6 months\' worth of living expenses.',
                    'category': 'emergency', 'compute': 6 * (USER_RENT + ML_FOOD + ML_ESSENTIALS + ML_IEE + USER_HEALTHCARE)},
                 {'name': 'Moderate-Interest Debts', 'description': 'For debts with moderate interest (>4%), pay back in full using either the Avalanche or Snowball method.',
                    'category': 'debts', 'compute': 'mod_loans'},

                 {'name': 'IRA', 'description': 'Max out the yearly contributions to a traditional or Roth IRA, whichever is more suitable.',
                    'category': 'retirement', 'compute': 0},
                 {'name': 'Large Future Expenses', 'description': 'College tuition, professional certifications, owning a car etc.',
                    'category': 'expenses', 'compute': 0},
                 {'name': 'Retirement Fund', 'description': 'Save 15\% of pre-tax income or contribute 15\% of pre-tax income to an employer 401(k) or 403(b), or contribute to an individual 401(k).',
                    'category': 'retirement', 'compute': 0},
                 {'name': 'Investable HSA', 'description': 'If you have a qualified health deductible health plan and thus are eligible for an investable HSA, then max your yearly HSA contributions.',
                    'category': 'retirement', 'compute': USER_HSA},
                 {'name': 'Early Retirement', 'description': 'If you want to retire early, max out your 401(k) or any employer sponsored retirement accounts.',
                    'category': 'retirement', 'compute': 0},
                 {'name': 'Other Expenses', 'description': 'Save for other goals such as down payment for homes, saving for vehicles or vacation funds.',
                    'category': 'expenses', 'compute': 0}]


class Card:
    """ Object to contain card. """

    is_fulfilled = False

    def __init__(self, card_dict):
        """ Instantiates a card. """
        for key, value in card_dict.items():
            setattr(self, key, value)

    def compute_value(self, current):
        """ Given budgeted amount and remaining salary, compute the value of card fulfilled."""
        if current == 0:
            self.value = 0
            return 0
        if self.compute <= current:
            self.value = self.compute
            self.is_fulfilled = True
            return (current - self.compute)
        else:
            self.value = self.current
            self.is_fulfilled = True
            return 0


class EmergencyCard(Card):
    """ Specialized card for emergency funds. """

    def __init__(self, card_dict):
        Card.__init__(self, card_dict)

    def compute_value(self, current, savings):
        if savings >= self.compute:
            self.is_fulfilled = True
            return current, savings
        if current == 0:
            self.value = 0
            return 0, savings
        if (self.compute - savings) <= current:
            self.value = self.compute - savings
            self.is_fulfilled = True
            return (current - (self.compute - savings)), self.compute
        else:
            self.value = current
            self.is_fulfilled = True
            return 0, savings + current


class LoanCard(Card):
    """ Specialized card for loans. """

    def __init__(self, card_dict):
        Card.__init__(self, card_dict)

    def compute_value(self, current, loans):
        if sum([loan['loan_remaining_amount'] for loan in loans]) == 0:
            self.is_fulfilled = True
            return current, loans
        if current == 0:
            self.value = 0
            return 0, loans

        if self.compute == 'minimums':
            sorted_loans = sorted(loans, key=lambda x: x['minimum_payment'])
            self.is_fulfilled = True
            for i in range(len(sorted_loans)):
                if current >= sorted_loans[i]['minimum_payment']:
                    current -= sorted_loans[i]['minimum_payment']
                    sorted_loans[i]['loan_remaining_amount'] -= sorted_loans[i]['minimum_payment']
                else:
                    sorted_loans[i]['loan_remaining_amount'] -= current
                    current = 0
                    break
            return current, sorted_loans
        elif self.compute == 'hi_loans':
            valid, invalid = sorted(list(filter(lambda x: x['ir'] >= 0.1, loans)), key=lambda y: y['ir']), list(filter(lambda x: x['ir'] < 0.1, loans))
            self.is_fulfilled = True
            for i in range(len(valid)):
                if current >= valid[i]['loan_remaining_amount']:
                    current -= valid[i]['loan_remaining_amount']
                    valid[i]['loan_remaining_amount'] = 0
                else:
                    valid[i]['loan_remaining_amount'] -= current
                    current = 0
                    break
            return current, valid + invalid
        elif self.compute == 'mod_loans':
            valid, invalid = sorted(list(filter(lambda x: 0.04 <= x['ir'] < 0.1, loans)), key=lambda y: y['ir']), list(filter(lambda x: x['ir'] < 0.04 or x['ir'] >= 0.1, loans))
            self.is_fulfilled = True
            for i in range(len(valid)):
                if current >= valid[i]['loan_remaining_amount']:
                    current -= valid[i]['loan_remaining_amount']
                    valid[i]['loan_remaining_amount'] = 0
                else:
                    valid[i]['loan_remaining_amount'] -= current
                    current = 0
                    break
            return current, valid + invalid




class FlowChart:
    """ Budgeting flowchart for a user. """

    def __init__(self, user_id):
        """ Instantiate a flowchart for a new user. """
        self.id = user_id
        self.salary = 10000
        self.current = self.salary
        self.chart = []

        self.original_checkings = 1000
        self.original_savings = 100
        self.checkings = self.original_checkings
        self.savings = self.original_savings

        self.loans = [{'loan_remaining_amount': 20, 'minimum_payment': 10, 'ir': 0.03}]


    def load(self, card_details):
        """ Load a card into the flowchart. """
        if card_details['category'] == 'emergency':
            card = EmergencyCard(card_details)
            self.current, self.savings = card.compute_value(self.current, self.savings)
        elif card_details['category'] == 'debts':
            card = LoanCard(card_details)
            self.current, self.loans = card.compute_value(self.current, self.loans)
        else:
            card = Card(card_details)
            self.current = card.compute_value(self.current)
        self.chart.append(card)

    def load_default(self):
        """ Loads the default sequence of cards. """
        for card in default_cards:
            self.load(card)
        self.saved = self.current
        self.checkings += self.saved


if __name__ == '__main__':
    fc = FlowChart("dummyId123")
