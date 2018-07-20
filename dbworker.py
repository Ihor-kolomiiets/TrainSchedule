import config
import sqlite3
import requests
import json
from bs4 import BeautifulSoup

r = requests.get('http://i.ua')
r.close()