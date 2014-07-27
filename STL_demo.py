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
train_img_path = '/home/avasbr/Desktop/train-images.idx3-ubyte'
train_lbl_path = '/home/avasbr/Desktop/train-labels.idx1-ubyte' 
test_img_path = '/home/avasbr/Desktop/t10k-images.idx3-ubyte' 
test_lbl_path = '/home/avasbr/Desktop/t10k-labels.idx1-ubyte'

# load all the data
train_img = idx2numpy.convert_from_file(train_img_path)
train_lbl = idx2numpy.convert_from_file(train_lbl_path)
test_img = idx2numpy.convert_from_file(test_img_path)
test_lbl = idx2numpy.convert_from_file(test_lbl_path)

dummy,row,col = train_img.shape
d = row*col # dimensions of training data

# set up unlabeled data - we will learn features from this data later
ul_digits = [5,6,7,8,9]
ul_idx = [i for i,v in enumerate(train_lbl) if v in ul_digits]
m_ul = len(ul_idx)
k_ul = len(ul_digits)

X_ul = np.reshape(train_img[ul_idx],(m_ul,d)).T/255. 

# this block is just for verification purposes/sanity checks - won't be used
y_ul = np.zeros((k_ul,m_ul))
for i,c in enumerate(train_lbl[ul_idx]):
	y_ul[ul_digits.index(c),i] = 1

# set up training data
tr_digits = [0,1,2,3,4]
tr_idx = [i for i,v in enumerate(train_lbl) if v in tr_digits]

m_tr = len(tr_idx)
X_tr = np.reshape(train_img[tr_idx],(m_tr,d)).T/255
k_tr = len(tr_digits)
y_tr = np.zeros((k_tr,m_tr))
for i,c in enumerate(train_lbl[tr_idx]):
	y_tr[tr_digits.index(c),i] = 1

# set up test data
te_idx = [i for i,v in enumerate(test_lbl) if v in tr_digits]
m_te = len(te_idx)
X_te = np.reshape(test_img[te_idx],(m_te,d)).T/255.
y_te = np.zeros((k_tr,m_te))
for i,c in enumerate(test_lbl[te_idx]):
	y_te[tr_digits.index(c),i] = 1

# Various initialization values
sae_hid = 200
scl_hid = [25]
decay = 0.0001
beta = 3
rho = 0.01
method = 'L-BFGS'

print 'Test 1: Running softmax classifier on raw pixels'
print '------------------------------------------------'
print 'Number of training samples: ',m_tr
print 'Number of testing samples: ',m_te
softmax = scl.SoftmaxClassifier(d=d,k=k_tr,n_hid=scl_hid,decay=decay)
softmax.set_weights('alt_random')
pred,mce = softmax.fit(X_tr,y_tr,method=method).predict(X_te,y_te)
print 'Misclassification rate: ',mce

# print 'Test 2: Run softmax classifier using learned features from unlabeled data'
# print '--------------------------------------------------------------------------'
# print 'Number of unlabeled samples: ',m_u
# print 'Number of training samples: ',m_tr
# print 'Number of testing samples: ',m_te
# sparse_ae = ae.Autoencoder(d=d,k=k_ul,n_hid=sae_hid,decay=decay,beta=beta,rho=rho)
# sparse_ae.set_weights('alt_random')
# sparse_ae.fit(X_u,method=method)
# X_tr_tfm = sparse_ae.transform(X_tr)
# X_te_tfm = sparse_ae.transfrom(X_te)
# softmax = scl.SoftmaxClassifier(d=d,k=k_tr,n_hid=scl_hid,decay=decay):