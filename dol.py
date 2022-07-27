import requests
from bs4 import BeautifulSoup

URL = "https://www.dol.gov/newsroom/releases/ilab"
base_url = "https://www.dol.gov"

years = ["2022"]
finish = True
all_sub_url = []

for year in years:
    #collect outer date and link
    while finish:
        r = requests.get(URL) #get url
        soup = BeautifulSoup(r.content, 'html.parser')
        main_div = soup.find_all('div', 'dol-feed-block')
        for div in main_div: #main div
            main_div_date = div.find('p', 'dol-date-text').getText()
            print(main_div_date)
            current_year = main_div_date.split(" ")[-1]
            if current_year not in years and current_year != year: #check year in list
                print("All years finish")
                finish = False
            if year in main_div_date:
                sub_url = base_url + div.find('a')['href'].strip()
                all_sub_url.append(sub_url)
                print(sub_url)
        #collect outer_html from sub linkes
        for link in all_sub_url:
            print(link)
            sub_r = requests.get(link)
            sub_soup = BeautifulSoup(sub_r.content, 'html.parser')
            inner_date = sub_soup.find('div', 'field--name-field-press-release-date').find_all('div')[1].getText()
            print(inner_date)
            inner_title = sub_soup.find('div', 'field--name-field-press-header').getText()
            print(inner_title)
            doc_number = sub_soup.find('div', 'field--name-field-press-release-number').find_all('div')[1].getText()
            print(doc_number)
            outer_html = str(sub_soup.find('div', 'field--name-field-press-type'))+\
                        str(sub_soup.find('div', 'field--name-field-press-header'))+\
                        str(sub_soup.find('div', 'field--name-field-press-body'))+\
                        str(sub_soup.find('div', 'field--name-field-agency-reference'))+\
                        str(sub_soup.find('div', 'field--name-field-press-release-date'))+\
                        str(sub_soup.find('div', 'field--name-field-press-release-number'))
            print(outer_html) #outer html

        try:
            pagination_nav = soup.find('nav', 'pagination')
            next_page = pagination_nav.find('a', attrs={ 'title': 'Go to next page' })
            next_page_link = next_page['href']
            print("https://www.dol.gov/newsroom/releases/ilab"+next_page_link)
            URL = "https://www.dol.gov/newsroom/releases/ilab"+next_page_link
        except:
            print("All pages reaches")
            finish = False




