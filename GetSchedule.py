from bs4 import BeautifulSoup
import requests
import dbworker
import TrainPars


# a = 'Суми'
# b = dbworker.find_train(a)
# print(b)
# r = requests.get(TrainPars.make_station_url(b[0]))
r = requests.get(TrainPars.make_station_url(2858))


def print_data():
    soup = BeautifulSoup(r.text, 'lxml')
    result = soup.find('table', class_='td_center').find_all('tr', height='20')[2:]
    message = ''
    for schedule_array in result:
        i = schedule_array.text.strip().split('\n')
        message += 'Поїзд: ' + i[0] + '\n' + 'Обіг: ' + i[1] + '\n' + 'Маршрут: ' + i[2] + '\n' + \
                   'Прибуття: ' + i[3] + '\n' + 'Відправлення: ' + i[4] + '\n\n'
    return message


if __name__ == '__main__':
    print(print_data())
