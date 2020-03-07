import re
def verify_login(username,password,cursor,db):
    query = """select physician_id from physician where email = %s and password = %s"""
    cursor.execute(query, (username,password,))
    record = cursor.fetchone()
    if record:
        return record,True
    else:
        return False

def verify_signup(fname,lname,email,password,cpassword,cursor,db):
    query = """select * from physician where email = %s"""
    cursor.execute(query, (email,))
    record = cursor.fetchone()
    if record:
        return False,"Username already exists!"
    if isValidName(fname) and isValidName(lname) and isValidEmail(email) and isValidPassword(password) and password==cpassword:
        query = "INSERT INTO physician (first_name,last_name,email,password) VALUES (%s,%s,%s,%s)"
        values = (fname,lname,email,password)
        cursor.execute(query,values)
        db.commit()
        return True, "Added successfully"
    else:
        return False, "Error in form!"

def get_physician_data(physician_id,cursor):
    query = """select first_name,last_name from physician where physician_id = %s"""
    cursor.execute(query, (physician_id,))
    record = cursor.fetchone()
    return record

def isValidName(name):
    return bool(re.match("^[a-zA-Z]+[a-zA-Z ]*$",name))

def isValidPassword(password):
    return bool(re.match("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{6,}$", password))

def isValidEmail(email):
    return bool(re.match("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$", email))

def get_physician_patients(phy_id,cursor):
    query = """select first_name,last_name,email,patient_id from patient where physician_id = %s"""
    cursor.execute(query, (phy_id,))
    record = cursor.fetchall()
    return record