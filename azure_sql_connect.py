import pyodbc
import json
import csv

server = 'omnivores-version-1.database.windows.net'
database = 'banana_sql_database'
username = 'Admin.Green'
password = '@passw0rd'
driver= '{SQL Server}'

output_file = "out.csv"

# Query to get column name
table_query = 'SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE=\'BASE TABLE\''
column_query = 'SELECT * FROM INFORMATION_SCHEMA.COLUMNS' 
table_column_query = 'SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=\'your_table_name\''

def write_csv_to_file(cursor, table_name):
    x_query = "SELECT * FROM %s" % (table_name)
    cursor.execute(x_query)
    with open(output_file, "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in cursor.description]) # write headers
        csv_writer.writerows(cursor) 
    print("Done!")
        
def create_connection(server, database, username, password, driver):
    cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    return cursor

def get_column_from_table(cursor, table):
    x_query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=\'%s\'" % (table)
    cursor.execute(x_query)
    row = cursor.fetchone()
    print("X name query results:")
    while row:
        print(row)
        row = cursor.fetchone()
    print("End of results!")    

def get_table_name(connected_cursor):
    table_query = 'SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE=\'BASE TABLE\''
    connected_cursor.execute(table_query)
    row = connected_cursor.fetchone()
    result_list = ''
    print("Table name query results:")
    while row:
        print(row)
        result_list += str(row) +','
        row = connected_cursor.fetchone()
    print("End of results!")
    return result_list

def get_column_name(connected_cursor):    
    connected_cursor.execute(column_query)
    row = connected_cursor.fetchone()
    print("Column name query results:")
    while row:
        print(row)
        row = connected_cursor.fetchone()
    print("End of results!")
    
def return_json_response(connection):
    table_name = get_table_name(connection)
    response = json.dumps( { "columns" : table_name} )
    print(response)
    

if __name__ == "__main__":
    connection = create_connection(server, database, username, password, driver)
    #return_json_response(connection)
    #get_table_name(connection)
    #get_column_from_table(connection, "CreditScore")
    write_csv_to_file(connection, "CreditScore")
        
    