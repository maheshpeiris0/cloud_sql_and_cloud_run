from flask import Flask, render_template, request, jsonify
import os
import json
import sqlalchemy
from google.cloud.sql.connector import Connector
from google.oauth2 import service_account

# Obtain the key from the environment variable
service_account_key = os.environ.get('GCP_ACCESS_KEY')
if not service_account_key:
    raise ValueError("The GCP_SERVICE_ACCOUNT_KEY environment variable is not set")

key_data = json.loads(service_account_key)

credentials = service_account.Credentials.from_service_account_info(
    key_data,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

# initialize Connector object
connector = Connector(credentials=credentials)

INSTANCE_CONNECTION_NAME = os.environ.get('INSTANCE_CONNECTION_NAME') # codespace variable
DB_USER = os.environ.get('DB_USER') # codespace variable
DB_PASS = os.environ.get('DB_PASS') # codespace variable
DB_NAME = 'cloudrun'


def getconn():
    return connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pg8000",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )


pool = sqlalchemy.create_engine(
    f"postgresql+pg8000://{DB_USER}:{DB_PASS}@/{DB_NAME}",
    creator=getconn,
)

app = Flask(__name__)


@app.route('/')
def index():
    try:
        with pool.connect() as db_conn:
            data = db_conn.execute(sqlalchemy.text("SELECT * FROM employee")).fetchall()
        return render_template('index.html', data=data)
    except Exception as e:
        print(e)
        return render_template('error.html'), 500


# Define a route for page_two
@app.route('/page_two')
def page_two():
    return render_template('page_two.html')

# Define a route for page_three
@app.route('/eventform')
def event_form():
    return render_template('eventform.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        data = request.json
        data["age"] = int(data["age"]) 
        with pool.connect() as db_conn:
            insert_sql = sqlalchemy.text("INSERT INTO employee (name, age, country) VALUES (:name, :age, :country);")
            bound_sql = insert_sql.bindparams(name=data["name"], age=data["age"], country=data["country"])
            db_conn.execute(bound_sql)
            db_conn.commit()

        return jsonify({"message": "Form data submitted successfully!"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred while submitting the form."}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)