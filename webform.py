#!/usr/bin/env python                                                                                                                                                                

import re
import mechanize

from bs4 import BeautifulSoup

def select_form(form):
    return form.attrs.get('id', None) == 'form1'

def get_state_items(browser):
    browser.select_form(predicate=select_form)
    ctl = browser.form.find_control('ctl00$ContentPlaceHolder1$ddlState')
    state_items = ctl.get_items()
    return state_items[1:]

def get_city_items(browser):
    browser.select_form(predicate=select_form)
    ctl = browser.form.find_control('ctl00$ContentPlaceHolder1$ddlCity')
    city_items = ctl.get_items()
    return city_items[1:]

br = mechanize.Browser()
br.open('http://www.marutisuzuki.com/Maruti-Price.aspx')    
br.select_form(predicate=select_form)
br.form['ctl00$ContentPlaceHolder1$ddlmodel'] = ['AK'] # model = Maruti Suzuki Alto K10                                                                                              

for state in get_state_items(br):
    # 1 - Submit form for state.name to get cities for this state                                                                                                                    
    br.select_form(predicate=select_form)
    br.form['ctl00$ContentPlaceHolder1$ddlState'] = [ state.name ]
    br.submit()

    # 2 - Now the city dropdown is filled for state.name                                                                                                                             
    for city in get_city_items(br):
        br.select_form(predicate=select_form)
        br.form['ctl00$ContentPlaceHolder1$ddlCity'] = [ city.name ]
        br.submit()

        s = BeautifulSoup(br.response().read(), 'lxml')
        t = s.find('table', id='ContentPlaceHolder1_dtDealer')
        r = re.compile(r'^ContentPlaceHolder1_dtDealer_lblName_\d+$')

        header_printed = False
        
        if not t:
            break
            
        for p in t.findAll('span', id=r):
            tr = p.findParent('tr')
            td = tr.findAll('td')

            if header_printed is False:
                str = '%s, %s' % (city.attrs['label'], state.attrs['label'])
                print str
                print '-' * len(str)
                header_printed = True

            print (' '.join(['%s' % x.text.strip() for x in td]))