import os
import string

import numpy as np
import pandas as pd
import sqlite3 as sql

db_file = os.path.join('market', 'market.db')

if os.path.exists(db_file):
    os.remove(db_file)

products = pd.read_csv('products.csv')
products['price'] = products['price'].map(str).str.replace(r'\$|\.00|,', '', regex=True).map(float)
products.fillna(products.mean(), inplace=True)
products['price'] = products['price'].map(int)
products['barcode'] = [''.join(np.random.choice(list(string.digits), 12)) for _ in range(len(products))]
products = products.reindex(columns=['name', 'price', 'barcode', 'description'])

from market import db
from market.model import Item, User

db.create_all()
db.session.rollback()
for i, row in products[products['name'].map(lambda d: len(d) < 50)].head(50).iterrows():
    item = Item(owner=None, **row.to_dict())
    db.session.add(item)
db.session.commit()
admin = User(username='admin', email_address='admin@example.com', password_hash='admin')
db.session.add(admin)
db.session.commit()