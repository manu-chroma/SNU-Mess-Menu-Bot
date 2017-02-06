from bs4 import BeautifulSoup
import requests
from dateutil.parser import *
from collections import defaultdict

def parser():
    # fetch url http://messmenu.snu.in/messMenu.php source
    URL = "http://messmenu.snu.in/messMenu.php"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    r = requests.get(URL, headers=headers)

    # create soup from source
    soup = BeautifulSoup(r.content, "lxml")

    response_dict = defaultdict(dict)

    """
    there are 2 tables present in the source
    table[0] -> dh1 and table[1] -> dh2
    """
    tables = soup.find_all('table')

    for idx, mess in enumerate(tables):
        response = mess.find_all("label")[0].text.strip()


        if "No Menu Available." in response:
            response_dict[idx]['response'] = 'False'
        else:
            # parse the date present in the source
            response_dict[idx]['response'] = 'True'
            response_dict[idx]['date'] =  parse(response).date()

            # parse all the meals of the day
            td_elements = mess.find_all("td")

            response_dict[idx]['breakfast'] = []
            for meal in (td_elements[1].find_all('p')):
                response_dict[idx]['breakfast'].append(meal.text.strip())

            response_dict[idx]["lunch"] = []
            for meal in (td_elements[2].find_all('p')):
                response_dict[idx]['lunch'].append(meal.text.strip())

            response_dict[idx]['dinner'] = []
            for meal in (td_elements[3].find_all('p')):
                response_dict[idx]['dinner'].append(meal.text.strip())

    return response_dict

if __name__ == "__main__":
    print(parser())
