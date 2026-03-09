from flask import Flask, render_template, request, jsonify, session # adding session to store tag variable for other post request
import x
import uuid
import time

from icecream import ic
ic.configureOutput(prefix=f'----- | ', includeContext=True)

app = Flask(__name__)
app.secret_key = 'any_secret_string_here' # This is required!

################ rendering pages
@app.route('/')
def index():
    return render_template('index.html', error=None)

@app.get("/signup")
def show_signup():
    try:
        return render_template("page_signup.html", x=x)
    except Exception as ex:
        print(ex, flush = True)
        return "ups ..."

@app.get("/create_destination")
def show_create_destination():
    try:
        if 'user_id' not in session:
            return redirect('/') # Redirect to login if not logged in
    
    # Pull data from session to pass to the template
        return render_template('page_create_destination.html', username=session.get('current_username'), user_id=session.get('user_id'))
    except Exception as ex:
        print(ex, flush = True)
        return "ups ..."


#################### LOG IN ROUTE
@app.post('/create_destination')
def login():
    try:
        user_username = request.form.get('user_username')
        user_password = request.form.get('user_password')
        db, cursor = x.db()
        # q = "SELECT * FROM users WHERE user_username = %s AND user_password = %s;"
        q = "SELECT user_id, user_username FROM users WHERE user_username = %s AND user_password = %s"
        cursor.execute(q, (user_username, user_password))
        
        # fetching the very first result in sql 
        row = cursor.fetchone()
        
        print("DATABASE RESULT:", row, flush=True)

        if row:
            # print return dictionary/object {} using keys instead of row[0]
            current_id = row['user_id']
            # save to session for next post request
            session['user_id'] = row['user_id']

            current_username = row['user_username']
            session['current_username']
            return render_template('page_create_destination.html', 
                                   username=current_username, 
                                   user_id=current_id)
        else:
            return render_template('index.html', error="Invalid username or password")
       
    except Exception as ex:
        print(f"Error: {ex}")
        return "Internal server error", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close() 

############################## CHECK USERNAME
@app.post("/api-check-username")
def check_username():
    try:
        user_username = x.validate_user_username()
        db, cursor = x.db()
        q = "SELECT * FROM users WHERE user_username = %s"
        cursor.execute(q, (user_username,))
        row = cursor.fetchone()
        if not row:
            return f"""
                <browser mix-update="span">
                    Username available
                </browser>
            """
        
        return f"""
            <browser mix-update="span">
                Username taken
            </browser>
        """        

    except Exception as ex:
        # print(ex, flush = True)
        ic(ex)

        if "--error-- user_username" in str(ex):
            return f"""<browser mix-update="span">{ex.args[0]}</browser>""", 400

        # Worst case, something unexpected
        return f"""<browser mix-update="span">System under maintenance</browser>""", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()  


############################## SIGN UP
@app.post("/signup")
def signup_post():
    try:
        user_password = x.validate_user_password()
        user_username = x.validate_user_username()
        user_pk = uuid.uuid4().hex
        db, cursor = x.db()
        q = "INSERT INTO users VALUES(%s, %s, %s)"        
        cursor.execute(q, (user_pk, user_username, user_password))
        db.commit()
        return "ok"
    except Exception as ex:

        # How do you check if it is a number
        if "Duplicate entry" in str(ex) and "user_username" in str(ex):
            return "username already in the system", 400

        return ex.args[0], ex.args[1]

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


############################## CREATE USER
@app.post("/api-create-user")
def create_user():
    try:
        user_username = x.validate_user_username()
        user_password = x.validate_user_password()
        user_pk = uuid.uuid4().hex
        db, cursor = x.db()
        q = "INSERT INTO users VALUES(%s, %s, %s)"
        cursor.execute(q, (user_pk, user_username, user_password))
        db.commit()

        tip = render_template("___tip.html", message="User created", status="ok")

        return f"""
        <browser mix-update="#tooltip">{tip}</browser>
        """
    
    except Exception as ex:
        # print(ex, flush = True)
        ic(ex)

        if "--error-- user_username" in str(ex):
            return f"""<browser mix-update="span">{ex.args[0]}</browser>""", 400

        if "--error-- user_password" in str(ex):
            tip = render_template("___tip.html", message="Invalid password", status="error")
            return f"""<browser mix-update="#tooltip">{tip}</browser>""", 400
        
    
        if "Duplicate entry" in str(ex) and "user_username" in str(ex):
            return f"""<browser mix-update="span">Username taken</browser>""", 400

        # Worst case, something unexpected
        return f"""<browser mix-update="span">System under maintenance</browser>""", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()  


############ CREATE DESTINATION
@app.post("/create_destination_login")
def create_destination():
    try:
        current_user_id = session.get('user_id')
        current_username = session.get('user_username') # Get the name here!

        travel_title = request.form.get('travel_title')
        travel_id = uuid.uuid4().hex
        travel_description = request.form.get('travel_description')
        travel_location = request.form.get('travel_location')
        travel_country = request.form.get('travel_country')

        travel_from_date = request.form.get('travel_from_date')
        travel_to_date = request.form.get('travel_to_date')
      
        db, cursor = x.db()
        q = "INSERT INTO travel (travel_id, fk_user_id, travel_title, travel_description, travel_location, travel_country, travel_from_date, travel_to_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(q, (travel_id, current_user_id, travel_title, travel_description, travel_location, travel_country, travel_from_date, travel_to_date))
        db.commit()

        return render_template("page_create_destination.html", username=current_username)

    except Exception as ex:
        return "Internal server error -create destination", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()  
