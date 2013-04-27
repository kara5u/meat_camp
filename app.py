# -*- coding: utf-8 -*-

from flask import Flask, make_response
import mechanize
import BeautifulSoup
import json
import sqlite3

app = Flask(__name__)
DEBUG = True



def search_bot(url):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', ('Mozilla/5.0 (Windows; U; Windows NT 5.1; rv:1.7.3)'' Gecko/20041001 Firefox/0.10.1'))]
    br.open(url)
    res = br.response().read()
    return res

def parse(xml):
    soup = BeautifulSoup.BeautifulSoup(xml)
    soup.prettify()
    res = list()
    for item in soup.findAll('item'):
        feed = dict()
        d = dict()
        print '#'
        en_html = ""
        for tag in item:
            if tag.__class__.__name__ == "Tag":
                if d.has_key(tag.name) == False:
                    d[tag.name] = list()
                d[tag.name].append(tag.string)
                if tag.name == "content:encoded":
                    c_soup = BeautifulSoup.BeautifulSoup(tag.string)
                    for a in c_soup.findAll('a'):
                        if a.string == u"原文へ":
                            en_html = search_bot(a.get('href'))
        feed["ja_JP"] = d
        feed["en"] = en_html
        res.append(feed)
    return res 

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
    json_string = "["
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


