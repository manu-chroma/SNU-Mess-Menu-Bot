from bs4 import BeautifulSoup
import requests
from dateutil.parser import *
from collections import defaultdict

def parser():
    # fetch url source
    URL = "http://messmenu.snu.in/messMenu.php"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    r = requests.get(URL, headers=headers)

    # create soup from source
    soup = BeautifulSoup(r.content, "lxml")

    # this will contain the complete mess menu
    response_dict = defaultdict(dict)

    """ 
    there are 2 tables present in the source
    table[0] -> dh1 and table[1] -> dh2
    each table contains date, breakfeast, lunch, dinner in <p> tags
    """
    tables = soup.find_all('table')
    mess_name = ['DH1','DH2']

    for idx, mess in enumerate(tables):
        response = mess.find_all("label")[0].text.strip()

        if "No Menu Available." in response:
            response_dict[mess_name[idx]]['respon1se'] = False
            response_dict[mess_name[idx]]['date'] = '' 
        else:
            # parse the date present in the source
            response_dict[mess_name[idx]]['response'] = True
            response_dict[mess_name[idx]]['date'] =  parse(response).date()

            # parse all the meals of the day
            td_elements = mess.find_all("td")

            meals_of_the_day = ['Breakfast', 'Lunch', 'Dinner']

            for meal_name_idx, meal_name in enumerate(meals_of_the_day):
                response_dict[mess_name[idx]][meal_name] = []

                for meal in (td_elements[meal_name_idx+1].find_all('p')):
                    response_dict[mess_name[idx]][meal_name].append(meal.text.replace('"', '').strip().capitalize())                

    return response_dict

if __name__ == "__main__":
    import pprint
    pprint.pprint(parser())
