from flask import request
import mysql.connector
import re # Regular expressions also called Regex

##############################
def db():
    try:
        db = mysql.connector.connect(
            host = "mariadb",
            user = "root",  
            password = "password",
            database = "2026_1_backend"
        )
        cursor = db.cursor(dictionary=True)
        return db, cursor
    except Exception as e:
        print(e, flush=True)
        raise Exception("Database under maintenance", 500)


##############################
USER_PASSWORD_MIN = 2
USER_PASSWORD_MAX = 20
USER_PASSWORD_REGEX = f"^.{{{USER_PASSWORD_MIN},{USER_PASSWORD_MAX}}}$"
def validate_user_password():
    user_password = request.form.get("user_password", "").strip()

    if not re.match(USER_PASSWORD_REGEX, user_password):
        raise Exception("--error-- user_password")
    if len(user_password) < USER_PASSWORD_MIN:
        raise Exception(f"User password minimum {USER_PASSWORD_MIN } characters", 400)
    if len(user_password) > USER_PASSWORD_MAX:
        raise Exception(f"User password maximum {USER_PASSWORD_MAX } characters", 400)    
    return user_password


##############################
USER_USERNAME_MIN = 2
USER_USERNAME_MAX = 20
USER_USERNAME_REGEX = f"^.{{{USER_USERNAME_MIN},{USER_USERNAME_MAX}}}$"
def validate_user_username():
    user_username = request.form.get("user_username", "").strip()
    if not re.match(USER_USERNAME_REGEX, user_username):
        raise Exception("--error-- user_username")
    return user_username



