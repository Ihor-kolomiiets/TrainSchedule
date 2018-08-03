from enum import Enum

token = '622336168:AAHoSaq5Khu05TZ1oY4DXBI6F61lDhEb03A'
stations_database = 'trainSchedule.db'
users_database = 'users.db'


#  Класс состояний
class States(Enum):
    S_START = '0'
    S_STATIONSEARCH = '1'
    S_THROUGHSTATIONS = '2'
