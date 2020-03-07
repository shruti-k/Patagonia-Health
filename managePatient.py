import re

def add_patient(fname,lname,email,phy_id,cursor,db):
    query = """select * from patient where email = %s and physician_id = %s"""
    cursor.execute(query, (email,phy_id,))
    record = cursor.fetchone()
    if record:
        return False,"Email id is already used."
    if isValidName(fname) and isValidName(lname) and isValidEmail(email):
        query = "INSERT INTO patient (first_name,last_name,email,physician_id) VALUES (%s,%s,%s,%s)"
        values = (fname,lname,email,phy_id)
        cursor.execute(query,values)
        db.commit()
        return True, "Added successfully"
    else:
        return False, "Error in form!"

def get_patient(patient_id,phy_id,cursor):
    query = """select * from patient where patient_id = %s and physician_id = %s"""
    cursor.execute(query, (patient_id,phy_id,))
    record = cursor.fetchone()
    return record

def update_patient(fname,lname,email,patient_id,phy_id,cursor,db):
    query = """select * from patient where email = %s and patient_id <> %s"""
    cursor.execute(query, (email,patient_id,))
    record = cursor.fetchone()
    if record:
        return False, "Email id is already used."
    if isValidName(fname) and isValidName(lname) and isValidEmail(email):
        query = """UPDATE patient SET first_name = %s,last_name =%s,email = %s WHERE patient_id = %s and physician_id = %s"""
        values = (fname, lname, email,patient_id, phy_id)
        cursor.execute(query, values)
        db.commit()
        return True, "Updated successfully"
    else:
        return False, "Error in form!"

def delete_patient(patient_id,phy_id,cursor,db):
    query = """DELETE from patient where patient_id = %s and physician_id = %s"""
    print(patient_id)
    print(phy_id)
    values = (patient_id, phy_id)
    cursor.execute(query, values)
    db.commit()
    return True, "Deleted successfully"

def isValidName(name):
    print(name,bool(re.match("^[a-zA-Z]+[a-zA-Z ]*$",name)))
    return bool(re.match("^[a-zA-Z]+[a-zA-Z ]*$",name))

def isValidEmail(email):
    print(email,bool(re.match("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$", email)))
    return bool(re.match("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$", email))
