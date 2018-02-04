#converter.py
import yo as parser
import re
from fractions import Fraction

def get_conversion_dict(url):
    try:
        obj = _call_create_object(url)
        obj.get_ingredients()
        obj_dict = obj.ingredients_dict
        return obj_dict
    except(parser.WrongURLException):
        raise AttributeError

def get_conversion(url, adjusted_serving):
    obj = _call_create_object(url)
    obj_dict = get_conversion_dict(url)
    obj.get_servings()
    serving = obj.servings
    k = (calculate(obj_dict, serving, int(adjusted_serving)))
    return to_str(k)

def to_str(k):
    final_str = ""
    for item in k:
        if k[item] != '0':
            final_str += str(k[item])+ " " +item+'\n'
        else:
            final_str += item+'\n'
    return final_str
    

def calculate(obj_dict, serving, adjusted_serving):
    ratio_frac = Fraction(adjusted_serving,serving)
    for i in obj_dict:
        num_list = obj_dict[i].split()
        num = 0
        for j in num_list:
            serving_Frac = 0
            if '/' in j:
                split_f = j.split('/')
                num += Fraction(int(split_f[0]),int(split_f[1]))
            else:
                num +=  Fraction(int(j),1)
        new_value = (num * ratio_frac).limit_denominator(16)
        if new_value.numerator > new_value.denominator and new_value.denominator != 1:
            whole = str(new_value.numerator//new_value.denominator)
            frac = str(new_value.numerator % new_value.denominator) + '/' + str(new_value.denominator)
            new_value = whole + ' ' + frac
        else:
            new_value = str(new_value)
        obj_dict[i] = new_value
    return obj_dict



def _call_create_object(url):
    key = {
        'bettycrocker':parser.BettyCrocker(url),
        'geniuskitchen':parser.GeniusKitchen(url),
        'foodnetwork':parser.FoodNetwork(url),
        'marthastewart':parser.MarthaStewart(url)
        }
    for i in key:
        if i in url:
            return key[i]

if __name__ == '__main__':
    #url = 'http://www.geniuskitchen.com/recipe/oven-barbecued-chicken-wings-20960'
    #url = 'https://www.bettycrocker.com/recipes/italian-sausage-lasagna/2601a67c-438d-407a-b163-2f57ede06cb9'
    url = 'http://www.foodnetwork.com/recipes/food-network-kitchen/chocolate-chip-cookies-recipe4-2011856'
    #url = 'http://www.foodnetwork.com/recipes/ree-drummond/the-cheesiest-quesadillas-3690636'
    get_conversion(url, 15)
