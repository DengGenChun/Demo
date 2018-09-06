set WORKON_HOME=D:\dt\PyEnv
set PYTHON_HOME=D:\env\Python3
set PATH=%PYTHON_HOME%;%PYTHON_HOME%\Scripts;%PATH%

pip install pipenv
pipenv install flask
pipenv install flask_sqlalchemy
pipenv install flask_script
pipenv install flask_migrate
pipenv install pymysql
pipenv install requests
