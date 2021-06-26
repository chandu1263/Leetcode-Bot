import mysql.connector

from secret import mysql_host, mysql_password, mysql_port, mysql_user, mysql_db


def add_user_to_users(userid, username):
    result = {}
    try:
        lc_db = mysql.connector.connect(
            host = mysql_host,
            user = mysql_user,
            password = mysql_password,
            database = mysql_db
        )
        cursor = lc_db.cursor()
    except Exception as e:
        print(e)
        result["status"] = "failure"
        result["reason"] = "Database connection error"
        return result
    try:
        query = "INSERT INTO users"
        query += " (userid, username, attempted_questions, solved_questions) VALUES ("
        query += "'" + str(userid) + "', '" + str(username) + "', 0, 0)"
        cursor.execute(query)
        lc_db.commit()
        cursor.close()
        lc_db.close()
        result["status"] = "success"
        return result
    except mysql.connector.Error as e:
        result["status"] = "failure"
        result["reason"] = str(e.errno) + e.msg
        return result
    
def get_user_from_users(userid):
    result = {}
    try:
        lc_db = mysql.connector.connect(
            host = mysql_host,
            user = mysql_user,
            password = mysql_password,
            database = mysql_db
        )
        cursor = lc_db.cursor()
    except Exception as e:
        print(e)
        result["status"] = "failure"
        result["reason"] = "Database connection error"
        return result
    try:
        query = "SELECT userid, username, attempted_questions, solved_questions, leetcode_username FROM users"
        query += " WHERE userid='" + str(userid) + "'"
        cursor.execute(query)
        userid, username, attempted_questions, solved_questions = "", "", -1, -1
        for userid_, username_, attempted_questions_, solved_questions_, leetcode_username_ in cursor:
            userid = str(userid_)
            username = str(username_)
            attempted_questions = int(attempted_questions_)
            solved_questions = int(solved_questions_)
        result["status"] = "success"
        result["value"] = [userid, username, attempted_questions, solved_questions]
        return result
    except Exception as e:
        print(e)
        result["status"] = "failure"
        result["reason"] = "Database connection error"
        return result


def add_moderator(userid):
    result = {}
    try:
        lc_db = mysql.connector.connect(
            host = mysql_host,
            user = mysql_user,
            password = mysql_password,
            database = mysql_db
        )
        cursor = lc_db.cursor()
    except Exception as e:
        print(e)
        result["status"] = "failure"
        result["reason"] = "Database connection error"
        return result
    try:
        query = "INSERT INTO moderators (userid) VALUES (" + str(userid) + ")"
        cursor.execute(query)
        lc_db.commit()
        cursor.close()
        lc_db.close()
        result["status"] = "success"
        return result
    except Exception as e:
        print(e)
        result["status"] = "failure"
        result["reason"] = "Mentioned user is already a moderator"
        return result     

def get_moderators():
    result = {}
    try:
        lc_db = mysql.connector.connect(
            host = mysql_host,
            user = mysql_user,
            password = mysql_password,
            database = mysql_db
        )
        cursor = lc_db.cursor()
    except Exception as e:
        print(e)
        result["status"] = "failure"
        result["reason"] = "Database connection error"
        return result
    try:
        query = "SELECT * FROM moderators"
        cursor.execute(query)
        moderators = []
        for id, userid in cursor:
            moderators.append(userid)
        result["status"] = "success"
        result["moderators"] = moderators
        return result
    except Exception as e:
        print(e)
        result["status"] = "failure"
        result["reason"] = "Database connection error"
        return result