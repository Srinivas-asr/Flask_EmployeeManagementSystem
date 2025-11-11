from datetime import timedelta
from flask import Flask,render_template,request,jsonify, session,redirect
import mysql.connector


app=Flask(__name__)

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    database="flask",
    password="Srinivas"
)


@app.route('/')
def Home():
    image = 'img.png'
    return render_template('home.html', image=image)
@app.route('/about')
def About():
    return render_template('about.html')
@app.route('/register')
def Register():
    return render_template('register.html')

@app.route('/login')
def Login():
    return render_template('login.html')

@app.route('/dashboard')
def Dashboard():
    return render_template('dashboard.html')


@app.route("/adminlogin1", methods=["GET", "POST"])
def InUserLogin():
    return render_template("adminlogin.html")


app.secret_key = "asr123"
app.permanent_session_lifetime = timedelta(minutes=1)

USER = {"username": "asr", "password": "123"}

@app.route("/adminlogin", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if username == USER["username"] and password == USER["password"]:
            session.permanent = True
            session['username'] = username
            return redirect("/getdata")
        else:
            return "Invalid Credentials. Try Again!"

    return redirect("/adminlogin")


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect("/")

@app.route('/insert', methods=["POST"])
def Insert():
    id=request.form['id']
    name=request.form['name']
    age=request.form['age']
    gender=request.form.get('gender')
    dob=request.form['dob']
    department=request.form['department']
    salary=request.form['salary']
    password=request.form['password']
    cpassword=request.form['cpassword']
    if password==cpassword:
        cursor=mydb.cursor()
        cursor.execute("insert into employee values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(id,name,age,gender,dob,department,salary,password,cpassword))
        mydb.commit()
        cursor.close()
        return f"details inserted successfully,<a href='/'><button>Home</button></a> <a href='/register'><button>Register Data</button></a>"
    return f"details don't inserted,<a href='/'><button>Home</button></a> <a href='/register'><button>Register Data</button></a><a href='/getdata'><button>Dashboard</button></a>"
    

@app.route('/getdata', methods=['GET'])
def GetData():
    cursor=mydb.cursor(dictionary=True)
    cursor.execute("select * from employee")
    data=cursor.fetchall()
    cursor.close()
    if 'username' in session:
        return render_template('dashboard.html',data=data)
    else:
        return redirect("/adminlogin1")


@app.route('/loginbyid', methods=["POST"])
def LoginById():
    id=request.form['id']
    password=request.form['password']
    cursor=mydb.cursor()
    cursor.execute("select password from employee where id=%s",(id,))
    result=cursor.fetchone()
    cursor.close()
    # return f"{password} {result[0]}"

    
    if result and result[0]==password:
        cursor=mydb.cursor(dictionary=True)
        cursor.execute("select * from employee where id=%s",(id,))
        user=cursor.fetchall()
        cursor.close()
        # return f"{user}"
        return render_template('userdashboard.html',user=user)
    elif not result:
        
        return f"id does not exist"
    else:
        return f"incorrect password"
    

@app.route('/deletebyid/<int:id>')
def DeleteByID(id):
    cursor=mydb.cursor()
    cursor.execute("delete from employee where id=%s",(id,))
    mydb.commit()
    cursor.close()
    return f"user {id} deleted sucessfully, <a href='/getdata'><button>View registered Data</button></a>"


@app.route('/updatebyid/<int:id>')
def UpdateById(id):
    cursor=mydb.cursor()
    cursor.execute("select * from employee where id=%s",(id,))
    result=cursor.fetchone()
    cursor.close()
    if result:
        return render_template('update.html',data=result)
    else:
        return f"no data found"


@app.route('/updateuser', methods=['POST'])
def UpdateUser():
    
    id=request.form['id']
    name=request.form['name']
    age=request.form['age']
    gender=request.form.get('gender')
    dob=request.form['dob']
    department=request.form['department']
    salary=request.form['salary']
    
    cursor=mydb.cursor()
    cursor.execute("update employee set name=%s,age=%s,gender=%s,dob=%s,department=%s,salary=%s where id=%s",(name,age,gender,dob,department,salary,id))
    mydb.commit()
    cursor.close()
    return f"details updated successfully,<a href='/getdata'><button>View registered Data</button></a> <a href='/register'><button>Register Data</button></a>"
    


if __name__=='__main__':
    app.run(debug=True)
