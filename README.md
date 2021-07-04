# Code-Bot

## A discord bot for programming guilds to keep track on their coding stats

### What can this bot do?

#### Register user

> !lc register
> !lc register "username"

User can register to the bot by using any of the two commands. User can provide his/her/their own username or bot parses their discord username and allots them that parsed name.

#### Add moderator

> !lc moderator @user

Only admin can add a moderator, if any other user tries to add a moderator, bot denies it and sends an alert message.

#### See moderator

> !lc moderator

All registered users can see who are the moderators. Bot sends the list of usernames of moderators on responding to this command.

#### Post question

> !lc post

Moderators can post a question from the database using this command. Bot sends a message with embed with question, url, points, level.

#### Leader board

> !lc leaderboard

Users can check their progress by using this command, this command will return the top coders in the guild. A rating system has been defined on account of number of solved questions, attempted questions and those respective questions' difficulty.

#### Attempt a question

> 👍

Reacting 👍 to the question posted by moderator indicates that the particular user attempted the question.

#### Solved a question

> ✅

Reacting ✅ to the question posted by moderator indicates that the particular user solved the question.

### TO DO

- [ ] Self stats for each user
- [ ] Make markdown operators in the question as characters
- [ ] Moderator can add question to the database
- [ ] Help reaction

## TECH STACK

- python
- discord.py
- AWS S3
- AWS RDS (MySQL)

- EC2 (hosted on)

### Connect to S3

A python library called boto3 is used to connect to AWS s3 from python script. Check this [file](https://github.com/chandu1263/code-bot/blob/master/s3_file_handler.py)

### Relational database

#### Table users

| Field               | Type         | Null | Key | Default | Extra |
|---------------------|--------------|------|-----|---------|-------|
| userid              | varchar(255) | NO   | PRI | NULL    |       |
| username            | varchar(255) | NO   |     | NULL    |       |
| attempted_questions | int          | YES  |     | NULL    |       |
| solved_questions    | int          | YES  |     | NULL    |       |
| leetcode_username   | varchar(255) | YES  |     | NULL    |       |
| rating              | int          | YES  |     | 0       |       |

#### Table questions

| Field      | Type         | Null | Key | Default | Extra          |
|------------|--------------|------|-----|---------|----------------|
| id         | int          | NO   | PRI | NULL    | auto_increment |
| url        | varchar(510) | NO   | UNI | NULL    |                |
| intro      | varchar(510) | NO   | UNI | NULL    |                |
| level      | varchar(10)  | YES  |     | NULL    |                |
| acceptance | float        | YES  |     | NULL    |                |
| points     | int          | YES  |     | 5       |                |

#### Table moderators

| Field  | Type         | Null | Key | Default | Extra          |
|--------|--------------|------|-----|---------|----------------|
| id     | int          | NO   | PRI | NULL    | auto_increment |
| userid | varchar(255) | NO   | UNI | NULL    |                |

#### Table posted

| Field       | Type         | Null | Key | Default | Extra |
|-------------|--------------|------|-----|---------|-------|
| message_id  | varchar(255) | NO   | PRI | NULL    |       |
| time        | varchar(255) | NO   |     | NULL    |       |
| question_id | int          | NO   |     | NULL    |       |

#### Table solved

| Field      | Type         | Null | Key | Default | Extra |
|------------|--------------|------|-----|---------|-------|
| userid     | varchar(255) | NO   | PRI | NULL    |       |
| questionid | int          | NO   | PRI | NULL    |       |

### Table attempted

| Field      | Type         | Null | Key | Default | Extra |
|------------|--------------|------|-----|---------|-------|
| userid     | varchar(255) | NO   | PRI | NULL    |       |
| questionid | int          | NO   | PRI | NULL    |       |

## Populating the questions in database

- Scraping the geeks for geeks must to coding questions.
- Sorted them based on own rating system
- Saved each question in *.txt* format in S3

## Configurations

- There is a file missing in this repo which is secret.py

```
# mysql

mysql_host = <mysql host>
mysql_user = <mysql user>
mysql_password = <mysql password>
mysql_port = 3306

# database

mysql_db = <database name>

# s3 user access
access_key = <s3 access key>
secret_access_key = <s3 secret access key>

# s3 bucket name

s3_bucket_name = <s3 bucket name>

```

### discord bot key

- Export discord bot key as environment variable.
- In main.py, key is automatically selected from the env and will be used to run the discord bot client.

## References

- https://discordpy.readthedocs.io/en/stable/api.html
- https://realpython.com/how-to-make-a-discord-bot-python/
- https://youtu.be/-w7XYr22UEw

### Contact

- You can reach me through my [mail](chandutargaryen@gmail.com)
- Or on [discord](longshot_007#4675)
