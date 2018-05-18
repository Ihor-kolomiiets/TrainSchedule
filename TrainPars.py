from bs4 import BeautifulSoup
import requests
import dbworker
import config
import mysql.connector


def make_station_url(sid=1, sid2=0, lng=''):  # Function for make url to parse
    return 'http://swrailway.gov.ua/timetable/eltrain3-5/?sid={}&sid2={}&startPicker2=&dateR=0&lng={}'\
        .format(sid, sid2, lng)


def make_region_url(geo2_list=2, lng=''):  # Function for make url to parse
    return 'http://swrailway.gov.ua/timetable/eltrain3-5/?geo2_list={}&lng={}'.format(geo2_list, lng)


def pars_station():
    for i in range(1, 4521):  # Parse all pages for find station 4521
        r = requests.get(make_station_url(i))
        soup = BeautifulSoup(r.text, 'lxml')
        ua_station = soup.find('td', class_='sh').find('input', id='namelike1').get('value')
        if ua_station == '':
            print('Nothing there in', i)
            dbworker.push_to_db((i, '', '', ''))
            continue
        r = requests.get(make_station_url(i, lng='_ru'))
        soup = BeautifulSoup(r.text, 'lxml')
        ru_station = soup.find('td', class_='sh').find('input', id='namelike1').get('value')
        r = requests.get(make_station_url(i, lng='_en'))
        soup = BeautifulSoup(r.text, 'lxml')
        en_station = soup.find('td', class_='sh').find('input', id='namelike1').get('value')
        dbworker.push_to_db((i, ua_station, ru_station, en_station))


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


def get_region():  # Bound region and stations
    conn = mysql.connector.connect(user=config.user, password=config.password,
                                   host=config.host, database=config.stations_database)
    cursor = conn.cursor()
    cursor.execute("SELECT id, ru_region_name from region")
    regions = cursor.fetchall()
    cursor.execute("SELECT id from stations")
    stations = cursor.fetchall()
    for station in stations:
        r = requests.get(make_station_url(station[0], lng='_ru'))
        soup = BeautifulSoup(r.text, 'lxml')
        region = soup.find('tr', class_='onx').find('td').find('a', class_='et').text
        for region_db in regions:
            if region_db[1] in region:
                cursor.execute('UPDATE stations SET region = %s where id = %s' % (region_db[0], station[0]))
                conn.commit()
                break
    cursor.close()
    conn.close()

