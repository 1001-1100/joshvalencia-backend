from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import pandas as pd
import numpy as np
from gsheets import Sheets
import random

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def getSheets():
    sheets = Sheets.from_files('client_secret.json','storage.json')
    url = 'https://docs.google.com/spreadsheets/d/16dHLD5WzkXBHLDg5Z9vO6nxKN_7a_lg4e-4xWzJYt38/'
    s = sheets.get(url)
    df = pd.DataFrame(s.sheets[0].values())
    df.columns = df.iloc[0]
    df = df.iloc[1:]
    return df

@app.route('/greetings', methods=['GET'])
@cross_origin()
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
    random.shuffle(greetings)
    finalGreetings = []
    greetingArray = []
    count = 0
    for g in greetings:
        count += 1
        greetingArray.append(g)
        if(count % 3 == 0):
            finalGreetings.append(greetingArray)
            greetingArray = []
    if(len(greetingArray) > 0):
        finalGreetings.append(greetingArray)
    return jsonify(finalGreetings)

@app.route('/quote', methods=['GET'])
@cross_origin()
def query_quotes():
    df = getSheets()
    quotes = []
    for q in df['quotes']:
        quotes.append(q)
    return jsonify(quotes)

# A welcome message to test our server
@app.route('/')
@cross_origin()
def index():
    return "<h1>Welcome to the Josh Valencia API!!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)