"""
Data structure to hold flowchart and cards.
"""

import sqlite3
import random
import requests
import json
from integration.model import ML_FOOD, ML_ESSENTIALS, ML_IEE, ML_NONESSENTIALS


conn = sqlite3.connect('database.db')
db = conn.cursor()


NESSIE_API_KEY = "key=96e574f60ee2fbf40489f05aab148328" # Abhishek's
NESSIE_ROOT_URL = "http://api.reimaginebanking.com"


default_cards = [{'name': 'Rent', 'description': 'Rent, mortgage and renter/homeowner insurance.',
                   'category': 'expenses'},
                 {'name': 'Food', 'description': 'Food and groceries.',
                   'category': 'expenses'},
                 {'name': 'Essentials', 'description': 'Utilities such as power, water, heat and toiletries.',
                    'category': 'expenses'},
                 {'name': 'Income-Earning Expenses', 'description': 'Expenses necessary to maintain an income, e.g. transportation and possibly phone/Internet bills.',
                    'category': 'expenses'},
                 {'name': 'Healthcare', 'description': 'Healthcare and health insurance.',
                    'category': 'expenses'},

                 {'name': 'Loan Minimum Payments', 'description': 'Minimum monthly payments on all debts and loans.',
                    'category': 'debts'},
                 {'name': 'Minimum Emergency Fund', 'description': '$1000 or one month\'s expenses, whichever is greater.',
                    'category': 'emergency'},
                 {'name': 'Non-Essential Bills', 'description': 'Cable, Internet and phone bills.',
                    'category': 'expenses'},
                 {'name': 'Employer Retirement Account', 'description': 'If employer offers a retirement account with an employer match, pay the amount needed to get the full employer match (but nothing more than that).',
                    'category': 'retirement'},

                 {'name': 'High-Interest Debts', 'description': 'For debts with high interest (>10%), pay back in full using either the Avalanche or Snowball method.',
                    'category': 'debts'},
                 {'name': 'Full Emergency Fund', 'description': 'Increase emergency fund to 6 months\' worth of living expenses.',
                    'category': 'emergency'},
                 {'name': 'Moderate-Interest Debts', 'description': 'For debts with moderate interest (>4%), pay back in full using either the Avalanche or Snowball method.',
                    'category': 'debts'},

                 {'name': 'IRA', 'description': 'Max out the yearly contributions to a traditional or Roth IRA, whichever is more suitable.',
                    'category': 'retirement'},
                 {'name': 'Large Future Expenses', 'description': 'College tuition, professional certifications, owning a car etc.',
                    'category': 'expenses'},
                 {'name': 'Retirement Fund', 'description': 'Save 15\% of pre-tax income or contribute 15\% of pre-tax income to an employer 401(k) or 403(b), or contribute to an individual 401(k).',
                    'category': 'retirement'},
                 {'name': 'Investable HSA', 'description': 'If you have a qualified health deductible health plan and thus are eligible for an investable HSA, then max your yearly HSA contributions.',
                    'category': 'retirement'},
                 {'name': 'Early Retirement', 'description': 'If you want to retire early, max out your 401(k) or any employer sponsored retirement accounts.',
                    'category': 'retirement'},
                 {'name': 'Other Expenses', 'description': 'Save for other goals such as down payment for homes, saving for vehicles or vacation funds.',
                    'category': 'expenses'}]


class Card:
    """ Object to contain card. """

    is_fulfilled = False

    def __init__(self, card_dict):
        """ Instantiates a card. """
        for key, value in card_dict.items():
            setattr(self, key, value)

    def compute_value(self, current):
        """ Given budgeted amount and remaining salary, compute the value of card fulfilled. """
        if current == 0:
            self.value = 0
            return 0
        if self.budgetted <= current:
            self.value = self.budgetted
            self.is_fulfilled = True
            return (current - self.budgetted)
        else:
            self.value = self.current
            self.is_fulfilled = True
            return 0


class EmergencyCard(Card):
    """ Specialized card for emergency funds. """

    def __init__(self, card_dict):
        Card.__init__(self, card_dict)

    def compute_value(self, current, savings):
        if savings >= self.budgetted:
            self.is_fulfilled = True
            return current, savings
        if current == 0:
            self.value = 0
            return 0, savings
        if (self.budgetted - savings) <= current:
            self.value = self.budgetted - savings
            self.is_fulfilled = True
            return (current - (self.budgetted - savings)), self.budgetted
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

        if self.budgetted == 'minimums':
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
        elif self.budgetted == 'hi_loans':
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
        elif self.budgetted == 'mod_loans':
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

    def __init__(self, nessie_id, salary, zipcode, is_first_time):
        """ Instantiate a flowchart for a new user. """
        self.nessie_id = nessie_id
        self.salary = salary
        self.zipcode = zipcode

        # TODO: Ask user to answer these questions
        monthly_rent = 800
        monthly_healthcare = 300
        monthly_era = 200
        monthly_hsa = 100

        # Get pre-populated/database budgetted numbers for each card.
        if is_first_time:
            self.budgetted = (monthly_rent, ML_FOOD, ML_ESSENTIALS, ML_IEE, monthly_healthcare, 'minimums',
                                max(1000, monthly_rent + ML_FOOD + ML_ESSENTIALS + ML_IEE + monthly_healthcare),
                                ML_NONESSENTIALS, monthly_era, 'hi_loans', 3 * (monthly_rent + ML_FOOD + ML_ESSENTIALS + ML_IEE + monthly_healthcare),
                                'mod_loans', 0, 0, 0, monthly_hsa, 0, 0)
        else:
            self.budgetted = db.execute("SELECT * FROM users WHERE nessieID = '%s'" % self.nessie_id).fetchall()[0][3:]

        self.current = self.salary
        self.chart = []
        self.get_nessie_data()

    def get_nessie_data(self):
        """ Get loan and balance data from Nessie. """
        self.loans = [{'loan_remaining_amount': 20, 'minimum_payment': 10, 'ir': random.uniform(0, 0.12)}]

        # Get accounts associated with customer. Also gets loan associated with each account.
        rc = requests.get(NESSIE_ROOT_URL + f"/customers/{self.nessie_id}/accounts?" + NESSIE_API_KEY)
        self.original_checkings = 0
        self.original_savings = 0
        for acc in rc.json():
            if acc['type'] == 'Checking':
                self.original_checkings += acc['balance']
            if acc['type'] == 'Savings':
                self.original_savings += acc['balance']
            rl = requests.get(NESSIE_ROOT_URL + f"/accounts/{acc['_id']}/loans?" + NESSIE_API_KEY)
            for loan in rl.json():
                self.loans.append({'loan_remaining_amount': loan['amount'], 'minimum_payment': loan['monthly_payment'], 'ir': random.uniform(0, 0.12)})
        self.checkings = self.original_checkings
        self.savings = self.original_savings

    def load(self, card_details, default_value):
        """ Load a card into the flowchart. """
        if card_details['category'] == 'emergency':
            card = EmergencyCard(card_details)
            card.budgetted = default_value
            self.current, self.savings = card.compute_value(self.current, self.savings)
            card.remaining = self.current
            card.bvalue = card.budgetted
        elif card_details['category'] == 'debts':
            card = LoanCard(card_details)
            card.bvalue = sum([loan['loan_remaining_amount'] for loan in self.loans])
            card.budgetted = default_value
            self.current, self.loans = card.compute_value(self.current, self.loans)
            card.remaining = self.current
        else:
            card = Card(card_details)
            card.budgetted = default_value
            self.current = card.compute_value(self.current)
            card.remaining = self.current
            card.bvalue = card.budgetted
        self.chart.append(card)

    def load_default(self):
        """ Loads the default sequence of cards. """
        for i in range(len(default_cards)):
            self.load(default_cards[i], self.budgetted[i])
        self.checkings += self.current

    def front_end_json(self):
        """ Pass card data to front end as JSON: [{cardObject}, {cardObject}, ...]
            where {cardObject} contains 5 keys: name, description, category, budgetted, remaining
        """
        return json.dumps([{'name': card.name, 'description': card.description,
            'category': card.category, 'budgetted': card.bvalue,
            'remaining': card.remaining} for card in self.chart])

    def google_bot_json(self):
        """ Return card data to Google Bot as JSON: [{cardObject}, {cardObject}, ...]
        where {cardObject} contains 5 keys: name, description, category, budgetted, remaining
        """

    def upsert_database(self):
        """ Pass updated budgetted values to database. """
        tup = tuple([card.budgetted for card in self.chart] + [self.nessie_id])
        update_query = """
            UPDATE
                users
            SET
                f1 = %f,
                f2 = %f,
                f3 = %f,
                f4 = %f,
                f5 = %f,
                f6 = '%s',
                f7 = %f,
                f8 = %f,
                f9 = %f,
                f10 = '%s',
                f11 = %f,
                f12 = '%s',
                f13 = %f,
                f14 = %f,
                f15 = %f,
                f16 = %f,
                f17 = %f,
                f18 = %f
            WHERE
                nessieID = '%s'
        """ % tup
        db.execute(update_query)
        conn.commit()


if __name__ == '__main__':
    fc = FlowChart("5b72dc8f322fa06b67793bb8", 10000, '02138', True)
    fc.load_default()
    fc.upsert_database()
