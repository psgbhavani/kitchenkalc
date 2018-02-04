#parse.py
import urllib.request
from bs4 import BeautifulSoup
import re

class WrongURLException(Exception):
    pass

class FoodNetwork:
    def __init__(self, url):
        self.url = url
        self.ingredients_dict = {}

    def get_ingredients(self):
        parsed = self._get_html()
        ingredients = parsed.find_all('label',attrs={'class':'o-Ingredients__a-ListItemText'})
        i_list = []
        for i in ingredients:
            i_list.append(i.text.strip())
        self._add_to_dictionary(i_list)

    def get_servings(self):
        parsed = self._get_html()
        serving_desc = parsed.find('section', attrs={'class':'o-RecipeInfo o-Yield'}).find('dd', attrs={'class':'o-RecipeInfo__a-Description'}).text.split(' ')
        for i in serving_desc:
            try:
                int(i)
            except ValueError:
                pass
            else:
                self.servings = int(i)
                break


    def _get_html(self):
        try:
            page = urllib.request.urlopen(self.url)
        except(urllib.error.HTTPError):
            raise WrongURLException
        parsed = BeautifulSoup(page, 'html.parser')
        return parsed

    def _add_to_dictionary(self, i_list:list):
        paren_pat = re.compile(r'\((.*)\)')
        qty_pat = re.compile(r'[0-9](( )|/|[0-9])*')
        for i in i_list:
            no_paren = re.sub(paren_pat, '', i)
            first_l = no_paren[0]
            try:
                eval(first_l)
            except:
                get_qty = '0'
            else:
                get_qty = re.match(qty_pat, no_paren).group()
            ingredient = re.sub(qty_pat, '', no_paren)

            self.ingredients_dict[ingredient.rstrip()] = get_qty

class GeniusKitchen:
    def __init__(self, url):
        self.url = url
        self.ingredients_dict = {}
        self.servings = 0

    def _get_html(self):
        try:
            page = urllib.request.urlopen(self.url)
        except(urllib.error.HTTPError):
            raise WrongURLException
        parse = BeautifulSoup(page, 'html.parser')
        return parse

    def get_ingredients(self):
        parse = self._get_html()
        parse_list = parse.findAll('span', attrs={'class':'food'})
        quantity_list = parse.findAll('span', attrs={'class':'qty'})
        for i,s in zip(parse_list, quantity_list):
            quant = ''
            if ' ' in s.text.strip():
                quant = s.text.strip().split()[0]+' '
            if s.find('sup') != None:
                quant += (s.find('sup').text.strip() + '/' + s.find('sub').text.strip())
            else:
                quant = s.text.strip()
            self.ingredients_dict[str(i.text.strip())] = str(quant)
    
    def get_servings(self):
        parse = self._get_html()
        try:
            self.servings = str(parse.find('td', attrs={'class':'servings'}).find('span', attrs={'class':'count'}).text.strip())
        except AttributeError:
            self.servings = str(parse.find('td', attrs={'class':'yield'}).find('span', attrs={'class':'count'}).text.strip())
        if '-' in self.servings:
           servings_list = self.servings.split('-')
           self.servings = int(servings_list[0])
        else:
            self.servings = int(self.servings)


class BettyCrocker:
    def __init__(self, url):
        self.url = url
        self.servings = 0
        self.ingredients_dict = {}

    def _get_html(self):
        try:
            page = urllib.request.urlopen(self.url)
        except(urllib.error.HTTPError):
            raise WrongURLException
        soup = BeautifulSoup(page, 'html.parser')
        return soup

    def get_ingredients(self):
        soup = self._get_html()
        count =0
        previous_item =""
        name_box = soup.find("div", attrs = {'class':'recipePartIngredients'})
        p =[ item.strip() for item in name_box.text.replace("  ","").replace("\n\n","").split('\n') if len(item) != 0 and len(item.strip()) != 0]
        for item in p[1:]:
            if item != '\r':
                if count%2 == 0:
                    previous_item = item
                else:
                    self.ingredients_dict[item] = previous_item
                count+=1
        
                
    def get_servings(self):
        soup = self._get_html()
        new_name_box = soup.find("li", attrs = {"id":"gmi_rp_primaryAttributes_servings"})
        self.servings = int(new_name_box.text.split('\n')[2])


class MarthaStewart:
    def __init__(self, url):
        self.url = url
        self.servings = 0
        self.ingredients_dict = {}

    def _get_html(self):
        page = urllib.request.urlopen(self.url)
        soup = BeautifulSoup(page, 'html.parser')
        return soup

    def get_ingredients(self):
        soup = self._get_html()
        count =0
        previous_item =""
        name_box = soup.find("ul", attrs = {'class':'components-list'})
        p =[ item.strip() for item in name_box.text.replace("  ","").replace("\n\n","").split('\n') if len(item) != 0 and len(item.strip()) != 0]
        self._add_to_dictionary(p)

    def _add_to_dictionary(self, i_list:list):
        paren_pat = re.compile(r'\((.*)\)')
        qty_pat = re.compile(r'[0-9](( )|/|[0-9])*')
        is_num = re.compile(r'\d*')

        print(i_list)
        for i in i_list:
            no_paren = re.sub(paren_pat, '', i)
            first_l = no_paren[0]
            try:
                get_qty = re.search(qty_pat, no_paren)
                print(get_qty)
                qty_index = get_qty.end()
                print(qty_index)
                get_qty = get_qty.group()
                ingredient = no_paren[qty_index:]
                self.ingredients_dict[ingredient.rstrip()] = get_qty

            except(AttributeError):
                ingredient = no_paren
                self.ingredients_dict[ingredient.rstrip()] = ""

        print(self.ingredients_dict)
                

           
       
        
                
    def get_servings(self):
        soup = self._get_html()
        new_name_box = soup.find("div", attrs = {"class":"instruction-time-data"})
        my_str = new_name_box.text
        list_str = [item.strip() for item in my_str.split('\n') if len(item) != 0]
        print(list_str[-1])
        is_num = re.compile(r'\d+')
        get_qty = re.search(is_num, list_str[-1])
        qty_index_start = get_qty.start()
        qty_index_end = get_qty.end()
        print(qty_index_start)
        
        
        try:
            print(my_str[qty_index_start:])
            self.servings = int(list_str[-1][qty_index_start: qty_index_end].strip())
        except(ValueError):
            self.servings = 1
        print(self.servings)
