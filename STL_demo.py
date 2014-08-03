# This goal of this demo is to build a neural network which can recognize digits 0-4, 
# but is trained on digits 5-9 - this is known as 'transfer' learning, or 'self-taught' 
# learning, where the idea is to learn features for one classification task is likely 
# to be useful for a similar classification task. This method is particularly useful if 
# there is an abundance of data for one classification task, but not of another, similar one.

import idx2numpy
import numpy as  np
import Autoencoder as ae
import SoftmaxClassifier as scl

# define the paths
train_img_path = '/home/avasbr/Desktop/MNIST_dataset/train-images.idx3-ubyte'
train_lbl_path = '/home/avasbr/Desktop/MNIST_dataset/train-labels.idx1-ubyte' 

# load all the data
train_img = idx2numpy.convert_from_file(train_img_path)
train_lbl = idx2numpy.convert_from_file(train_lbl_path)
m_tr,row,col = train_img.shape
d = row*col # dimensions of training data
k = max(train_lbl)+1
X = np.reshape(train_img,(m_tr,d)).T/255.
y = np.zeros((k,m_tr))
for i,cidx in enumerate(train_lbl):
	y[cidx,i] = 1

# set up the unlabeled data
ul_digits = [5,6,7,8,9]
ul_idx = [i for i,v in enumerate(train_lbl) if v in ul_digits]
X_ul = X[:,ul_idx]
temp = y[:,ul_idx]
y_ul = temp[ul_digits,:]

# set up training and test data
tr_digits = [0,1,2,3,4]
k_tr = len(tr_digits)

tr_idx = [i for i,v in enumerate(train_lbl) if v in tr_digits]
m_l = len(tr_idx)
X_l = X[:,tr_idx]
temp = y[:,tr_idx]
y_l = temp[tr_digits,:]

X_tr = X_l[:,:(m_l/2)]
y_tr = y_l[:,:(m_l/2)]
X_te = X_l[:,(m_l/2):]
y_te = y_l[:,(m_l/2):]

# Various initialization values
sae_hid = 200
scl_hid = []
n_iter = 400
decay = 0.003
beta = 3
rho = 0.1
method = 'L-BFGS'

print 'Test 1: Run softmax classifier on raw pixels'
nnet = scl.SoftmaxClassifier(d=d,k=k_tr,n_hid=scl_hid,decay=decay)
nnet.set_weights('alt_random')
pred,mce = nnet.fit(X_tr,y_tr,method=method,n_iter=n_iter).predict(X_te,y_te)
print 'Misclassification rate: ',mce

print 'Test 2: Run softmax classifier using learned features from unlabeled data'
sae_net = ae.Autoencoder(d=d,n_hid=sae_hid,decay=decay,beta=beta,rho=rho)
sae_net.set_weights('alt_random')
sae_net.fit(X_ul,method=method,n_iter=n_iter)
X_tr_tfm = sae_net.transform(X_tr)
X_te_tfm = sae_net.transform(X_te)
nnet = scl.SoftmaxClassifier(d=sae_hid,k=k_tr,n_hid=scl_hid,decay=decay)
nnet.set_weights('alt_random')
print 'Performing Softmax regression'
pred,mce = nnet.fit(X_tr_tfm,y_tr,method=method,n_iter=n_iter).predict(X_te_tfm,y_te)
print 'Misclassification rate: ',mce