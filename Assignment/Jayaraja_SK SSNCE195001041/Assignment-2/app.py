import psycopg2

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect


conn = psycopg2.connect(database="crudapp", user="postgres", password="__enter_password__", host="127.0.0.1", port="5432")

app = Flask(__name__)


@app.route("/",methods=["GET","POST"])
def login():
    if(request.method=="GET"):
        return render_template("login.html", error=None)
    elif(request.method=="POST"):
        username = request.form["username"]
        password = request.form["password"]

        cursor = conn.cursor()

        query = f'select username from users where username = \'{username}\' and password = \'{password}\''
        cursor.execute(query)
        info = cursor.fetchone()

        if(info == None):
            return render_template("login.html", error="INVALID CREDENTIALS !!!")


        return render_template("home.html", name=username)


@app.route("/signup",methods=["GET","POST"])
def signup():
    if(request.method=="GET"):
        return render_template("signup.html", error=None, msg=None)
    elif(request.method=="POST"):
        username = request.form["username"]
        email = request.form["email"]
        roll_no = request.form["roll_no"]
        password = request.form["password"]

        cursor = conn.cursor()

        query = f'select email from users where email = \'{email}\''
        cursor.execute(query)
        rows = cursor.fetchall()

        if(len(rows)!=0):
            return render_template("signup.html", error="EMAIL ALREADY EXISTS !!!")


        query = f'select username from users where username = \'{username}\''
        cursor.execute(query)
        rows = cursor.fetchall()

        if(len(rows)!=0):
            return render_template("signup.html", error="USERNAME ALREADY EXISTS !!!")

        query = "insert into users values(%s, %s, %s, %s)"
        cursor.execute(query, (email, username, roll_no, password))
        conn.commit()

        return render_template("signup.html", error=None,msg="ACCOUNT CREATED SUCCESSFULLY !!! PLEASE LOGIN")



@app.route("/users",methods=["GET","POST"])
def users():
    if(request.method=="GET"):
        cursor = conn.cursor()

        query = f'select username, email, roll_no from users'
        cursor.execute(query)
        rows = cursor.fetchall()

        return render_template("users_list.html", users=rows)
    elif(request.method=="POST"):
        username = request.form["username"]
        email = request.form["email"]
        roll_no = request.form["roll_no"]
        password = request.form["password"]

        cursor = conn.cursor()

        query = f'select email from users where email = \'{email}\''
        cursor.execute(query)
        rows = cursor.fetchall()

        if(len(rows)!=0):
            return render_template("signup.html", error="EMAIL ALREADY EXISTS !!!")


        query = f'select username from users where username = \'{username}\''
        cursor.execute(query)
        rows = cursor.fetchall()

        if(len(rows)!=0):
            return render_template("signup.html", error="USERNAME ALREADY EXISTS !!!")

        query = "insert into users values(%s, %s, %s, %s)"
        cursor.execute(query, (email, username, roll_no, password))
        conn.commit()

        return render_template("signup.html", error=None,msg="ACCOUNT CREATED SUCCESSFULLY !!! PLEASE LOGIN")


@app.route("/user/<string:username>/update",methods=["GET","POST"])
def userUpdate(username):
    if(request.method=="GET"):
        cursor = conn.cursor()

        query = f'select username, email, roll_no from users where username = \'{username}\''
        cursor.execute(query)
        info = cursor.fetchone()

        return render_template("user_update.html",username=info[0],email=info[1],roll_no=info[2],error=None)
    elif(request.method=="POST"):
        new_username = request.form["username"]
        email = request.form["email"]
        roll_no = request.form["roll_no"]

        cursor = conn.cursor()

        query1 = f'select email from users where email = \'{email}\' and username <> \'{username}\''
        cursor.execute(query1)
        rows1 = cursor.fetchall()


        query2 = f'select username from users where username = \'{new_username}\' and username <> \'{username}\''
        cursor.execute(query2)
        rows2 = cursor.fetchall()


        if(len(rows1) == 0 and len(rows2) == 0):
            query = "update users set email=%s, username=%s, roll_no=%s where username=%s"
            cursor.execute(query, (email, new_username, roll_no, username))
            conn.commit()

        return redirect("/users")


@app.route("/user/<string:username>/delete")
def userDelete(username):
    cursor = conn.cursor()

    query = f'delete from users where username=\'{username}\''
    cursor.execute(query)
    conn.commit()

    return redirect("/users")



if __name__=="__main__":
    app.run()
    conn.close()
    
