from train import Model
import pickle,json
import pandas as pd

if __name__ == '__main__':
	with open('traindata.json','r') as fp:
		data = json.load(fp)

	X_train = pd.Series(json.loads(data['X_train']))
	y_train = pd.Series(json.loads(data['y_train']))

	m = Model(X_train,y_train)
	cv , cv_train_reviews = m.train()
	print(cv)
	lr = m.model(cv_train_reviews)
	print(lr)
	with open('model.pkl', 'wb') as fout:
		pickle.dump((cv,lr), fout)