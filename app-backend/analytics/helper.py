from .dummy_data_generator import data_csv
import json


class Individual:

    def __init__(self, income, location, categoryArray) :
        self.income = income
        self.location = location
        self.categoryArray = categoryArray


def parseCSV(income, zipcode, data):
   individuals = []
   for index, row in data.iterrows():
       if (income * 0.75 < row['income']) and (row['income'] < income * 1.25) and (zipcode == row['zipcodes']):
           category_array = {'food': row['food'], 'essentials': row['essentials'], 'IEE': row['IEE']}
           individual = Individual(row['income'], row['zipcodes'], category_array)
           individuals.append(individual)
   json_string = json.dumps([ind.__dict__ for ind in individuals])
   return json_string
