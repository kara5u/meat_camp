# -*- coding: utf-8 -*-

from flask import Flask, make_response
import mechanize
import BeautifulSoup
import json
import sqlite3

app = Flask(__name__)
DEBUG = True

def select_db():
    res = list()
    conn = sqlite3.connect("main.db")
    c = conn.cursor()
    c.execute("select * from feed order by pubdate desc limit 10")
    for row in c:
        print row[1]
        res.append(row[0])
    conn.close()

    return res

@app.route('/')
def get():
    feeds = select_db()
    json_string = "[ "
    for txt in feeds:
        json_string += txt
        json_string += ","
    json_string = json_string[:-1] + "]"
    

    #response = make_response(str(json.dumps(parse(search_bot("http://jp.techcrunch.com/feed/")))))
    response = make_response(json_string)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
    #select_db()
    #debug()
    app.debug = DEBUG
    app.run()


