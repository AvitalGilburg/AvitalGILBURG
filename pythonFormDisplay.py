#!/usr/bin/python
print("Content-type: text/html \n")

import pymysql

# Connect to the database
conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='gilburg',
    password='gilburg',
    database='gilburg'
)

# Create a cursor object
cursor = conn.cursor()

# Execute the SQL query to retrieve the data
query = "SELECT * FROM avital_gilburg"
cursor.execute(query)

# Fetch all the rows
rows = cursor.fetchall()

# Close the cursor and connection to the database
cursor.close()
conn.close()

# Create an HTML page to display the data
html = '<!DOCTYPE html>\n'
html += '<html>\n'
html += '<head>\n'
html += '<title>Avital Gilurg\'s Makeup Form Data</title>\n'
html += '</head>\n'
html += '<body bgcolor="lightpink">\n'
html += '<h1>Avital Gilurg\'s Makeup Form Data</h1>\n'
html += '<table border="1">\n'
html += '<tr><th>First Name</th><th>Last Name</th><th>Email</th><th>brand</th><th>Makeup color</th><th>texture</th><th>credit card</th></tr>\n'
for row in rows:
    html += '<tr>'
    for column in row:
        html += '<td>' + str(column) + '</td>'
    html += '</tr>\n'
html += '</table>\n'
html += '</body>\n'
html += '</html>\n'

# Display the HTML page
print(html)
