import json
import connect_to_db as db

FLAGS = NONE


def return_json_response(connection):
    table_name = db.get_table_name(connection)
    response = json.dumps( { "columns" : table_name} )
    print(response)

if __name__ == "__main__":
    connection = db.create_connection(db.server, db.database, db.username, db.password, db.driver)
    return_json_response(connection)
    parser = argparse.ArgumentParser()
    parser.add_argument('--fake_data', nargs='?', const=True, type=bool,
                      help='If true, uses fake data for unit testing.')
    