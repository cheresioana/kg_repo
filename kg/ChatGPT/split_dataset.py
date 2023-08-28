import pandas as pd

if __name__=="__main__":
    dataset = pd.read_csv('data2.csv')
    print(dataset.shape)
    random_entries = dataset.sample(10)
    dataset = dataset.drop(random_entries.index)
    print(dataset.shape)
    random_entries.to_csv('test_entries.csv', index=False)
    dataset.to_csv('train_entries.csv', index=False)
