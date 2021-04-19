import pandas as pd

train_set_csv_path = "./csvs/processed_train_set.csv"
test_set_csv_path = "./csvs/processed_test_set.csv"

train_set = pd.read_csv(train_set_csv_path)
test_set = pd.read_csv(test_set_csv_path)
