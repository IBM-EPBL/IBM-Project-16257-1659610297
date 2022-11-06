from flask import *
import ibm_db
app=Flask(__name__)
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=125f9f61-9715-46f9-9399-c8177b21803b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30426;SECURITY=SSL;SSLServerCertificate:DigiCertGlobalRootCA;PROTOCOL=TCPIP;UID=ynl77900;PWD=N0YoPruXMu0a6OeR;", "", "")
@app.route("/", methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template("Login/index.html",status="",colour="red")
    elif request.method=='POST':
        email=request.form["email"]
        password=request.form["password"]
        query = '''select * from retailers where email = \'{}\''''.format(email)
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        if(row is not False):
            print(row)
            if(row['PASSWORD'] != password):
                return render_template("Login/index.html",status="Invalid Password",colour="red")
            else:
                return render_template("Dashboard/index.html")

        return render_template("Login/index.html",status="Invalid Email",colour="red")

@app.route("/signup", methods=['GET','POST'])
def signup():
    if request.method=='GET':
        return render_template("Login/signup.html",status="",colour="red")
    elif request.method=='POST':
        email=request.form["email"]
        password=request.form["password"]
        first_name=request.form["first_name"]
        last_name=request.form["last_name"]
        store_name=request.form["store_name"]
        address=request.form["address"]
        phone_number=request.form["phone_number"]
        query = '''select * from retailers where email = \'{}\''''.format(email)
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        if(row is False):
            query = '''insert into retailers(email, password, first_name, last_name, store_name, address, phone_number) values('{}', '{}', '{}', '{}', '{}', '{}', '{}')'''.format(email, password, first_name, last_name, store_name, address, phone_number)
            exec_query = ibm_db.exec_immediate(conn, query)
            return render_template("Login/signup.html",status="Signup Success",colour="green")
        else:
            return render_template("Login/signup.html",status="User Already Exists",colour="red")

@app.route("/dashboard", methods=['GET','POST'])
def dashboard():
    if request.method=="GET":
        return render_template("Dashboard/index.html")

@app.route("/forms", methods=['GET','POST'])
def forms():
    if request.method=="GET":
        return render_template("Dashboard/forms.html")
    elif request.method=="POST":
        name=request.form["name"]
        fname=request.form["fname"]
        lname=request.form["lname"]
        sname=request.form["sname"]
        print(name)
        return redirect(url_for("tables"))
        # return render_template("Dashboard/tables.html",name=name,fname=fname,lname=lname,sname=sname)

@app.route("/tables", methods=['GET','POST'])
def tables():
    if request.method=="GET":
        return render_template("Dashboard/tables.html")

if __name__=="__main__":
    app.run()