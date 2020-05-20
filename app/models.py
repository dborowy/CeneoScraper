import requests
from bs4 import BeautifulSoup

class Product():
    def __init__(self, product_id=None,name=None, opinions=[]):
        self.product_id = product_id
        self.name = name
        self.opinions = opinions

    def extract_product(self):
        page_response = requests.get('https://www.ceneo.pl/'+request.form['product_code'])
        page_tree = BeautifulSoup(page_response.text, 'html.parser')
        self.name = page_tree.select('hq.product_name').pop().get_text().strip()
        try:
            opinions_count=int(page_tree.select("a.product-reviews-link > span").pop().get_text().strip())
        except IndexError:
            opinions_count = 0
        if opinions_count > 0:
            url_prefix = 'https://www.ceneo.pl/'
            url_postfix = '#tab=reviews'
            url = url_prefix+'/'+product_id+url_postfix
            while url:
                page_response = requests.get(url)
                page_tree = BeautifulSoup(page_response.text, 'html.parser')
                opinions = page_tree.select('li.js_product-review')

                #opinion = opinions[0]
                for opinion in opinions:
                    features = {key:extract_feature(opinion, *args)
                                for key, args in selectors.items()}
                    features['opinion_id'] = int(opinion['data-entry-id'])
                    features['purchased'] = True if features['purchased'] == 'Opinia potwierdzona zakupem'else False
                    features['useful'] = int(features['useful'])
                    features['useless'] = int(features['useless'])
                    features['pros'] = remove_whitespace(features['pros'])
                    features['cons'] = remove_whitespace(features['cons'])
                    
                    opinions_list.append(features)


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
        return(f'opinion id: {self.opinion_id}\n author: {self.author}\n')
    
    def __repr__(self):
        pass

    def extract_opinion(self):
        pass

opinion = Opinion()
print(opinion)