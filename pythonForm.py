#!/usr/bin/python
import cgi
import cgitb  # cgi with traceback error handling
#import mysql.connector as mydb
import pymysql as mydb  # Mysql 3x database driver
import re  # regular expressions

cgitb.enable()

print("Content-Type: text/html \n")  # required http response header (w/ extra line)

fn_error, ln_error, email_error = '', '', ''
brnd_error, makeup_error, opt_error, cc_error = '', '', '', ''
msg = ''

elements = cgi.FieldStorage()  # obtain the http parameters

firstname = elements.getvalue('firstname') or ""  # text field
lastname = elements.getvalue('lastname') or ""
email = elements.getvalue('email') or ""  # textarea
brand = elements.getvalue('brand') or ""
makeup = elements.getvalue('makeup') or ""  # could be a list
option1 = elements.getvalue('option1') or ""  # checkboxes
option2 = elements.getvalue('option2') or ""
option3 = elements.getvalue('option3') or ""
option4 = elements.getvalue('option4') or ""
creditCard = elements.getvalue('creditCard') or ""  # radio button

"""===================================================================================  
==================================================================================="""


def validate():  # function validate

    global fn_error, ln_error, email_error, brnd_error, makeup_error, opt_error, cc_error
    global msg

    if firstname == '': fn_error = '*'
    if lastname == '': ln_error = '*'
    if email == '': email_error = '*'
    if brand == '': brnd_error = '*'
    if makeup == '': makeup_error = '*'
    if option1 == '' and option2 == '' and option3 == '' and option4 == '': opt_error = '*'
    if creditCard == '': cc_error = '*'

    if fn_error or ln_error or email_error or brnd_error or makeup_error or opt_error or cc_error:
        msg = 'Please correct error fields above'


"""===================================================================================  
==================================================================================="""

def display():
    global fn_error, ln_error, email_error, brnd_error, makeup_error, opt_error, cc_error
    global msg

    print(F'''
        <!DOCTYPE html>
        <html>
        <head>
        <title>Avital gilburg's makeup form</title>
        <style>
            span   {{color:red}}
            select {{width:160px}}                                      
        </style>
        </head>
        <body bgcolor="lightpink">
        <h1><center>Avital gilburg's makeup form</center></h1>
        <form name="form1" method="POST" action=project.py>             

        <table>
            <tr><td><b>Enter First Name <span> {fn_error} </span>
                <td><input type="text" name="firstname" value="{firstname}">
            <tr><tr><td><b>Last Name <span> {ln_error} </span>
                <td><input type="text" name="lastname" value="{lastname}">
            <tr><td><b> Enter email <span> {email_error} </span>
                <td><input type="text" name="email" value="{email}">
    ''')
    print('<tr><td><b>Choose a Brand <span>' + brnd_error + '</span>')  
    print('<td><select name="brand">')
    print('<option value="">---choose from below---</option>')
    print('<option value="LO"', end='')
    if brand == 'LO': print('selected', end='')
    print('>Loreal </option>')
    print('<option value="MA"', end='')
    if brand == 'MA': print('selected', end='')
    print(">MAC</option>")
    print('<option value="NA"', end='')
    if brand == 'NA': print('selected', end='')
    print('>NARS</option>')
    print('<option value="EL"', end='')
    if brand == 'EL': print('selected', end='')
    print('>ELF</option>')
    print('<option value="NY"', end='')
    if brand == 'NY': print('selected', end='')
    print('>NYX</option>')
    print('<option value="MA"', end='')
    if brand == 'MA': print('selected', end='')
    print(">MAYBELLINE</option>")
    print('</select>')

    print('<tr><td><b>Makeup color <span>' + makeup_error + '</span>')  
    print('<td><select name="makeup" SIZE="4" multiple>')
    print('<option value="light"', end='')
    if 'light' in makeup: print('selected', end='')
    print('>light</option>')
    print('<option value="tan"', end='')
    if 'tan' in makeup: print('selected', end='')
    print('>tan</option>')
    print('<option value="golden"', end='')
    if 'golden' in makeup: print('selected', end='')
    print('>golden</option>')
    print('<option value="light brown"', end='')
    if 'light brown' in makeup: print('selected', end='')
    print('>light brown</option>')
    print('<option value="brown"', end='')
    if 'brown' in makeup: print('selected', end='')
    print('>brown</option>')
    print('<option value="cool"', end='')
    if 'cool' in makeup: print('selected', end='')
    print('>cool</option>')
    print('<option value="dark"', end='')
    if 'dark' in makeup: print('selected', end='')
    print('>dark</option>')
    print('</select>')

    print('<tr><td><b>Select texture <span>' + opt_error + '</span><td>')  
    print('<input type="checkbox" name="option1" value="liquid"', end='')
    if option1 != '': print('checked', end='')
    print('> liquid')
    print('<input type="checkbox" name="option2" value="powder"', end='')
    if option2 != '': print('checked', end='')
    print('> powder')
    print('<input type="checkbox" name="option3" value="silken"', end='')
    if option3 != '': print('checked', end='')
    print('> silken')
    print('<input type="checkbox" name="option4" value="jelly"', end='')
    if option4 != '': print('checked', end='')
    print('> jelly')

    print('<tr><td><b>Credit Card <span>' + cc_error + '</span><td>')  
    print('<input type="radio" name="creditCard" value="MC"', end='')
    if creditCard == 'MC': print('checked', end='')
    print('>   Master Card')
    print('<input type="radio" name="creditCard" value="VISA"', end='')
    if creditCard == 'VISA': print('checked', end='')
    print('> Visa')
    print('<input type="radio" name="creditCard" value="AMEX"', end='')
    if creditCard == 'AMEX': print('checked', end='')
    print('> American Express')
    print('<input type="radio" name="creditCard" value="DISC"', end='')
    if creditCard == 'DISC': print('checked', end='')
    print('> Discover')

    print('''
        <tr>
        <td width=140px>
        <tr>
        <td colspan=2>
        <input type="submit" value="  Place Order  "  >
        <input type="reset"  value="Cancel"           >
        </table>
    ''')

    print("<p style='color:red'>" + msg + '</p>')
    print("</form>")
    print("</body>")
    print("</html>")



def saveDB():  # save to database

    global msg

    if firstname == '': return

    makeups = makeup
    if type(makeup) is list:
        makeups = ','.join(makeup)  # join an array using commas

    options = ''
    if option1: options += option1 + ','  # join all the values for options
    if option2: options += option2 + ','
    if option3: options += option3 + ','
    if option4: options += option4 + ','
    options = re.sub(r",$", "", options)  # strip off the last comma for the array

    sql = "INSERT INTO avital_gilburg "
    sql += "VALUES('" + firstname + "','" + lastname + "','" + email + "'"
    sql += ",'" + brand + "','" + makeups + "','" + options + "','" + creditCard + "')"

    try:
        conn = mydb.connect(host='localhost', user='gilburg', password='gilburg', database='gilburg')  # connect to host

        cursor = conn.cursor()  # create a cursor

        cursor.execute(sql);  # execute the sql

        conn.commit()

    except mydb.OperationalError as e:
        errorNum = e.args[0]
        errorMsg = e.args[1]
        msg = 'Database Error - ' + str(errorNum) + errorMsg

    msg = "Your order has been saved successfully";

    cursor.close()
    conn.close()


"""===================================================================================
==================================================================================="""

if elements: validate()  # if something was entered call validate
if msg == '': saveDB()  # if no errors, save in database
display()

