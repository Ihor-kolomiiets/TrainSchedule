from enum import Enum

token = '382546574:AAE2kuiu51P01BE9_5YnFlNGlsN2kY3rUTE'
stations_database = 'trainSchedule.db'
users_database = 'users.db'


#  Класс состояний
class States(Enum):
    S_START = '0'
    S_STATIONSEARCH = '1'
    S_SECONDADD = '2'
    S_DELETEFIRST = '3'
    S_DELETESECOND = '4'
    S_NUFFIN = '_'
