from flask import Flask
from flask import render_template
from flask import request



app = Flask(__name__)


@app.route("/",methods=["GET","POST"])
def Form():
    if(request.method=="GET"):
        return render_template("form.html")
    elif(request.method=="POST"):
        username=request.form["username"]
        email=request.form["email"]
        mobile_no=request.form["mobile_no"]
        

        return render_template("response.html",username=username,email=email,mobile_no=mobile_no)


if __name__=="__main__":
    app.run()
    
