from flask import Flask, request, render_template,redirect,url_for
import mysql.connector as mysql
from managePhysician import *
from managePatient import *
db = mysql.connect(
    host = "sskangle.mysql.pythonanywhere-services.com",
    user = "sskangle",
    passwd = "patagonia",
    database = "sskangle$patagonia",
    auth_plugin='mysql_native_password'
)
app = Flask(__name__,template_folder='.')
cursor = db.cursor()
physician_id = None
@app.route("/")
def landingpage():
    return render_template('physicianLoginPage.html')

@app.route('/login',methods = ['GET','POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    response = verify_login(username,password,cursor,db)
    global physician_id
    physician_id = response[0][0]
    if response[1]:
        return redirect(url_for('physician_dashboard'))
    else:
        return render_template('physicianLoginPage.html',msg="Please enter valid credentials!")

@app.route('/physician_dashboard')
def physician_dashboard():
    patient_list = get_physician_patients(physician_id,cursor)
    physician_data = get_physician_data(physician_id,cursor)
    return render_template('physicianDashboard.html',patients=patient_list,physician_name = physician_data[0]+" "+physician_data[1])

@app.route('/register_physician')
def register_physician():
    return render_template('registerPhysician.html')

@app.route('/add_physician',methods = ['GET','POST'])
def add_physician():
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    password = request.form['password']
    cpassword = request.form['cpassword']
    response = verify_signup(fname,lname,email,password,cpassword,cursor,db)
    if response[0]:
        return render_template('physicianLoginPage.html',signup_success_msg="Account created successfully. Login to view your account.")
    else:
        return render_template('physicianDashboard.html',error_msg=response[1])


@app.route('/add_patient',methods = ['GET','POST'])
def register_patient():
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    response = add_patient(fname,lname,email,physician_id,cursor,db)
    if response[0]:
        return redirect(url_for('physician_dashboard'))
    else:
        patient_list = get_physician_patients(physician_id, cursor)
        physician_data = get_physician_data(physician_id, cursor)
        return render_template('physicianDashboard.html', patients=patient_list,
                               physician_name=physician_data[0] + " " + physician_data[1],error_msg=response[1])


@app.route('/delete_patient/<patient_id>')
def delete_patients(patient_id):
   print("patient id---***",patient_id,physician_id)
   response = delete_patient(patient_id,physician_id,cursor,db)
   if response[0]:
        return redirect(url_for('physician_dashboard'))

@app.route('/update_patient/<patient_id>',methods = ['GET','POST'])
def update_patients(patient_id):
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    response = update_patient(fname,lname,email,patient_id,physician_id,cursor,db)
    print(response)
    if response[0]:
        return redirect(url_for('physician_dashboard'))
    else:
        return render_template('editPatient.html', pid=patient_id,fname=fname,lname=lname,email=email,error_msg=response[1])

@app.route('/edit_patient/<patient_id>')
def edit_patients(patient_id):
    patient_data = get_patient(patient_id,physician_id,cursor)
    return render_template('editPatient.html', pid=patient_data[0],fname=patient_data[2],lname=patient_data[3],email=patient_data[4])

@app.route('/logout')
def logout():
    global physician_id
    physician_id = None
    return render_template('physicianLoginPage.html')

if __name__ == "__main__":
    app.run()

