from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from gsheets import Sheets
import random

app = Flask(__name__)

def getSheets():
    sheets = Sheets.from_files('client_secret.json','storage.json')
    url = 'https://docs.google.com/spreadsheets/d/16dHLD5WzkXBHLDg5Z9vO6nxKN_7a_lg4e-4xWzJYt38/'
    s = sheets.get(url)
    df = pd.DataFrame(s.sheets[0].values())
    df.columns = df.iloc[0]
    df = df.iloc[1:]
    return df

@app.route('/')
def hello_world():
    return 'Hello there!'

@app.route('/greetings', methods=['GET'])
def query_greetings():
    df = getSheets()
    greetings = []
    print(df['message'], df['name'])
    messages = df['message']
    names = df['name']
    for i in range(1, len(messages)+1):
        print(i)
        greetings.append({
            'message': messages[i],
            'name': names[i]
        })
    return jsonify(greetings)

@app.route('/quote', methods=['GET'])
def query_quotes():
    df = getSheets()
    quotes = df['quotes']
    index = random.randint(1, len(quotes))
    return jsonify({'quote': quotes[index]})

app.run()