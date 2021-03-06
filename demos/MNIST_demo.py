# This demo is intended to train a softmax classifier on the MNIST data. This
# network has no hidden layer, and achieves about 92.6% accuracy on the test set

import idx2numpy
import numpy as np
from nnet import SoftmaxClassifier as scl
from nnet.common import dataproc as dp

# define the paths
print 'Loading data...'
train_img_path = '/home/avasbr/Desktop/data/train-images.idx3-ubyte'
train_lbl_path = '/home/avasbr/Desktop/data/train-labels.idx1-ubyte' 
test_img_path = '/home/avasbr/Desktop/data/t10k-images.idx3-ubyte' 
test_lbl_path = '/home/avasbr/Desktop/data/t10k-labels.idx1-ubyte'

# convert the raw images into feature vectors
train_img = idx2numpy.convert_from_file(train_img_path)
m,row,col = train_img.shape
d = row*col # dimensions
X = np.reshape(train_img,(m,d)).T/255. # train data matrix
train_lbl = idx2numpy.convert_from_file(train_lbl_path)
k = max(train_lbl)+1

# set the targets for the training-set
y = np.zeros((k,m))
for i,idx in enumerate(train_lbl):
	y[idx,i] = 1

split = 0.5 # proporition to split for training/validation
pidx = np.random.permutation(m)

m_tr = int(split*m)
X_tr = X[:,pidx[:m_tr]]
y_tr = y[:,pidx[:m_tr]]

X_val = X[:,pidx[m_tr:]]
y_val = y[:,pidx[m_tr:]]

# set the data matrix for test
test_img = idx2numpy.convert_from_file(test_img_path)
m_te = test_img.shape[0]
X_te = np.reshape(test_img,(m_te,d)).T/255. # test data matrix
test_lbl = idx2numpy.convert_from_file(test_lbl_path)

# set the targets for the test-set
y_te = np.zeros((k,m_te))
for i,idx in enumerate(test_lbl):
	y_te[idx,i] = 1

# for gradient descent-based optimization algorithms
def x_data():
	batch_size = 300
	idx = 0
	while True: # cyclic generation
		idx_range = range((idx*batch_size)%m_tr,((idx+1)*batch_size-1)%m_tr+1)
		yield (X_tr[:,idx_range],y_tr[:,idx_range])
		idx += 1

print 'MNIST classification using the Softmax classifier\n'

print 'Data:'
print '-----'
print 'Number of samples for training:',m_tr
print 'Number of samples for testing:',m_te,'\n'

# define the architecture
nnet_params = {'d':d,'k':k,'n_hid':[],'decay':0.0} # initialize parameters
optim_params = {'method':'L-BFGS-B','n_iter':400} # define optimization routine
# optim_params = {"method":"SGD","n_iter": 200,"learn_rate":0.9,"plot_val_curves":True,"val_idx":10}

# print to console
dp.pretty_print('Neural Network parameters',nnet_params)
dp.pretty_print('Optimization parameters',optim_params)

# fit the model to the data and report performance
nnet = scl.SoftmaxClassifier(**nnet_params) # define the network
nnet.fit(X=X_tr,y=y_tr,x_data=x_data,X_val=X_val,y_val=y_val,**optim_params) # train
pred,mce_te = nnet.predict(X_te,y_te)

print 'Performance:'
print '------------'
print 'Accuracy:',100.*(1-mce_te),'%'

# print 'Saving the model'
# fname = '/home/bhargav/Desktop/mnist_softmax_network.pickle'
# nnet.save_network(fname)
