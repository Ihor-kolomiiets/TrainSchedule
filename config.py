from enum import Enum
token = ''
database = ''


#  Класс состояний
class States(Enum):
    S_START = '0'
    S_STATIONSEARCH = '1'
    S_THROUGHSTATIONS = '2'
    S_SECONDSTATION = '3'
