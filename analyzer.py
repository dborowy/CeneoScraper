import os 
import pandas as pd

print(os.listdir('./opinions'))

product_id = input('Podaj kod produktu: ')
opinions = pd.read_json('opinions/'+product_id+'.json')

print(opinions)