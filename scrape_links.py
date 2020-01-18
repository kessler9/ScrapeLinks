from bs4 import BeautifulSoup as BS
from time import time
import psycopg2
import requests
import config
import sys
import re

init_ts = time()

links = list(filter(lambda x: bool(x), [
    a.get('href', False) for a in 
    BS(requests.get(f'http://{sys.argv[1]}').text, features='html.parser').find_all('a')
]))

with open('links.txt', 'w+') as fh:
    fh.write('\n'.join(links))

connection = psycopg2.connect(config.CONNECTION_STRING)
cursor = connection.cursor()

for link in links:
    cursor.execute(
        "INSERT INTO LINKS(HREF, DOMAIN) VALUES(%s, %s)",
        (link, sys.argv[1],)
    )
    print(f'INSERTED {link}')

connection.commit()

print(f'DONE AFTER {time()-init_ts}s')
