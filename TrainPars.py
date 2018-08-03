import json
import sqlite3
import time
import requests
from bs4 import BeautifulSoup
import config
import GetSchedule


def make_region_url(geo2_list=2, lng=''):  # Function for make url to parse
    return 'http://swrailway.gov.ua/timetable/eltrain3-5/?geo2_list={}&lng={}'.format(geo2_list, lng)


def pars_region():  # Pars regions names
    conn = sqlite3.connect(config.stations_database)
    cursor = conn.cursor()
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
        cursor.execute("INSERT INTO regions (id, name_ua, name_ru, name_en) VALUES ('%s', '%s', '%s', '%s')"
                       % (str(i), ua_region, ru_region, en_region))
    conn.commit()
    cursor.close()
    conn.close()


def pars_stations():
    conn = sqlite3.connect(config.stations_database)
    cursor = conn.cursor()
    sid = 1
    while True:
        stations_list = []
        url = GetSchedule.make_station_url(sid, lng='')
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        r.close()
        region = soup.find('td', colspan='5').find('a', class_='et').get('href')
        region_id = region.replace('?geo2_list=', '').replace('&lng=', '')
        stations_list.append(str(sid))
        check_for_valid = soup.find('td', colspan='50')
        if region_id == '' and sid > 5000:
            print("End of pars data")
            break
        if check_for_valid is not None:
            print('Not valid')
            sid += 1
            continue
        for lng in ['', '_ru', '_en']:
            time.sleep(1)
            json_url = 'http://swrailway.gov.ua/timetable/eltrain3-5/?JSON=station&id=%s&lng=%s' %(sid, lng)
            r = requests.get(json_url)
            j = json.loads(r.text)
            r.close()
            station_name = j['label']
            stations_list.append(station_name)
        stations_list.append(region_id)
        stations_tuple = tuple(stations_list)
        print(stations_tuple)
        cursor.execute('INSERT INTO stations (station_id, name_ua, name_ru, name_en, region_id) '
                       'VALUES ("%s", "%s", "%s", "%s", "%s")' % stations_tuple)
        sid += 1
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    pars_stations()
