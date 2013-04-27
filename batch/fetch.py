# -*- coding: utf-8 -*-

import mechanize
import BeautifulSoup
import sqlite3
import json
import datetime

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
        d = dict()
        #print '#'
        en_html = ""
        pub_date = datetime.datetime.now()
        url = ""
        for tag in item:
            if tag.__class__.__name__ == "Tag":
                ## クライアントがkeyに":"が含まれる場合jsonをパースできないらしいので暫定的に対処．
                ## 設計上クライアントサイドで修正するべき問題であるため今後修正するべき．
                json_tag = tag.name.replace(":", "-")
                #if d.has_key(tag.name) == False:
                #    d[tag.name] = list()
                #d[tag.name].append(tag.string)
                if d.has_key(json_tag) == False:
                    d[json_tag] = list()
                d[json_tag].append(tag.string)
                if tag.name == "content:encoded":
                    c_soup = BeautifulSoup.BeautifulSoup(tag.string)
                    for a in c_soup.findAll('a'):
                        if a.string == u"原文へ":
                            l = a.get('href')
                            en_html = search_bot(l)
                            url = l
                elif tag.name == "pubdate":
                    pub_date = datetime.datetime.strptime(
                        tag.string.replace("+0000", ""), 
                        "%a, %d %b %Y %H:%M:%S ")
                #elif tag.name == "link":
                #    print tag.string.__str__()
                #    url = tag.string
        d["en"] = en_html
        #res.append(d)
        db_insert(json.dumps(d), url, pub_date)

    return res

def db_insert(feed, url, pubdate):
    print pubdate
    print url
    conn = sqlite3.connect("../main.db")
    c = conn.cursor()
    c.execute("select * from feed where url='%s'" % url)
    for row in c:
        print "abort"
        return 
    c.execute('insert into feed values (?, ?, ?)', (feed, url, pubdate))
    conn.commit()
    conn.close()


res = json.dumps(parse(search_bot('http://jp.techcrunch.com/feed/')))
#print res
#print json.loads(res)
