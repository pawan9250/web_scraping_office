# main_url = "https://www.dol.gov/general/foia/reports/chief-foia-officer"
# article = xpath = "/html/body/div/div/main/div[2]/div/div/article" *//article[@role="article"]
# year_link = find element by tag name = a["href"]
# year
#titile
# outer_html = xpath = "//*[@id="block-pagetitle-2"]"+"/html/body/div/div/main/div[2]/div/div/article/div/div/div/div/div/div/div"

# from datetime import date
# from turtle import title
import requests
from bs4 import BeautifulSoup

URL = "https://www.dol.gov/general/foia/reports/chief-foia-officer"
base_url = "https://www.dol.gov"

years = ["2022"]
finish = True
all_sub_url = []
ln_titles = []
ln_date = []

# for year in years:
#     #collect outer date and link
#     while finish:
for year in years:
    r = requests.get(URL) #get url
    soup = BeautifulSoup(r.content, 'html.parser')
    article_tag = soup.find('article', attrs={ 'role': 'article' })
    sub_links = article_tag.find_all('a')
    for a_tag in sub_links:
        link = base_url+a_tag['href']
        
        a_tag_text = a_tag.getText()
        
        a_tag_year = a_tag_text.split(" ")[0]
        
        if a_tag_year not in years and a_tag_year != year: #check year in list
            print("All years finish")
            break
        print(link)
        print(a_tag_text)
        print(a_tag_year)
        if a_tag_year == year:
            all_sub_url.append(link)
            ln_titles.append(a_tag_text)
            ln_date.append("1/1/"+a_tag_year)

#collect outer html from sub links
for sub_url, dates, titles in zip(all_sub_url, ln_date, ln_titles):
    print(sub_url, "\n", dates, "\n", titles)
    sub_r = requests.get(sub_url)
    sub_soup = BeautifulSoup(sub_r.content, 'html.parser')
    outer_html = str(sub_soup.find('div', attrs={ 'id':'block-pagetitle-2'}))+\
                 str(sub_soup.find('div', 'paragraph paragraph--type--text-block paragraph--view-mode--default'))

    # print(outer_html)


    