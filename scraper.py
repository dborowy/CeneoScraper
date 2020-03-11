#import bibliotek
import requests
from bs4 import BeautifulSoup
#adres URL strony z opiniami
url = 'https://www.ceneo.pl/82304782#tab=reviews'

#pobranie kodu HTML strony z adresu URL
page_response = requests.get(url)
page_tree = BeautifulSoup(page_response.text, 'html.parser')

#Wybranie z kodu strony fragmentów odpowiadających poszczególnym opiniom

opinions = page_tree.select('li.review-box')
opinion = opinions[0]
opinion_id = opinion['data-entry-id'].pop(0).string
author = opinion.select('div.reviewer-name-line').pop(0).string
recommendaion = opinion.select('div.product-review-summary').pop(0).string
stars = opinion.select('span.review-score-count').pop(0).string
purchased = opinion.select('div.product-review-pz').pop(0).string
useful = opinion.select('button.vote-yes').pop(0)['data-total-vote']
useless = opinion.select('button.vote-no').pop(0)['data-total-vote']
content = opinion.select('p.product-review-body').pop(0).get_text()

print(useless)
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