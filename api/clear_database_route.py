from __main__ import app
from database_init import clean_database


@app.route('/api/clear_db/<Password>', methods=['GET'])
def clear_db_route(Password):
    if Password != "BME547":
        return "Password incorrect"
    clean_database()
    return "Cleaned Database", 200
