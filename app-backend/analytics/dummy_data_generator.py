import random
import numpy
import pandas

num_of_users = 10000
num_of_budget_params = 10
total_income = 0
total_food = 0
total_essentials = 0
total_iee = 0

zipcodes = ['94016', '44101', '60007', '10024', '22031']


def generate_data():
    global total_income
    global total_food
    global total_essentials
    global total_iee

    random_city_num = random.randint(0, 4)

    random_income = random.randint(1000, 12500)
    total_income += random_income

    random_list = random.sample(range(100000), num_of_budget_params)
    divided_list = [x / sum(random_list) for x in random_list]

    food_spend = random_income * divided_list[0]
    total_food += food_spend

    essentials_spend = random_income * divided_list[1]
    total_essentials += essentials_spend

    ieee_spend = random_income * divided_list[2]
    total_iee += ieee_spend

    return {'zipcodes': zipcodes[random_city_num], 'income': random_income,
            'food': int(random_income * divided_list[0]),
            'healthcare': int(random_income * divided_list[1]),
            'transportation': int(random_income * divided_list[2]),
            'rent': int(random_income * divided_list[3]),
            'entertainment': int(random_income * divided_list[4]),
            'gifts': int(random_income * divided_list[5]),
            'personal care': int(random_income * divided_list[6])
            }


def data_csv():
    dummy_data = ([generate_data() for i in range(num_of_users)])
    dummy_data = pandas.DataFrame(dummy_data, columns=['zipcodes', 'income',
    'food', 'healthcare', 'transportation', 'rent', 'entertainment', 'gifts', 'personal care'])
    # dummy_data = pandas.DataFrame.to_csv(dummy_data)
    return dummy_data


'''
print('Overall Averages:')
print('Income:', int(total_income / num_of_users))
print('Food Spending:', int(total_food / num_of_users))
print('Essentials Spending:', int(total_essentials / num_of_users))
print('IEE Spending:', int(total_iee / num_of_users))
'''
