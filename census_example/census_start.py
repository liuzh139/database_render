import pandas as pd
import tensorflow as tf
import os

# Turn off CPU/GPU warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

model_dir = './tmp'
train_data_file = 'census_train.csv'
test_data_file = 'census_test.csv'

# Define columns
COLUMNS = ["age", "workclass", "fnlwgt", "education", "education_num",
           "marital_status", "occupation", "relationship", "race", "gender",
           "capital_gain", "capital_loss", "hours_per_week", "native_country",
           "income_bracket"]
df_train = pd.read_csv(train_data_file, names=COLUMNS, skipinitialspace=True)
df_test = pd.read_csv(test_data_file, names=COLUMNS, skipinitialspace=True, skiprows=1)

LABEL_COLUMN = "target_feature_label"

# Define the target column - that is the income over 50k
df_train[LABEL_COLUMN] = (df_train["income_bracket"].apply(lambda x: ">50K" in x)).astype(int)
df_test[LABEL_COLUMN] = (df_test["income_bracket"].apply(lambda x: ">50K" in x)).astype(int)

CATEGORICAL_COLUMNS = ["workclass", "education", "marital_status", "occupation",
                       "relationship", "race", "gender", "native_country"]
CONTINUOUS_COLUMNS = ["age", "education_num", "capital_gain", "capital_loss", "hours_per_week"]

# Categorical columns with keys
gender = tf.contrib.layers.sparse_column_with_keys(column_name="gender", keys=["Female", "Male"])

# Categorical columns with hash_key
education = tf.contrib.layers.sparse_column_with_hash_bucket("education", hash_bucket_size=1000)
race = tf.contrib.layers.sparse_column_with_hash_bucket("race", hash_bucket_size=100)
marital_status = tf.contrib.layers.sparse_column_with_hash_bucket("marital_status", hash_bucket_size=100)
relationship = tf.contrib.layers.sparse_column_with_hash_bucket("relationship", hash_bucket_size=100)
workclass = tf.contrib.layers.sparse_column_with_hash_bucket("workclass", hash_bucket_size=100)
occupation = tf.contrib.layers.sparse_column_with_hash_bucket("occupation", hash_bucket_size=1000)
native_country = tf.contrib.layers.sparse_column_with_hash_bucket("native_country", hash_bucket_size=1000)

# Continuous columns with real value
age = tf.contrib.layers.real_valued_column("age")
education_num = tf.contrib.layers.real_valued_column("education_num")
capital_gain = tf.contrib.layers.real_valued_column("capital_gain")
capital_loss = tf.contrib.layers.real_valued_column("capital_loss")
hours_per_week = tf.contrib.layers.real_valued_column("hours_per_week")

# Continuous features categorical through bucketization
age_buckets = tf.contrib.layers.bucketized_column(age, boundaries=[18, 25, 30, 35, 40, 45, 50, 55, 60, 65])

# Intersecting Multiple Columns with CrossedColumn
education_x_occupation = tf.contrib.layers.crossed_column([education, occupation], hash_bucket_size=int(1e4))
age_buckets_x_education_x_occupation = tf.contrib.layers.crossed_column(
    [age_buckets, education, occupation], hash_bucket_size=int(1e6))

def input_fn(df):
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

def train_input_fn():
    return input_fn(df_train)

def eval_input_fn():
    return input_fn(df_test)

# Basic model
model_first = tf.contrib.learn.LinearClassifier(feature_columns=[
    gender, native_country, education, occupation, workclass, marital_status, race,
  age_buckets, education_x_occupation, age_buckets_x_education_x_occupation],
                                      model_dir=model_dir)

# Model that is regulized to pass
model_regulized = tf.contrib.learn.LinearClassifier(feature_columns=[
    gender, native_country, education, occupation, workclass, marital_status, race,
  age_buckets, education_x_occupation, age_buckets_x_education_x_occupation],
                                      optimizer=tf.train.FtrlOptimizer(
                                          learning_rate=0.1,
                                         # l1_regularization_strength=1.0,
                                          l2_regularization_strength=1.0),
                                      model_dir=model_dir)

# model_regulized.fit(input_fn=train_input_fn, steps=200)
model_first.fit(input_fn=train_input_fn, steps=200)

results = model_first.evaluate(input_fn=eval_input_fn, steps=1)

print("Report starting!")    

for key in sorted(results):
    print("Result: %s: \t %s" % (key, results[key]))

print("Report finished!") 