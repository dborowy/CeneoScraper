import requests
from bs4 import BeautifulSoup
from enum import Enum, auto
from app import app
from app.utils import extract_feature, remove_whitespace
import json

class Product():
    def __init__(self, product_id=None,name=None, opinions=[]):
        self.product_id = product_id
        self.name = name
        self.opinions = opinions

    def extract_product(self):
        page_response = requests.get('https://www.ceneo.pl/'+self.product_id)
        page_tree = BeautifulSoup(page_response.text, 'html.parser')
        self.name = page_tree.select('h1.product-name').pop().get_text().strip()
        try:
            opinions_count=int(page_tree.select("a.product-reviews-link > span").pop().get_text().strip())
        except IndexError:
            opinions_count = 0
        if opinions_count > 0:
            url_prefix = 'https://www.ceneo.pl/'
            url_postfix = '#tab=reviews'
            url = url_prefix+'/'+self.product_id+url_postfix
            opinions_list = []
            while url:
                page_response = requests.get(url)
                page_tree = BeautifulSoup(page_response.text, 'html.parser')
                opinions = page_tree.select('div.js_product-review')

                #opinion = opinions[0]
                for opinion in opinions: 
                    op = Opinion()
                    op.extract_opinion(opinion)
                    op.transform_opinion()
                    opinions_list.append(op)
                try:
                    url = url_prefix+page_tree.select("a.pagination__next").pop()["href"]
                except IndexError:
                    url = None
            self.opinions = opinions_list
    
    def __str__(self):
        return f'product id: {self.product_id}\n nazwa: {self.name}\n\n'+'\n'.join(str(opinion) for opinion in self.opinions)

    def __dict__(self):
        return {
            "product id": self.product_id,
            "product name": self.name,
            "opinions": [opinion.__dict__() for opinion in self.opinions]
        }
    
    def save_product(self):
        with open("app/opinions/"+self.product_id+".json", 'w', encoding="UTF-8") as fp:
            json.dump(self.__dict__(), fp, ensure_ascii=False, separators=(",",": "), indent=4 )

    def read_product(self, product_id):
        with open("app/opinions/"+product_id+".json", 'r') as f:
            pr = json.loads(f)
        self.product_id = product_id
        self.name = pr['name']
        opinions = pr['opinions']
        for opinion in opinions:
            op = Opinion()
            op.from_dict(opinion)
            self.opinions.append(op)


class Opinion:
    selectors = {
        'author':['div.reviewer-name-line'],
        'recommendation':['div.product-review-summary'],
        'stars':['span.review-score-count'],
        'content':['p.product-review-body'],
        'pros':['div.pros-cell > ul'],
        'cons':['div.cons-cell > ul'],
        'useful':['button.vote-yes','data-total-vote'],
        'useless':['button.vote-no','data-total-vote'],
        'purchased':['div.product-review-pz'],
        'purchase_date':['span.review-time > time:nth-of-type(1)','datetime'],
        'review_date':['span.review-time > time:nth-of-type(1)','datetime']   
    }
    def __init__(self,opinion_id=None,author=None,recommendation=None,
                stars=None,content=None,pros=None,cons=None,useful=None,
                useless=None,purchased=None,purchase_date=None,review_date=None):
        self.opinion_id = opinion_id
        self.author = author
        self.recommendation = recommendation
        self.stars = stars
        self.content = content
        self.pros = pros
        self.cons = cons
        self.useful = useful
        self.useless = useless
        self.purchased = purchased
        self.purchase_date = purchase_date
        self.review_date = review_date
         
    def __str__(self):
        return '\n'.join(key+': '+('' if getattr(self,key) is None else getattr(self,key)) for key in self.selectors.keys())
    
    def __dict__(self):
        features = {key:('' if getattr(self,key) is None else getattr(self,key))
                    for key in self.selectors.keys()}
        features['opinion_id'] = self.opinion_id
        return features

    def extract_opinion(self):
        for key, args in self.selectors.items():
            setattr(self, key, utils.extract_feature(opinion, *args))
        self.opinion_id = int(opinion["data-entry-id"])
    
    def transform_opinion(self):
        self.purchased = True if self.purchased == "Opinia potwierdzona zakupem" else False
        self.useful = int(self.useful)
        self.useless = int(self.useless)
        self.content = remove_whitespaces(self.content)
        self.pros = remove_whitespaces(self.pros)
        self.cons = remove_whitespaces(self.cons)

    def from_dict(self, opinion_dict):
        for key, value in opinion_dict.items():
            setattr(self, key, value)

