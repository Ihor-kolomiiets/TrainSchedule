import requests
from bs4 import BeautifulSoup

# 5 последних запросов сохранять в бд


def make_station_url(sid=1, sid2=0, lng=''):  # Function for make url to parse
    return 'http://swrailway.gov.ua/timetable/eltrain3-5/?sid={}&sid2={}&startPicker2=&dateR=0&lng={}'\
        .format(sid, sid2, lng)


def lviv_station_url(station_id):
    return 'http://railway.lviv.ua/scripts/rozklad_2018-v2/station.php?station=%s' % str(station_id)


def lviv_route_url(station_id1, station_id2):
    return 'http://railway.lviv.ua/scripts/rozklad_2018-v2/?s1=%s&s2=%s' % (str(station_id1), str(station_id2))


# getting schedule for station from south railroad
def print_data(station_id):
    r = requests.get(make_station_url(station_id))
    soup = BeautifulSoup(r.text, 'lxml')
    result = soup.find('table', class_='td_center').find_all('tr', height='20')[2:]
    message = ''
    splitted_message = []
    for schedule_array in result:
        i = schedule_array.text.strip().split('\n')
        message += 'Поїзд: ' + i[0] + '\n' + 'Обіг: ' + i[1] + '\n' + 'Маршрут: ' + i[2] + '\n' + \
                   'Прибуття: ' + i[3] + '\n' + 'Відправлення: ' + i[4] + '\n\n'
        if len(message) > 2700:
            splitted_message.append(message)
            message = ''
    splitted_message.append(message)
    print(splitted_message)
    return splitted_message


# getting schedule for station from lviv railroad
def print_lviv_station(station_id):
    r = requests.get(lviv_station_url(station_id))
    soup = BeautifulSoup(r.text, 'lxml')
    result = soup.find('table', class_='table table-striped table-hover table-condensed').find_all('tr')[1:]
    message = ''
    splitted_message = []
    for i in result:
        array_of_row = i.text.split('\n')
        if not array_of_row[6]:
            array_of_row[6] = 'щоденно'
        if not array_of_row[3]:
            array_of_row[3] = '-'
        if not array_of_row[5]:
            array_of_row[5] = '-'
        message += "Поїзд: " + array_of_row[1] + '\n' + 'Обіг: ' + array_of_row[6] + '\n' \
                   + 'Маршрут: ' + array_of_row[2] + '\n' + 'Прибуття: ' + array_of_row[3] + '\n' \
                   + 'Відправлення: ' + array_of_row[5] + '\n\n'
        print(len(message))
        if len(message) > 2500:
            splitted_message.append(message)
            message = ''
    splitted_message.append(message)
    return splitted_message


# getting schedule between two station from lviv railroad
def print_lviv_schedule(station_id, station_id2):
    r = requests.get(lviv_route_url(station_id, station_id2))
    soup = BeautifulSoup(r.text, 'lxml')
    result = soup.find('table', class_='table table-striped table-hover table-condensed')
    if result is None:
        print('Empty')
        return False
    result = result.find_all('tr')[1:]
    message = ''
    splitted_message = []
    for i in result:
        schedule = i.text.split('\n')
        if not schedule[10]:
            schedule[10] = 'щоденно'
        message += 'Поїзд: ' + schedule[1].strip() + '\n' + 'Обіг: ' + schedule[10].strip() + '\n' \
                   + 'Відправлення зі ст. ' + schedule[4].strip() + ': ' + schedule[3].strip() + '\n' \
                   + 'Прибуття на ст. ' + schedule[8].strip() + ': ' + schedule[7].strip() + '\n\n'
        if len(message) > 2500:
            splitted_message.append(message)
            message = ''
    splitted_message.append(message)
    print(message)
    print(splitted_message)
    return splitted_message


# getting schedule between two station from south railroad
def print_data_schedule(station_id, station_id2):
    r = requests.get(make_station_url(station_id, station_id2))
    soup = BeautifulSoup(r.text, 'lxml')
    result = soup.find('table', class_='td_center').find_all('tr', height='20')[2:]
    stations_name = soup.find('table', class_='td_center').find_all('tr', height='20')[0].find_all('td', colspan='2')
    if not result:
        return False
    message = ''
    splitted_message = []
    for schedule_array in result:
        schedule = schedule_array.find_all('td')
        message += 'Поїзд: ' + schedule[0].find('a').text + '\n' + 'Обіг: ' + schedule[1].text + '\n' \
                   + 'Маршрут: ' + schedule[2].text + '\n' \
                   + 'Відправлення зі ' + stations_name[0].find('b').text + ': ' + schedule[4].text + '\n' \
                   + 'Прибуття на ' + stations_name[1].find('b').text + ': ' + schedule[5].text + '\n\n'
        """ Telegram have restriction for message with more than 3000 characters,
        we need split big message. 2600 was chosen because message should be splited properly,
        for prevent split information related to one station"""
        if len(message) > 2600:
            splitted_message.append(message)
            message = ''
    splitted_message.append(message)
    print(splitted_message)
    return splitted_message


if __name__ == '__main__':
    pass
    # print_lviv_schedule(509, 874)
