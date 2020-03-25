#import bibliotek
import requests
from bs4 import BeautifulSoup
import pprint
import json
#adres URL strony z opiniami
#url = 'https://www.ceneo.pl/82304782#tab=reviews'
#76891701
url_prefix = 'https://www.ceneo.pl/'
product_id = input('Podaj kod produktu')
url_postfix = '#tab=reviews'
url = url_prefix+'/'+url_postfix
#pobranie kodu HTML strony z adresu URL
#page_response = requests.get(url)
#page_tree = BeautifulSoup(page_response.text, 'html.parser')
while url is not None:
        page_response = requests.get(url)
        page_tree = BeautifulSoup(page_response.text, 'html.parser')
#Wybranie z kodu strony fragmentów odpowiadających poszczególnym opiniom
opinions_list = []

opinions = page_tree.select('li.js_product-review')
#opinion = opinions[0]
for opinion in opinions:
    opinion_id = opinion["data-entry-id"]
    author = opinion.select('div.reviewer-name-line').pop(0).string
    try: 
        recommendation = opinion.select('div.product-review-summary').pop(0).string
    except IndexError:
        recommendation = None
    stars = opinion.select('span.review-score-count').pop(0).string
    try:
        purchased = opinion.select('div.product-review-pz').pop(0).string
    except IndexError:
        purchased = None
    useful = opinion.select('button.vote-yes').pop(0)['data-total-vote']
    useless = opinion.select('button.vote-no').pop(0)['data-total-vote']
    content = opinion.select('p.product-review-body').pop(0).get_text()
    try:
        cons = opinion.select('div.cons-cell > ul').pop(0).get_text
    except IndexError:
        cons = None
    try:
        pros = opinion.select('div.pros-cell > ul').pop(0).get_text
    except IndexError:
        pros = None
    date = opinion.select('span.review-time > time')
    review_date = date.pop(0)['datetime']
    try:
        purchase_date = date.pop(0)['datetime']
    except IndexError:
        purchase_date = None

    #print(opinion_id,author,recommendation,stars,purchased,useful,useless,review_date,purchase_date)
    opinions_dict = {
        'opinion_id':opinion_id,
        'author':author,
        'recommendation':recommendation,
        'stars':stars,
        'content':content,
        'pros':pros,
        'cons':cons,
        'useful':useful,
        'useless':useless,
        'purchased':purchased,
        'purchase_date':purchase_date,
        'review_date':review_date    
    }
    opinions_list.append(opinions_dict)
    try:
        url =url_prefix+page_tree.select('a.pagination_next').pop()['href']
    except IndexError:
        url = None

filename = product_id+'.json'
with open ('opinions.json','w') as fp:
    json.dump(opinions_list, fp, ensure_ascii=False)


