#!/usr/bin/env python
'''
List classes that are offered by goodlife
'''

import requests
import operator
#Get all the regions
regions=[]
data={"knownCategoryValues":"","category":"Regions","contextKey":"findaclub"}
r = requests.post('http://www.goodlifefitness.com/webservices/getcitiesinregion.asmx/getregions',json=data)
dict = r.json()['d']
for region_info in dict:
    regions.append(region_info['name'])

#Get all the cities, build region to cities map and city to region map    
cities=[]    
citiesInRegion={}    
regionOfCity={}
for region in regions:
    data={"knownCategoryValues":"Regions:"+region+";","category":"Cities"}
    r = requests.post('http://www.goodlifefitness.com/webservices/getcitiesinregion.asmx/getcitiesbyregionfindaclass',json=data)
    dict = r.json()['d']
    for city_info in dict:
        cities.append(city_info['name'])
        citiesInRegion.setdefault(region,[]).append(city_info['name'])
        regionOfCity[city_info['name']]=region
        
classes=[]        
classesInCity={}
citiesWithClass={}
for city in cities:
    city_data={"knownCategoryValues":"Regions:"+regionOfCity[city]+";Cities:"+city+";","category":"Classes"}
    r = requests.post('http://www.goodlifefitness.com/webservices/getcitiesinregion.asmx/getclassesincity',json=city_data)
    dict = r.json()['d']
    for class_info in dict:
        classes.append(class_info['name'].strip())
        classesInCity.setdefault(city,[]).append(class_info['name'].strip())
        citiesWithClass.setdefault(class_info['name'].strip(),[]).append(city)

classPopularity={}
for offer in classes:
    classPopularity[offer]=classPopularity.get(offer,0)+1
    
#----Sample Usage
#----Question: Where are each classes offered, ranked by popularity and class name
with open('WhereAreTheClassesOffered.txt','w') as fp:
    rank = 1
    for offer, cities in sorted(citiesWithClass.items(), key=lambda x: (len(x[1]), x[0]), reverse=True):
        fp.write(str(rank)+"."+offer.encode('utf8')+" ")
        fp.write("--Offered in " + str(len(cities)) + " cities\n")
        for city in cities:
            fp.write("\t( {0}: {1} )\n".format(city, regionOfCity[city]))
        rank = rank + 1    
            
#----Question: What are the popularity of each course being offered in the city
with open('WhatAreTheCitiesOffering.txt','w') as fp:
    rank = 1
    for city, offers in sorted(classesInCity.items(), key=lambda x: len(x[1]), reverse=True):
        fp.write(str(rank)+".( {0}, {1} ) offers {2} classes\n".format(city, regionOfCity[city], len(offers)))
        for offer in sorted(offers, key = lambda x: classPopularity[x], reverse=True):
            fp.write("\t[ {0}: {1} ]\n".format(offer.encode('utf8'), classPopularity[offer]))
        rank = rank + 1