from bs4 import BeautifulSoup
import requests
import dbworker


def make_url(sid=1, sid2=0, lng=''):  # Function for make url to parse
    return 'http://swrailway.gov.ua/timetable/eltrain3-5/?sid={}&sid2={}&startPicker2=&dateR=0&lng={}'\
        .format(sid, sid2, lng)


for i in range(1, 4521):  # Parse all pages for find station 4521
    r = requests.get(make_url(i))
    soup = BeautifulSoup(r.text, 'lxml')
    ua_station = soup.find('td', class_='sh').find('input', id='namelike1').get('value')
    if ua_station == '':
        print('Nothing there in', i)
        dbworker.push_to_db((i, '', '', ''))
        continue
    r = requests.get(make_url(i, lng='_ru'))
    soup = BeautifulSoup(r.text, 'lxml')
    ru_station = soup.find('td', class_='sh').find('input', id='namelike1').get('value')
    r = requests.get(make_url(i, lng='_en'))
    soup = BeautifulSoup(r.text, 'lxml')
    en_station = soup.find('td', class_='sh').find('input', id='namelike1').get('value')
    dbworker.push_to_db((i, ua_station, ru_station, en_station))