# Connect to the database.
import pymysql
import json

def application(environ, start_response):
	# MySql connection
	# Get password:
	password = ""
	with open (environ["PASS_FILE"], "r") as passFile:
		password=passFile.read()
	conn = pymysql.connect(
		db = 'appartment',
		user = 'root',
		passwd = password,
		host = 'localhost'
	)
	c = conn.cursor()

	method = environ["REQUEST_METHOD"]
	
	if method == "POST":
		name = ""
		try:
			length = int(environ.get('CONTENT_LENGTH', '0'))
			status = '200 OK'
		except ValueError:
			length = 0
			status = '422 Unprocessable Entity'
		if length != 0:
			name = environ['wsgi.input'].read(length).decode("utf-8")
		if name:
			try:
				c.execute("INSERT INTO Users SET name = %s", (name))
				conn.commit()
				c.execute("SELECT * FROM Users")
				output = str(c.fetchall())
			except Exception as e:
				output = "Oops, that name already exists! Try again."
				status = "400 Bad Request"
	
	elif method == "DELETE":
		name = ""
		try:
			length = int(environ.get('CONTENT_LENGTH', '0'))
			status = '200 OK'
		except ValueError:
			length = 0
			status = '422 Unprocessable Entity'
		if length != 0:
			name = environ['wsgi.input'].read(length).decode("utf-8")
		if name:
			c.execute("DELETE FROM Users WHERE name = %s", (name))
			conn.commit()
			c.execute("SELECT * FROM Users")
			output = str(c.fetchall())
	else:
		status = '400 Bad Request'
		output = "request: " + method

	response_headers = [('Content-type', 'text/plain'),
	                    ('Content-Length', str(len(output)))]

	start_response(status, response_headers)

	return [output.encode('ascii'), output.encode('ascii')]
