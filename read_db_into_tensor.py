import MySQLdb
import re
import json
import pandas as pd
import tensorflow as tf

db = MySQLdb.connect(
    host = 'localhost',
     user = 'root',
     passwd = '19931124',
     db = 'test'
)
cursor = db.cursor()

def get_column_name(connected_cursor): 
    column_query = 'SELECT * FROM INFORMATION_SCHEMA.COLUMNS' 
    connected_cursor.execute(column_query)
    row = connected_cursor.fetchone()
    print("Column name query results:")
    while row:
        print(row)
        row = connected_cursor.fetchone()
    print("End of results!")    

def get_column_from_table(cursor, table):
    x_query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=\'%s\'" % (table)
    cursor.execute(x_query)
    row = cursor.fetchone()
    columns = []
    while row:
        # Remove special char from the column name
        column_name = re.sub('[^a-zA-Z0-9 \n\.\'\(\)]', '', str(row))
        columns.append(column_name)
        row = cursor.fetchone()
    return columns
    
def read_db_columns(cursor, table_name):
    x_query = "SELECT * FROM %s" % (table_name)
    cursor.execute(x_query)
    row = cursor.fetchone()
    
    print(row)
    columns = []    
    
def return_json_columns(columns):
    result = '{'
    for column_name in columns:
        result += " \"column_name\" :  \"" + column_name + "\", "
    result += '}'

    return json.dumps(result)

def read_json_to_columns(json_input):
    
    # This is example of how to read the columns into list
    json_input = '{"column": [{"name": "age", "data_type": "continous"}, {"name": "gender", "data_type": "categorical"} ] }'
    
    CATEGORICAL_COLUMNS = []
    CONTINUOUS_COLUMNS = []
    
    try:
        decoded = json.loads(json_input)
     
        # Access data
        for x in decoded['column']:
            if x['data_type'] == 'continous':
                CONTINUOUS_COLUMNS += x['name']
            if x['data_type'] == 'categorical':
                CATEGORICAL_COLUMNS += x['name']
                
        return CATEGORICAL_COLUMNS, CONTINUOUS_COLUMNS
     
    except (ValueError, KeyError, TypeError):
        print( "JSON format error")
        
def read_json_to_tensors(json_input):
    
    # This is example of how to read the columns into list
    json_input = '{"column": [{"name": "age", "data_type": "continous"}, {"name": "gender", "data_type": "categorical"} ] }'
    try:
        decoded = json.loads(json_input)
        
        # A list of tensor holder for columns
        column_tensors={}
 
        # Access data
        for x in decoded['column']:
            print( x['name'])
            if x['data_type'] == 'continous':
                column_tensors["tensor_{0}".format(x['name'])] = tf.contrib.layers.real_valued_column(x['name'])
            if x['data_type'] == 'categorical':
                # hash_bucket_size here can be improved/adjusted based on database size
                # can do preprocessing on column categorical value count
                column_tensors["tensor_{0}".format(x['name'])] = tf.contrib.layers.sparse_column_with_hash_bucket(x['name'], hash_bucket_size=1000)
                
        return column_tensors
    
    except (ValueError, KeyError, TypeError):
        print( "JSON format error")        

def read_column_from_db(df, CONTINUOUS_COLUMNS, CATEGORICAL_COLUMNS):
    # Creates a dictionary mapping from each continuous feature column name (k) to
    # the values of that column stored in a constant Tensor.
    continuous_cols = {k: tf.constant(df[k].values)
                       for k in CONTINUOUS_COLUMNS}    
    
    # Creates a dictionary mapping from each categorical feature column name (k)
    # to the values of that column stored in a tf.SparseTensor.
    categorical_cols = {k: tf.SparseTensor(
        indices=[[i, 0] for i in range(df[k].size)],
        values=df[k].values,
        dense_shape=[df[k].size, 1])
                      for k in CATEGORICAL_COLUMNS}
    
    # Merges the two dictionaries into one.
    feature_cols = continuous_cols.copy()
    feature_cols.update(categorical_cols)  
    
    # Specify a column
    label = tf.constant(df[LABEL_COLUMN].values)
    # Returns the feature columns and the label.
    return feature_cols, label    

# Example usage of training a model
def train_linear_classifier(feature_columns, target_column_type):
    
    # Specify a directory to store the model
    model_dir = './tmp'
        
    if target_column_type == "categorical":
        model = tf.contrib.learn.LinearClassifier(feature_columns = feature_columns, model_dir = model_dir)
    if target_column_type == "continous":
        model = tf.contrib.learn.DNNRegressor(feature_columns=feature_columns, hidden_units=[1024, 512, 256])
    return model

if __name__ == "__main__":
