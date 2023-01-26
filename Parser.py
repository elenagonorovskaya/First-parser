# -*- coding: utf-8 -*-
"""
Spyder, mac ARM 64
Программа парсит данные с сайта с продажей мейн-кунов и рисует график зависимости возраста котенка от цены

"""

from bs4 import BeautifulSoup as bs
#import pandas as pd
import requests
from datetime import datetime
import matplotlib
#matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import copy
#import numpy as nm

class Kitten:
    def __init__(self, xgender, xage, xprice):
        self.gender = xgender
        self.age = xage
        self.price = xprice
        
    def show(self):
        print(self.gender, '\nВозраст: ', self.age, ' дней', '\nЦена: ', self.price, ' руб.')
    
   # def info(self):
   #    print(f'Age: {self.age}, Name: {self.name}')


class Cats:
    def __init__(self, xgender, xage, xprice):
        self.gender = copy.deepcopy(xgender)
        self.age = copy.deepcopy(xage)
        self.price = copy.deepcopy(xprice)
        self.count = len(xgender)
        
    def show(self):
        print(self.gender, '\nВозраст: ', self.age, ' дней', '\nЦена: ', self.price, ' руб.')
        
    def graph(self):
        x_female = []
        y_female = []
        x_male = []
        y_male = []
        for i in range(self.count):
            if self.gender[i] == 'Мальчик котёнок':
                x_male.append(self.age[i])
                y_male.append(self.price[i])
            else:
                x_female.append(self.age[i])
                y_female.append(self.price[i])
                
        plt.plot(x_male, y_male, 'ro', label=r'Котенок мальчик')
        plt.plot(x_female, y_female, 'ro', color='indigo', label=r'Котенок девочка')
        plt.xlabel(r'количество дней')
        plt.ylabel(r'цена, руб.')
        plt.title(r'Зависимость возраста котенка от цены') 
    
        
        
url='https://mainecoonomania.ru/mainecoon/filter/category-is-kitten/apply/'
#чтобы спарсить всех котят нужно менять параметр part, но эта страница не загружается в браузере, хотя код 200
#url='https://mc.yandex.ru/webvisor/46900656?wv-check=19576&wv-type=0&wmode=0&wv-part=2&wv-hit=835667887&page-url=https://mainecoonomania.ru/mainecoon/filter/category-is-kitten/apply/&rn=684583647&browser-info=et:1674757002:w:787x765:v:960:z:180:i:20230126211642:u:1662715669736880825:vf:fppw4pdxetycw4cz2ehur:st:1674757002&t=gdpr(14)ti(2)'

page = requests.get(url)
soup = bs(page.text, 'lxml')
part = 1

print(page.status_code)
temp = soup.find_all('h4', style='padding:0; margin:0 ; ') #котенок девочка или мальчик
temp2 = soup.find_all('ul', style='padding:0; margin:0  0 0 10px;') #информация о котенке
temp3 = soup.find_all('h3', class_='price pull-right') #цена


gender=[]
date_of_birth = []
age = []
price = []
current_date = datetime.now().date()


size = 0

for i in temp:
    s = i.text.split()
    gender.append(s[0] + ' ' + s[1])
    size += 1
   
for j in temp2:
    date = j
    s = date.find('li').text
    #date_of_birth.lstrip('Дата рождения: ')
    d = s.split(' ')
    date_of_birth.append(d[2])
    a = datetime.strptime(d[2], '%d.%m.%Y').date()
    current_age = current_date - a
    age.append(current_age.days)
        
for k in temp3:
    kk = k.text.split(' ')
    ss = int(kk[3])*1000 + int(kk[4])
    price.append(ss)
    
print(age, price, gender) #массивы возраста, цены и пола

caats=Cats(gender, age, price)
caats.show()
caats.graph()


Female_kitten = []    
Male_kitten = []

for i in range(0, size):
    cat_add = Kitten(gender[i], age[i], price[i])
    if gender[i] == 'Мальчик котёнок':
        Male_kitten.append(cat_add)
    else:
        Female_kitten.append(cat_add)

kit=Kitten(gender[0], age[0], price[0])
kit.show()

#Построение графика
# xAge_female = []
# yAge_female = []
# xAge_male = []
# yAge_male = []

# for i in range(len(Female_kitten)):
#     xAge_female.append(Female_kitten[i].age)
#     yAge_female.append(Female_kitten[i].price)

# for i in range(len(Male_kitten)):
#     xAge_male.append(Male_kitten[i].age)
#     yAge_male.append(Male_kitten[i].price)
    

# plt.plot(xAge_male, yAge_male, 'ro', label=r'Котенок мальчик')
# plt.plot(xAge_female, yAge_female, 'ro', color='indigo', label=r'Котенок девочка')
# plt.xlabel(r'количество дней')
# plt.ylabel(r'цена, руб.')
# plt.title(r'Зависимость возраста котенка от цены')  

plt.show()
