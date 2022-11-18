from flask import *

from datetime import date
import ibm_db
import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content
app=Flask(__name__)
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=2f3279a5-73d1-4859-88f0-a6c3e6b4b907.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30756;SECURITY=SSL;SSLServerCertificate:DigiCertGlobalRootCA;PROTOCOL=TCPIP;UID=rch34173;PWD=MwsEJWWZqnmoeUkt;", "", "")
# conn=None
# conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=125f9f61-9715-46f9-9399-c8177b21803b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30426;SECURITY=SSL;SSLServerCertificate:DigiCertGlobalRootCA;PROTOCOL=TCPIP;UID=ynl77900;PWD=N0YoPruXMu0a6OeR;", "", "")

@app.route("/", methods=['GET'])
def login():
    if request.method=='GET'  :
        resp=make_response(render_template('Login/index.html'))
        resp.set_cookie('userID',"",expires=0)
        return resp
    return render_template("Login/index.html",status="",colour="red")

@app.route("/signup", methods=['GET','POST'])
def signup():
    if request.method=='GET' :
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

@app.route("/", methods=['POST'])
def setcookie():
    if request.method=='POST':
        email=request.form["email"]
        password=request.form["password"]
        query = '''select * from retailers where email = \'{}\''''.format(email)
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        if(row is not False):
            if(row['PASSWORD'] != password):
                return render_template("Login/index.html",status="Invalid Password",colour="red")
            else:
                resp=make_response(render_template('Dashboard/index.html'))
                resp.set_cookie('userID',str(row['RETAILER_ID']))
                return resp

        return render_template("Login/index.html",status="Invalid Email",colour="red")

# @app.route("/ ", methods=['GET'])
# def delete_cookie():
#     if request.method=='GET':
        
    


@app.route("/dashboard", methods=['GET','POST'])
def dashboard():
    if request.method=="GET" and request.cookies.get('userID')!=None:
        return render_template("Dashboard/index.html")

@app.route("/add_customer", methods=['GET','POST'])
def add_customer():
    if request.method=="GET" and request.cookies.get('userID')!=None:
        return render_template("Dashboard/add_customer.html")
    elif request.method=="POST" and request.cookies.get('userID')!=None:
        name=request.form["name"]
        retailer_id=request.cookies.get('userID')
        id=int(request.form["id"])
        query = '''select * from customer where customer_id = \'{}\' and retailer_id=\'{}\''''.format(id,retailer_id)
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        retailer_id=request.cookies.get('userID')
        if(row is False):
            query = '''insert into customer(customer_id,retailer_id,customer_name) values('{}', '{}', '{}')'''.format(id,retailer_id,name)
            exec_query = ibm_db.exec_immediate(conn, query)
            return render_template("Dashboard/add_customer.html",status="Customer Added",colour="green")
        else:
            return render_template("Dashboard/add_customer.html",status="Customer Already Exists",colour="red")

@app.route("/view_customer", methods=['GET','POST'])
def view_customer():
    if request.method=="GET" and request.cookies.get('userID')!=None:
        
        ret_id=request.cookies.get('userID')
        query = '''select * from customer where retailer_id=\'{}\''''.format(ret_id)

        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        name=[]
        id=[]
        while(row):
            name.append(row["CUSTOMER_NAME"])
            id.append(row["CUSTOMER_ID"])
            row = ibm_db.fetch_both(exec_query)
        return render_template("Dashboard/view_customer.html",name=name,id=id,len=len(name))
        
@app.route("/add_item", methods=['GET','POST'])
def add_item():
    if request.method=="GET" and request.cookies.get('userID')!=None:
        return render_template("Dashboard/add_item.html")
    elif request.method=="POST" and request.cookies.get('userID')!=None:
        name=request.form["name"]
        price=float(request.form["price"])
        query = '''select * from items where item_name = \'{}\''''.format(name)
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        retailer_id=request.cookies.get('userID')
        if(row is False):
            query = '''insert into items(retailer_id,item_name,price,left_out) values('{}', '{}', '{}', '{}')'''.format(retailer_id,name,price,0)
            exec_query = ibm_db.exec_immediate(conn, query)
            return render_template("Dashboard/add_item.html",status="Item Added",colour="green")
        else:
            return render_template("Dashboard/add_item.html",status="Item Already Exists",colour="red")

@app.route("/view_item", methods=['GET','POST'])
def view_item():
    if request.method=="GET" and request.cookies.get('userID')!=None:
        ret_id=request.cookies.get('userID')
        query = '''select * from items where retailer_id=\'{}\''''.format(ret_id)
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        name=[]
        id=[]
        price=[]
        left_out=[]
        while(row):
            name.append(row["ITEM_NAME"])
            id.append(row["ITEM_ID"])
            price.append(row["PRICE"])
            left_out.append(row["LEFT_OUT"])
            row = ibm_db.fetch_both(exec_query)
        return render_template("Dashboard/view_item.html",name=name,id=id,price=price,left_out=left_out,len=len(name))

@app.route("/add_inventory", methods=['GET','POST'])
def add_inventory():
    name=[]
    retailer_id=request.cookies.get('userID')
    query = '''select * from items where retailer_id=\'{}\''''.format(retailer_id)
    exec_query = ibm_db.exec_immediate(conn, query)
    row = ibm_db.fetch_both(exec_query)
    while(row):
        name.append(row["ITEM_NAME"])
        row = ibm_db.fetch_both(exec_query)
    if request.method=="GET" and request.cookies.get('userID')!=None:
        return render_template("Dashboard/add_inventory.html",name=name,len=len(name),status=" ")
    elif request.method=="POST" and request.cookies.get('userID')!=None:
        fname=request.form["name"]
        quantity=request.form["quantity"]
        stock_date=date.today()
        # Finding ITEM ID
        ret_id=request.cookies.get('userID')
        query = '''select item_id from items where item_name = \'{}\' and retailer_id=\'{}\''''.format(fname,ret_id)
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        id=row["ITEM_ID"]
        # INSERTION
        query = '''insert into inventory(item_id,quantity,stock_date) values('{}', '{}', '{}')'''.format(id,quantity,stock_date)
        exec_query = ibm_db.exec_immediate(conn, query)
        #UPDATION
        query = '''update items set left_out=left_out+\'{}\' where item_id=\'{}\''''.format(quantity,id)
        exec_query = ibm_db.exec_immediate(conn, query)
        return render_template("Dashboard/add_inventory.html",name=name,len=len(name),status="Inventory added")

@app.route("/view_inventory", methods=['GET','POST'])
def view_inventory():
    name=[]
    retailer_id=request.cookies.get('userID')
    query = '''select * from items where retailer_id=\'{}\''''.format(retailer_id)
    exec_query = ibm_db.exec_immediate(conn, query)
    row = ibm_db.fetch_both(exec_query)
    while(row):
        name.append(row["ITEM_NAME"])
        row = ibm_db.fetch_both(exec_query)
    items=list()
    if request.method=="GET" and request.cookies.get('userID')!=None:
        return render_template("Dashboard/view_inventory.html",name=name,items=items)
    elif request.method=="POST" and request.cookies.get('userID')!=None:
        item_name=request.form["name"]
        start=request.form["start_date"]
        end=request.form["end_date"]
        query = '''select item_id from items where item_name = \'{}\''''.format(item_name)
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        id=row["ITEM_ID"]
        query = '''select stock_date,quantity from inventory where item_id=\'{}\' and stock_date<=\'{}\' and stock_date>=\'{}\''''.format(id,end,start)
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        while(row):
            items.append({"item_name":item_name,"quantity":row[1],"stock_date":row[0]})
            row = ibm_db.fetch_both(exec_query)
        return render_template("Dashboard/view_inventory.html",name=name,items=items)

@app.route("/add_sale", methods=['GET','POST'])
def add_sale():
    # ITEMS
    items=list()
    ret_id=request.cookies.get('userID')
    query = '''select * from items where retailer_id=\'{}\''''.format(ret_id)
    exec_query = ibm_db.exec_immediate(conn, query)
    row = ibm_db.fetch_both(exec_query)
    while(row):
        items.append({"name": row["ITEM_NAME"], "quantity": row["LEFT_OUT"], "price": row["PRICE"]})
        row = ibm_db.fetch_both(exec_query)
    # CUSTOMERS
    custname=list()
    ret_id=request.cookies.get('userID')
    query = '''select * from customer where retailer_id=\'{}\''''.format(ret_id)
    exec_query = ibm_db.exec_immediate(conn, query)
    row = ibm_db.fetch_both(exec_query)
    while(row):
        custname.append({"name":row["CUSTOMER_NAME"],"id":row["CUSTOMER_ID"]})
        row = ibm_db.fetch_both(exec_query)
    if request.method=="GET" and request.cookies.get('userID')!=None:
        return render_template("Dashboard/add_sale.html",items=items,cname=custname,status="")
    elif request.method=="POST" and request.cookies.get('userID')!=None:
        i_array=request.form["item_array"]
        q_array=request.form["quantity_array"]
        item_list=i_array.split(",")
        quantity_list=q_array.split(",")
        cname=request.form["cname"]
        today = date.today()
        # FINDING CUSTOMER ID
        query = '''select customer_id from customer where customer_name = \'{}\''''.format(cname)
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        id=row["CUSTOMER_ID"]
        #SALE TABLE
        query = '''insert into sale(sale_date,customer_id) values('{}', '{}')'''.format(today,id)
        print(id)
        exec_query = ibm_db.exec_immediate(conn, query)
        #GET SALE ID
        query = '''select sale_id from sale where sale_date = \'{}\' and customer_id=\'{}\''''.format(today,id)
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        sale_id=row["SALE_ID"]
        #SALE ITEM TABLE
        n=len(item_list)
        print(item_list,n)
        for i in range(n):
            query = '''select item_id from items where item_name = \'{}\''''.format(item_list[i])
            exec_query = ibm_db.exec_immediate(conn, query)
            row = ibm_db.fetch_both(exec_query)
            item_id=row["ITEM_ID"]
            #UPDATION
            query = '''update items set left_out=left_out-\'{}\' where item_id=\'{}\''''.format(quantity_list[i],item_id)
            exec_query = ibm_db.exec_immediate(conn, query)
            #MAIL
            products=list()
            ret_id=request.cookies.get('userID')
            query = '''select item_name,left_out from items where left_out<5 and retailer_id=\'{}\''''.format(ret_id)
            exec_query = ibm_db.exec_immediate(conn, query)
            row = ibm_db.fetch_both(exec_query)
            while(row):
                print(row)
                products.append({"name":row["ITEM_NAME"],"quantity":row["LEFT_OUT"]})
                row = ibm_db.fetch_both(exec_query)
            retailer_id=request.cookies.get('userID')
            query = '''select email from retailers where retailer_id=\'{}\''''.format(retailer_id)
            exec_query = ibm_db.exec_immediate(conn, query)
            row = ibm_db.fetch_both(exec_query)
            retailer_email=row["EMAIL"]
            print(retailer_email)
            stock_alert_mail(retailer_email, products)
            # INSERTION
            query = '''insert into sale_items(sale_id,quantity,item_id) values('{}', '{}', '{}')'''.format(sale_id,quantity_list[i],item_id)
            exec_query = ibm_db.exec_immediate(conn, query)
        return render_template("Dashboard/add_sale.html",items=items,cname=custname,status="Sale Success")


@app.route("/view_sale", methods=['GET','POST'])
def view_sale():
    items=list()
    if request.method=="GET" and request.cookies.get('userID')!=None:
        return render_template("Dashboard/view_sale.html",items=items)
    elif request.method=="POST" and request.cookies.get('userID')!=None:
        start=request.form["start_date"]
        end=request.form["end_date"]
        query = '''select item_id,sum(quantity) from sale_items where sale_id in (select sale_id from sale where sale_date<= \'{}\' and sale_date>=\'{}\') group by(item_id) order by sum(quantity) desc'''.format(end,start)
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        while(row):
            ret_id=request.cookies.get('userID')
            query1 = '''select item_name,price from items where item_id=\'{}\' and retailer_id=\'{}\''''.format(row[0],ret_id)
            exec_query1 = ibm_db.exec_immediate(conn, query1)
            row1 = ibm_db.fetch_both(exec_query1)
            if(row1):
                items.append({"item_id":row[0],"item_name":row1[0],"quantity":row[1],"amount":(row1[1]*row[1])})
            row = ibm_db.fetch_both(exec_query)
        # Item Name and Price
        return render_template("Dashboard/view_sale.html",items=items)

def stock_alert_mail(to_email, products):
    sg = sendgrid.SendGridAPIClient(api_key='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')
    from_email = Email("karthik19046@cse.ssn.edu.in")
    
    to_email = To(to_email)
    
    subject = "Stock Alert !!! - Inventory Management System"

    msg = '''
    <html>

    <body>
        <p>Dear Customer,</p>

        <p>We kindly request you to refill the items listed below as they're falling shortage in quantity.</p>

        <table style='border: 1px solid black; border-collapse: collapse;'>

        <tr>
            <td style="font-weight: bold; padding: 5px 10px 5px 10px; border: 1px solid black;">ITEM NAME</td>
            <td style="font-weight: bold; padding: 5px 10px 5px 10px; border: 1px solid black;">QUANTITY LEFT</td>
        </tr>
    '''

    for i in products:
        msg += "<tr>"

        msg += f'<td style="padding: 5px 10px 5px 10px; border: 1px solid black;">{i["name"]}</td>'
        msg += f'<td style="padding: 5px 10px 5px 10px; border: 1px solid black;">{i["quantity"]}</td>'
        

        msg += "</tr>"

    msg += '''
    </table>
    
    <body>
    
    </html>
    '''
    
    content = Content("text/html", msg)
    
    mail = Mail(from_email, to_email, subject, content)
    mail_json = mail.get()
    response = sg.client.mail.send.post(request_body=mail_json)
    
    print(response.status_code)
    print(response.headers)

if __name__=="__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)