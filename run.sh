export FLASK_APP=wsgi.py
export FLASK_DEBUG=0
export APP_CONFIG_FILE=config.py
export SQLALCHEMY_DATABASE_URI=sqlite+pysqlite:///database.db
export SECRET_KEY=abcd1234

flask run