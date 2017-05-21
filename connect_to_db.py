import pyodbc

server = 'omnivores-version-1.database.windows.net'
database = 'banana_sql_database'
username = 'Admin.Green'
password = '@passw0rd'
driver= '{SQL Server}'
output_file = "out.csv"

x_query = 'SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE=\'BASE TABLE\''

def create_connection(server, database, username, password, driver):
    cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    return cursor

def query_from_db(cursor, query):
    cursor.execute(query)
    row = cursor.fetchone()
    print("Query results from database:")
    while row:
       # print(row)
        row = cursor.fetchone()
   # print("End of results!")    

def get_table_name(connected_cursor):
    table_query = 'SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE=\'BASE TABLE\''
    connected_cursor.execute(table_query)
    row = connected_cursor.fetchone()
   
    result_list = ''
  #  print("Table name query results:")
    while row:
        row = row[0]
        #print(row)
        result_list += str(row) + ','
        row = connected_cursor.fetchone()
  #  print("End of results!")
  # remove the comma on the end
    return result_list[0:-1]

def get_column_name(connected_cursor): 
    column_query = 'SELECT * FROM INFORMATION_SCHEMA.COLUMNS' 
    connected_cursor.execute(column_query)
    row = connected_cursor.fetchone()
    print("Column name query results:")
    while row:
        print(row)
        row = connected_cursor.fetchone()
    print("End of results!")
    
def write_table_to_csv(cursor, table_name):
    x_query = "SELECT * FROM %s" % (table_name)
    cursor.execute(x_query)
    with open(output_file, "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in cursor.description]) # write headers
        csv_writer.writerows(cursor) 
    print("Write table to csv done!")    

if __name__ == "__main__":
    connection = create_connection(server, database, username, password, driver)
    get_column_name(connection)