import os
import time
from bs4 import BeautifulSoup, Comment
from flask import Flask, render_template, redirect, url_for
import re
import requests
import json
import io
import numpy as np

app = Flask(__name__)

def fetch(url):
    data = []
    html = requests.get(url)
    parseable = BeautifulSoup(html.content,"html.parser")
    odds_table = parseable.find("table", {"id": "odds_table"})
    rows = odds_table.findAll('tr',{'data-dt': re.compile(r".*")})
    for item in rows:
        obj = {}
        country = item.find('img')['alt']
        obj['country'] = country
        all_odds = item.findAll('td',{'data-aff-dt': re.compile(r".*")})
        odds = []
        for item in all_odds:
            odds.append(float(item.contents[0]))
        avg = np.mean(odds)
        avg = "%.2f" % (1 / avg * 100) +"%"
        obj['odds'] = avg
        data.append(obj)
    return data

#Only fetch new data if data is older than 2 hours
datasets = [['static/data.json','https://eurovisionworld.com/odds/eurovision'],['static/data-top10.json','https://eurovisionworld.com/odds/eurovision-top-10'],['static/data-semi1.json','https://eurovisionworld.com/odds/eurovision-semi-final-1'],['static/data-semi2.json','https://eurovisionworld.com/odds/eurovision-semi-final-2']]

for dataset in datasets:
    file_mod_time = os.stat(dataset[0]).st_mtime
    last_time = (time.time() - file_mod_time) / 360
    if last_time > 2:
        data = fetch(dataset[1])
        with io.open(dataset[0], 'w', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False))

@app.route('/eurovision')
def render_home():
    #print last_time
    return render_template('index.html')

@app.route('/')
def redirect_home():
    #print last_time
    return redirect(url_for('render_home'))

if __name__ == '__main__':
    app.run(debug=True)