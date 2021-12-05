from __main__ import app
from database_init import clean_database


@app.route('/api/clear_db/<Password>', methods=['GET'])
def clear_db_route(Password):
    """Developer method which simply clears database.
    Correct password is required (BME547)

    send get request to host/api/clear_db/<Password>
    to clear database contents

    Returns:
        str: either "Password incorrect" or "Cleaned Database"
    """
    if Password != "BME547":
        return "Password incorrect"
    clean_database()
    return "Cleaned Database", 200
