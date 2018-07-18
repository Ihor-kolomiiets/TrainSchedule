from bs4 import BeautifulSoup
import requests
import re
import dbworker
import config
import mysql.connector


def main():
    for id in range(2, 28):
        r = requests.get('http://swrailway.gov.ua/timetable/eltrain3-5/?geo2_list=%s&lng=' % id)
        if r.status_code != 200:
            continue
        soup = BeautifulSoup(r.text, 'lxml')
        result = soup.find_all('td', valign='top')[4:]
        stationsInfo = []
        for i in result:
            stationsInfo.append(i.find_all('a'))
        for i in stationsInfo:
            for j in i:
                if j.text == '':
                    continue
                test = re.search('\d+', j.get('href'))
                dbworker.push_to_db((test.group(0), j.text, id))


def make_station_url(sid=1, sid2=0, lng=''):  # Function for make url to parse
    return 'http://swrailway.gov.ua/timetable/eltrain3-5/?sid={}&sid2={}&startPicker2=&dateR=0&lng={}'\
        .format(sid, sid2, lng)


def make_region_url(geo2_list=2, lng=''):  # Function for make url to parse
    return 'http://swrailway.gov.ua/timetable/eltrain3-5/?geo2_list={}&lng={}'.format(geo2_list, lng)


def pars_region():  # Pars regions names
    for i in range(2, 28):
        if i == 25:
            continue
        r = requests.get(make_region_url(i))
        soup = BeautifulSoup(r.text, 'lxml')
        ua_region = soup.find('li').find_all('b')[10].text
        print(ua_region)
        r = requests.get(make_region_url(i, lng='_ru'))
        soup = BeautifulSoup(r.text, 'lxml')
        ru_region = soup.find('li').find_all('b')[10].text
        print(ru_region)
        r = requests.get(make_region_url(i, lng='_en'))
        soup = BeautifulSoup(r.text, 'lxml')
        en_region = soup.find('li').find_all('b')[9].text
        print(en_region)
        dbworker.push_to_region((i, ua_region, ru_region, en_region))


if __name__ == '__main__':
    main()