from .dummy_data_generator2 import data_csv2
import json


class Individual:

    def __init__(self, income, location, categoryArray) :
        self.income = income
        self.location = location
        self.categoryArray = categoryArray


def parseCSV2(income, zipcode, data, incomeRange, isZipCodeOptional):
   individuals = []
   for index, row in data.iterrows():
       if(isZipCodeOptional) :
        zipcode = row['zipcodes']

       if (income * (1 - incomeRange) < row['income']) and (row['income'] < income * (1 + incomeRange)) and (zipcode == row['zipcodes']):
           category_array = {}
           for categoryName in row.keys() :
               category_array[categoryName] = row[categoryName]

           del category_array["income"]
           del category_array["zipcodes"]
           individual = Individual(row['income'], row['zipcodes'], category_array)
           individuals.append(individual)
   json_string = json.dumps([ind.__dict__ for ind in individuals])
   return json_string
