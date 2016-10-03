# Appartment

The App(artment) will be a webapp that keeps track of receipts, shared expenses, cooking schedules, and chores. Once the basic features are completed, work will start on image recognition so that receipts can be scanned instead of entered manually. It is based on a Python backend that talks directly to a wsgi server (without the need of a framework like Django), an SQL database, and a javascript front end. The server this will be developed for is Apache 2 with [mod_wsgi](https://modwsgi.readthedocs.io/en/develop/) as the wsgi link. Although neither the backend nor the frontend are setup yet, you can setup the server for it as follows:

### Setup
`$` Represents commands to run in terminal
`$$` represents commands in a program's own command line environment

Pick a location to pull this repo to. This will be refered to as `{APP_HOME}`.

1. Python

  -	Install [pyenv](https://github.com/yyuu/pyenv#basic-github-checkout)
  ```shell
$	git clone https://github.com/yyuu/pyenv.git ~/.pyenv
$	echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
$	echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
$	echo 'eval "$(pyenv init -)"' >> ~/.bashrc
$	exec $SHELL
 ```
  -	Install Python3
  ```shell
$	sudo apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils
$	env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.5.2
$	pyenv global 3.5.2
```
  -	Install pip3
  ```shell
$	sudo apt install python3-pip
```

2. MySQL

  -	Install MySQL
  ```shell
$	sudo apt install mysql-server
```
  -	Pick a password

  -	Setup MySQL
  ```shell
$	mysql_secure_installation
```
  -	Follow prompts

  -	Install PyMySql
  ```shell
$	pip3 install pymysql
```
  -	Create the database
  ```shell
$	mysql -u root -p
```
  ```SQL
$$	CREATE DATABASE example;
$$	USE example;
$$	CREATE TABLE numbers (num INT, word VARCHAR(20));
```
  -	ctrl-D to exit
  
3. Apache

  -	[Install Apache](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-apache-mysql-and-python-lamp-server-without-frameworks-on-ubuntu-14-04)
  ```shell
$	sudo apt install apache2
$	sudo apt install apache2-dev
```
  -	Find where the apache configuration files are (folder with "apache2.conf" or "httpd.conf")
  ```shell
$	sudo find / -name 'apache2.conf' 2>/dev/null
```
  -	In my case this is "/etc/apache2/", it will be refered to as `{APACHE_HOME}`
  -	Write down this location

  -	[Install mod_wsgi](http://modwsgi.readthedocs.io/en/develop/user-guides/quick-installation-guide.html)
  - Download the source tar ball from link above
  -	Replace X.Y with actual version number in the next commands
  ```shell
$	tar xvfz mod_wsgi-X.Y.tar.gz
$	cd mod_wsgi_X.Y
$	./configure
$	make
```
  -	If make failed reinstall python with the PYTHON_CONFIGURE_OPTS env set as seen in the Install Python section (for pyenv)
  ```shell
$	sudo make install
```
  -	Load mod_wsgi
  -	Find where mods are stored by looking at any file that ends in ".load" in the /etc/apache2/mods-available/ directory
  -	It will have a line that looks like "LoadModule status_module /usr/lib/apache2/modules/mod_status.so"
  ```shell
$	sudo touch {APACHE_HOME}/mods-available/wsgi.load
```
  -	Add the following line to this new file, using the path to the ".so" file found from the other .load file:
  ```
	LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so
  WSGIPythonHome /home/albert/.pyenv/versions/3.5.2
```
  -	Enable the module
  ```shell
$	sudo a2enmod wsgi
```
  -	Restart the server and check the error log (/var/log/apache2/error.log for me) for the line "Apache/2.4.8 (Unix) mod_wsgi/4.4.21 Python/2.7 configured"
  ```shell
$	service apache2 restart
```
  -	Clean up, clean up, everybody everywhere!
  ```shell
$	make clean
```
  -	Configure Apache
  ```shell
$	sudo nano {APACHE_HOME}/sites-available/000-default.conf
```
  -	This is the config file for the server that is running on port 80
  -	Add the following on the line right after the `<VirtualHost *:80>`line.
  ```
	SetEnv PASS_FILE /path/to/mysql/password/file
  
	<Directory {APP_HOME}/public>
		Require all granted
	</Directory>

	<Directory {APP_HOME}/api>
		Require all granted
	</Directory>

	WSGIScriptAlias /api/receipts {APP_HOME}/api/receipts.wsgi
```
  -	Change the line with `Document root` so that it looks like:
  ```
  DocumentRoot {APP_HOME}/public
 ```
  - Phew, done! Now we can restart Apache one last time and test it out:
  ```shell
$	service apache2 restart
```
  - If you go to http://localhost on a browser, you should now see a simple page that has a test button. Currently, all that happens when it is clicked is that a request of the type that is typed into the input box is sent to the server, and Python sends back a string telling you what request was sent. Test it out!
