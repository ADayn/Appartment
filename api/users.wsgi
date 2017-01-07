# Connect to the database.
import pymysql
import json

def application(environ, start_response):
	try:
		length = int(environ.get("CONTENT_LENGTH", "0"))
		status = "200 OK"
	except ValueError:
		length = 0
		status = "422 Unprocessable Entity"
	# Read password from file 
	password = ""
	with open (environ["PASS_FILE"], "r") as passFile:
		password=passFile.read()
	# Connect to the database
	connection = pymysql.connect(
		db = "appartment",
		user = "root",
		password = password,
		host = "localhost",
		autocommit = True,
		cursorclass=pymysql.cursors.DictCursor
	)

	with connection.cursor() as cursor:
		method = environ["REQUEST_METHOD"]
		name = environ["wsgi.input"].read(length).decode("utf-8") if length > 0 else ""
		if method == "GET":
			cursor.execute("SELECT * FROM Users")
			output = json.dumps(cursor.fetchall())
		elif method == "POST":
			if name:
				try:
					cursor.execute("INSERT INTO Users SET name = %s", (name))
					cursor.execute("SELECT * FROM Users")
					output = json.dumps(cursor.fetchall())
				except Exception as e:
					output = "Oops, that name already exists! Try again."
					status = "400 Bad Request"
		elif method == "DELETE":
			if name:
				cursor.execute("DELETE FROM Users WHERE name = %s", (name))
				cursor.execute("SELECT * FROM Users")
				output = json.dumps(cursor.fetchall())
		else:
			status = "405 Method Not Allowed"
			output = json.dumps({
				"request": method,
				"allowed": [
					"GET",
					"POST",
					"DELETE"
				]
			})



	response_headers = [("Content-type", "text/plain"),
	                    ("Content-Length", str(len(output)))]
	start_response(status, response_headers)
	return [output.encode("ascii"), output.encode("ascii")]
