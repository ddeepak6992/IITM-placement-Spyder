# -*- coding: utf-8 -*-

import mechanize
import cookielib
from bs4 import BeautifulSoup
from lxml import etree


def extract(elem):
    try:
        elem = elem.getchildren()[0]
        return extract(elem)
    except:
        return elem.text.strip()
def scraper(USERNAME, PASSWORD):    
    print 'Fetching database'
    #Browser
    br = mechanize.Browser()
     
    #Cookie Jar
    cj = cookielib.LWPCookieJar()
     
    #Browser Options
    br.set_cookiejar(cj)
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
     
     
    #Adding request headers
    br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0'),
                                  ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                                  ('Accept-Language', 'en-gb,en;q=0.5'),
                                  ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')]
    
    br.open('http://placement.iitm.ac.in/students/login.php')
    br.select_form(nr=0)
    for control in br.form.controls:
        if control.name == 'rollno':
            br[control.name] = USERNAME
        if control.name == 'pass':
            br[control.name] = PASSWORD
    br.submit()
    res = br.open('http://placement.iitm.ac.in/students/app_comp.php')
    html_doc = res.read()
    soup = BeautifulSoup(html_doc)
    mainContent = soup.find_all(name = 'div', attrs = {'id':'content'})[0]
    table_str = str(mainContent.find_all('table')[2])
    
    parser = etree.XMLParser(recover=True)
    table = etree.fromstring(table_str, parser=parser)
    rows = table.getchildren()
    database = {}
    for row in rows[2:]:
        elems = [x for x in row.iterchildren()]
        company = extract(elems[1])
        profile = extract(elems[2])
        test = extract(elems[3])
        GD = extract(elems[4])
        interview = extract(elems[5])
        database[str((company,profile))] = str([test,GD,interview])
    return database
