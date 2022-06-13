import time
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
import file_helper

###Session.get####
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def get_next_url(soup):
    if soup:
        buttons = soup.find(class_='pagination__inner')
        if buttons:
            next_url = buttons.findAll(class_='pagination__button button--flat button--small')[1]['href']
            return next_url


def get_soup(url):
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, "lxml")
    if response.status_code != 200:
        return None
    return soup


def get_next_soup(soup):
    if soup:
        buttons = soup.find(class_='pagination__inner')
        if buttons:
            next_url = buttons.findAll(class_='pagination__button button--flat button--small')[1]['href']
            response = requests.get(next_url, headers=header)
            if response.status_code != 200:
                return None
            soup = BeautifulSoup(response.text, "lxml")
            return soup


def get_last_page_numer(soup):
    if soup:
        buttons = soup.find(class_='pagination__inner')
        if buttons:
            last_page_number = buttons.findAll(class_='pagination__page-number')[-1].text.split(' ')[3]
            return last_page_number


def get_details(soup):
    details = []
    if soup:
        parameters = soup.findAll(class_='listing__link js-listing-active-area')
        for parameter in parameters:
            ad_details = [""] * 4
            if parameter.find(class_='listing__featured-parameters').find(class_='listing__address'):
                ad_details[0] = unidecode(
                    parameter.find(class_='listing__featured-parameters').find(class_='listing__address').text)
            else:
                ad_details[0] = 'None'

            if parameter.find(class_='listing__featured-parameters').find(class_='price'):
                ad_details[1] = str(int(float(parameter.find(class_='listing__featured-parameters').find(
                    class_='price').text.strip().split(' ')[0]) * 1000000))
            else:
                ad_details[1] = '0'

            if parameter.find(class_='listing__parameters').find(class_='listing__parameter listing__data--room-count'):
                ad_details[2] = ''.join(c for c in parameter.find(class_='listing__parameters').find(
                    class_='listing__parameter listing__data--room-count').text if c.isdigit() or c == '+')
            else:
                ad_details[2] = '0'

            if parameter.find(class_='listing__parameters').find(class_='listing__parameter listing__data--area-size'):
                ad_details[3] = unidecode(parameter.find(class_='listing__parameters').find(
                    class_='listing__parameter listing__data--area-size').text).split()[0]
            else:
                ad_details[3] = '0'
            details.append(ad_details)
    return details


# If you want to run this script in parallel, you can use these functions
def get_and_write_flats():
    file_helper.initialize_json("ingatlan_com_flats")
    url = "https://ingatlan.com/szukites/elado+lakas?page=2"
    soup = get_soup(url)
    if not soup:
        print('Could not get soup')
        return None
    last_page = get_last_page_numer(soup)
    details = get_details(soup)
    file_helper.write_details(details, "ingatlan_com_flats")
    for _ in range(int(last_page) - 5):
        soup = get_next_soup(soup)
        if not soup:
            continue
        details += get_details(soup)
    file_helper.write_details(details, "ingatlan_com_flats")


def get_and_write_houses():
    file_helper.initialize_json("ingatlan_com_houses")
    url = "https://ingatlan.com/lista/elado+haz?page=2"
    soup = get_soup(url)
    if not soup:
        print('Could not get soup')
        return None
    last_page = get_last_page_numer(soup)
    details = get_details(soup)
    file_helper.write_details(details, "ingatlan_com_houses")
    for _ in range(int(last_page) - 5):
        soup = get_next_soup(soup)
        if not soup:
            continue
        details += get_details(soup)
    file_helper.write_details(details, "ingatlan_com_houses")


if __name__ == '__main__':
    get_and_write_flats()
    get_and_write_houses()
