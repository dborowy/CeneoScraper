#import bibliotek
import requests
from bs4 import BeautifulSoup
#adres URL strony z opiniami
#url = 'https://www.ceneo.pl/82304782#tab=reviews'
url = 'https://www.ceneo.pl/76891701#tab=reviews'

#pobranie kodu HTML strony z adresu URL
page_response = requests.get(url)
page_tree = BeautifulSoup(page_response.text, 'html.parser')

#Wybranie z kodu strony fragmentów odpowiadających poszczególnym opiniom

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

    print(opinion_id,author,recommendation,stars,purchased,useful,useless,review_date,purchase_date)
# - opinia: li.review-box
# - identyfikator: li.review-box["data-entry-id"]
# - autor: div.reviewer-name-line
# - rekomendacja: div.product-review-summary > em
# - liczba gwiazdek: span.review-score-count
# - czy potwierdzona zakupem: div.product-review-pz
# - data wystawienia: span.review-time > time["datetime"] pierwsze wystąpienie
# - data zakupu: span.review-time > time["datetime"] drugie wystąpienie
# - przydatna: button.vote-yes["data-total-vote"]
# - nieprzydatna: button.vote-no["data-total-vote"]
# - treść: p.product-review-body
# - wady: div.cons-cell > ul
# - zalety: div.pros-cell > ul