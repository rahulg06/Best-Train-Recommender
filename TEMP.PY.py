import pickle
train_info = pickle.load(open('train_info.pkl', 'rb'))
TEMP=train_info[train_info['train_no'] == '12801']
print(train_info.iloc[600][0])
print(type(train_info))
