import os
from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory, g, session
from tempfile import mkdtemp
from flask_session import Session
import sqlite3 as sql
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Constants
UPLOAD_FOLDER = "static/images/"
ALLOWED_EXTENSIONS = {'jpg','png','jpeg'}
DATABASE = 'database.db'

# App configs
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)


# Source code: https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
# Attach database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sql.connect(DATABASE)
    return db

# Close connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Source code: https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
# File uploads
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Main gallery of all photos
@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
   
    # GET request used to search by name
    search = request.args.get("search")



    # Modify search_query based on if search exists
    sqlite_query = """SELECT DISTINCT name, filepath, user_id FROM images"""
    if search:
        # Search for users or by file name

        sqlite_query = sqlite_query + """ WHERE images.name LIKE ? OR user_id IN (
                                          SELECT user_id FROM users WHERE username LIKE ?)"""
        cursor.execute(sqlite_query, ("%" + search + "%", "%" + search + "%"))

    else:
        cursor.execute(sqlite_query)

    # Get database query results
    records = cursor.fetchall()

    # Pass database info into template
    for i in range(len(records)):
        user_id = records[i][2]
        user_query = """SELECT username FROM users WHERE user_id=?"""
        cursor.execute(user_query,(user_id,))
        name = cursor.fetchall()[0]
        records[i] = records[i] + name

    return render_template("index.html", list=records)


# Personal Photo Gallery
@app.route("/my-images")
@login_required
def owned():
    db = get_db()
    cursor = db.cursor()

    # GET request for search by filename
    search = request.args.get("search")

    # Get all images owned by user
    # Modifier for search query if there is search bar value
    sqlite_query = """SELECT DISTINCT name, filepath FROM images WHERE user_id = ?"""
    if search:
        sqlite_query = sqlite_query + """ AND images.name LIKE ?"""
        cursor.execute(sqlite_query, (session["user_id"], "%" + search + "%",))
    else:
        cursor.execute(sqlite_query, (session["user_id"],))

    records = cursor.fetchall()

    # Find username
    user_query = """SELECT username FROM users WHERE user_id=?"""
    cursor.execute(user_query,(session["user_id"],))
    user=cursor.fetchall()[0][0]

    return render_template("my-images.html", list=records, user=user)


# Route to upload photos into repo
@app.route('/add', methods=['GET', 'POST'])
@login_required
def upload_file():

    # POST request
    if request.method == 'POST':

        # check if the post request has the file part, redirect back if not
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        # Get files from file upload
        files = request.files.getlist('files[]')
        
        db = get_db()
        cursor = db.cursor()

        # Iterate through files
        for file in files:
            # If user does not select file, browser also submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            # Save file into uploads folder in way that each user can have 1 image with given name
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                user_filename = str(session["user_id"]) + "____" + filename
                path = os.path.join(app.config['UPLOAD_FOLDER'], user_filename)
                file.save(path)
            
                # Convert data into tuple format
                data_tuple = (filename, path, session["user_id"],)
                sqlite_insert_query = """ INSERT INTO images (name, filepath, user_id) VALUES (?, ?, ?)"""
    
                # Insert into database
                cursor.execute(sqlite_insert_query, data_tuple)

                db.commit()

        return redirect(url_for('index'))

    # GET request
    return render_template('add.html')
        

# Route to delete photos
@app.route('/delete', methods=['GET','POST'])
@login_required
def delete_file():
    db = get_db()
    cursor = db.cursor()

    # Post request
    if request.method == "POST":
        deletes=request.form.getlist("deletes")

        # If no photos selected to delete, return request url
        if not deletes:
            return(redirect(request.url))

        # Delete selected images if they exist 
        sqlite_delete_query = """ DELETE FROM images WHERE filepath = ? """
        for item in deletes:
            if os.path.exists(item):
                os.remove(item)
            cursor.execute(sqlite_delete_query, (item,))
            db.commit()

        return redirect(url_for('index'))

    # Create gallery of user's photos, similar to owned()
    sqlite_query = """SELECT DISTINCT name, filepath FROM images WHERE user_id = ?"""
    cursor.execute(sqlite_query, (session["user_id"],))
    records = cursor.fetchall()

    user_query = """SELECT username FROM users WHERE user_id=?"""
    cursor.execute(user_query,(session["user_id"],))
    user=cursor.fetchall()[0][0]

    return render_template("delete.html", records=records, user=user)


# Login route
@app.route('/login', methods=['GET','POST'])
def login():
    # Forget any user_id
    session.clear()

    db = get_db()
    cursor = db.cursor()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html", msg="Must submit username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html", msg="Must submit password")

        # Query database for username
        cursor.execute("""SELECT * FROM users WHERE username = ?""", (request.form.get("username"),))
        rows = cursor.fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            return render_template("login.html", msg="Incorrect username or password")

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html", msg="")


## Logout route
@app.route("/logout")
@login_required
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# Register route
@app.route("/register", methods=["GET", "POST"])
def register():
    db = get_db()
    cursor = db.cursor()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Get all needed information if inputted
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirmation")
        cursor.execute("""SELECT username FROM users""")

        usernames = cursor.fetchall()
        # Ensure username was submitted
        if not username:
            return render_template("register.html", msg="Must submit username")

        # Ensure password was submitted
        elif not password:
            return render_template("register.html", msg="Must submit password")

        # Ensure passwords match
        elif not password == confirm:
            return render_template("register.html", msg="Passwords do not match")

        # Check if username is duplicated
        for user in usernames:
            if username in user[0]:
                return render_template("register.html", msg="User already exists. Please try another username.")

        # Add user and hash of password to database
        cursor.execute("""INSERT INTO users(username, password) VALUES (?,?)""", (username, generate_password_hash(password)))
        db.commit()

        session.clear()
        cursor.execute("""SELECT user_id FROM users WHERE username = ?""", (username,))
        id = cursor.fetchall()
        session["user_id"] = id[0][0]

        # Redirect user to home page
        return redirect("/")

    # GET request
    return render_template("register.html", msg="")

if __name__ == "__main__":
    app.run(debug=True)