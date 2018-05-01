# WooMessages

To run flask app:

    <activate virtual environment>
 
    pip install flask
    pip install WTForms
    pip install tabulate
    pip install flask_login
    pip install passlib
    export FLASK_APP=app_main.py
    flask run
  
To initalise db:
   
    export FLASK_APP=app_main.py
    flask initdb

To initalise db with CSV data:

    export FLASK_APP=app_main.py
    flask initdb_with_csv <filename>
    
    e.g: flask initdb_with_csv WooMessages_CSV.csv
  
To run command line arguments:
    
    python3 query_WooMessage.py show api/message
    python3 query_WooMessage.py show api/chat
    python3 query_WooMessage.py show api/user

To run tests:

    python3 -m pytest -v test_flask_api.py
   
To test db with sqlite:

    sqlite3 WooMessages.sqlite < test_db.sql
  
