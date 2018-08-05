from bs4 import BeautifulSoup
import requests
import dbworker

# 5 последних запросов сохранять в бд


def make_station_url(sid=1, sid2=0, lng=''):  # Function for make url to parse
    return 'http://swrailway.gov.ua/timetable/eltrain3-5/?sid={}&sid2={}&startPicker2=&dateR=0&lng={}'\
        .format(sid, sid2, lng)


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
                   + 'Маршрут: ' + schedule[2].text + '\n' + 'Прибуття на ' \
                   + stations_name[0].find('b').text + ': ' + schedule[3].text + '\n' \
                   + 'Відправлення зі ' + stations_name[0].find('b').text + ': ' + schedule[4].text + '\n' \
                   + 'Прибуття на ' + stations_name[1].find('b').text + ': ' + schedule[5].text + '\n' \
                   + 'Відправлення зі ' + stations_name[1].find('b').text + ': ' + schedule[6].text + '\n\n'
        if len(message) > 2600:
            splitted_message.append(message)
            message = ''
    splitted_message.append(message)
    print(splitted_message)
    return splitted_message


if __name__ == '__main__':
    print_data('Сумы')
