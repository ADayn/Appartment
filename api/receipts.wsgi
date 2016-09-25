#!/home/albert/.pyenv/shims/python

# Turn on debug mode.
import cgitb
cgitb.enable()

# Connect to the database.
import pymysql

import os

def application(environ, start_response):
	# MySql connection
	# Get password:
	password = "";
	with open (environ["PASS_FILE"], "r") as passFile:
		password=passFile.read()

	conn = pymysql.connect(
		db = 'example',
		user = 'root',
		passwd = password,
		host = 'localhost')
	c = conn.cursor()

	# Insert some example data.
	# c.execute("INSERT INTO numbers VALUES (1, 'One!')")
	# c.execute("INSERT INTO numbers VALUES (2, 'Two!')")
	# c.execute("INSERT INTO numbers VALUES (3, 'Three!')")
	# conn.commit()

	# Print the contents of the database.
	# c.execute("SELECT * FROM numbers")

	output = "You made a " + environ["REQUEST_METHOD"] + " request!"

	status = '200 OK'
	response_headers = [('Content-type', 'text/plain'),
						('Content-Length', str(len(output)))]
	start_response(status, response_headers)

	return [output.encode('ascii')]