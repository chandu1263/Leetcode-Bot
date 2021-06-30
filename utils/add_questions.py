import requests
from bs4 import BeautifulSoup
import mysql.connector

from secret import mysql_db, mysql_host, mysql_password, mysql_port, mysql_user
lc_db = mysql.connector.connect(
    host = mysql_host,
    user = mysql_user,
    password = mysql_password,
    database = mysql_db
)
cursor = lc_db.cursor()

url = "https://www.geeksforgeeks.org/must-do-coding-questions-for-companies-like-amazon-microsoft-adobe/"
page = requests.get(url)
soup = BeautifulSoup(page.content, features="html5lib")

data = soup.find_all('ol')
for each in data:
    for url in each.find_all('a', href=True):
        question_url = url['href'].strip()
        question_intro = url.text.strip()
        if "//practice.geeksforgeeks" in question_url and "/problems/" in question_url:
            query = "INSERT INTO questions (url, intro) VALUES ('" + question_url + "', '" + question_intro + "')"
            try:
                cursor.execute(query)
            except Exception as e:
                print(e)

lc_db.commit()
cursor.close()
lc_db.close()