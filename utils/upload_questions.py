from scrape_question import get_data_from_url
import os

import sys
sys.path.append("../")

import mysql.connector

from s3_file_handler import S3_file_handler
from secret import *


s3_file_handler = S3_file_handler()

lc_db = mysql.connector.connect(
    host = mysql_host,
    user = mysql_user,
    password = mysql_password,
    database = mysql_db
)
cursor = lc_db.cursor(buffered=True)
query = "SELECT * FROM temp"
cursor.execute(query)

count = 0
# data = cursor
for id, url in cursor:
    print(id, url)

    result = get_data_from_url(id, url)
    if result["status"] == "failure":
        continue
    intro, level, accuracy = result["intro"], result["level"], result["accuracy"]

    filename = str(id) + ".txt"
    count += 1
    # if count <= 31:
    #     continue
    result = s3_file_handler.upload_file("../temp/" + filename, filename)
    print(result)
    os.remove("../temp/" + filename)
    lc_db1 = mysql.connector.connect(
        host = mysql_host,
        user = mysql_user,
        password = mysql_password,
        database = mysql_db
    )
    cursor1 = lc_db1.cursor(buffered=True)
    points = 5
    if level[0] == 'M':
        points += 5
    elif level[0] == 'H':
        points += 10
    points += (int(100-accuracy)) // 10
    update_query = "UPDATE questions SET intro='" + intro + "', level='" + level + "', acceptance=" + str(accuracy) + ", points=" + str(points)
    update_query += " WHERE id=" + str(id) + ";"
    print(update_query)
    try:
        cursor1.execute(update_query)
        lc_db1.commit()
        cursor1.close()
        lc_db1.close()
    except Exception as e:
        print(e)
    print(count)

print("total row affected: " + str(count))

lc_db.commit()
cursor.close()
lc_db.close()