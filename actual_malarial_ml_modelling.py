# -*- coding: utf-8 -*-
"""Actual_Malarial_ML_modelling.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PopmTckL0_MtTBiUVuBgGF8dI0qbCWrj
"""

import tensorflow_datasets as tfds
tfds.builder('malaria')
tfds.load('malaria')

import numpy as np
import tensorflow as tf
import os
import matplotlib.pyplot as plt

a=0
l=[]
for fn in os.listdir('/content/cell-images-for-detecting-malaria/cell_images/Parasitized'):
  a+=1
  if(a<=10):
    print(plt.imread(os.path.join('/content/cell-images-for-detecting-malaria/cell_images/Parasitized',fn)).shape)
    l.append(os.path.join('/content/cell-images-for-detecting-malaria/cell_images/Parasitized',fn))

IMG_SIZE = (64,64,3)
a=1
# for i in l:
#   plt.subplot(1,10,a)
#   plt.imshow(plt.imread(i))
#   a+=1
plt.subplot(1,2,2)
plt.imshow(plt.imread(l[0]))
plt.show()
plt.subplot(1,2,2)
plt.imshow(plt.imread(l[1]))
plt.show()
img = plt.imread(l[0])

labels=[]
#all the images from the parasitized will go to label 0 and uninfected will go to label 1
#Before that we will change the size of the input images to our desired input size which will be (64,64,3)
dataset = []
for fn in os.listdir('/content/cell-images-for-detecting-malaria/cell_images/cell_images/Uninfected'):
  img = plt.imread(os.path.join('/content/cell-images-for-detecting-malaria/cell_images/cell_images/Uninfected',fn))
  img = img.resize(64,64)

l1 = []
l2=[]
for fn in os.listdir('/content/cell-images-for-detecting-malaria/cell_images/cell_images/Uninfected'):
  s = os.path.join('/content/cell-images-for-detecting-malaria/cell_images/cell_images/Uninfected',fn)
  if(s.split('.')[1]=='png'):
    l1.append(s)
  else:
    l2.append(s)
#A wrong entry not of png type is there in the given datset it should be ignored
print(l2[0])
print(len(l1))
print(len(os.listdir('/content/cell-images-for-detecting-malaria/cell_images/cell_images/Uninfected')))

l3 = []
l4 = []
for fn in os.listdir('/content/cell-images-for-detecting-malaria/cell_images/cell_images/Parasitized'):
  s = os.path.join('/content/cell-images-for-detecting-malaria/cell_images/Parasitized',fn)
  if(s.split('.')[1]=='png'):
    l3.append(s)
  else:
    l4.append(s)
print(len(l3))
print(len(l4))
print(l4[0])

type(os.path.join('/content/cell-images-for-detecting-malaria/cell_images/cell_images/Uninfected',l[0]))

from PIL import Image
import cv2
for fn in os.listdir('/content/cell-images-for-detecting-malaria/cell_images/Parasitized'):
  s=os.path.join('/content/cell-images-for-detecting-malaria/cell_images/Parasitized',fn)
  if(s.split('.')[1]=='png'):
    img=cv2.imread(s)
    img=Image.fromarray(img,'RGB')
    img=img.resize((64,64))
    # print(type(img))
    dataset.append(np.array(img))
    labels.append(0)

import cv2
for fn in os.listdir('/content/cell-images-for-detecting-malaria/cell_images/Uninfected'):
  s=os.path.join('/content/cell-images-for-detecting-malaria/cell_images/Uninfected',fn)
  if(s.split('.')[1]=='png'):
    img=cv2.imread(s)
    img=Image.fromarray(img,'RGB')
    # img=np.array(img)
    img=img.resize((64,64))
    # print(type(img))
    dataset.append(np.array(img))
    labels.append(1)

#Model making
import keras
INPUT_SHAPE = (64,64,3)
input=keras.layers.Input(shape=INPUT_SHAPE)
conv1 = keras.layers.Conv2D(32, kernel_size=(3, 3),
                               activation='relu', padding='same')(input)
pool1 = keras.layers.MaxPooling2D(pool_size=(2, 2))(conv1)
norm1 = keras.layers.BatchNormalization(axis = -1)(pool1)
drop1 = keras.layers.Dropout(rate=0.2)(norm1)
conv2 = keras.layers.Conv2D(32, kernel_size=(3, 3),
                               activation='relu', padding='same')(drop1)
pool2 = keras.layers.MaxPooling2D(pool_size=(2, 2))(conv2)
norm2 = keras.layers.BatchNormalization(axis = -1)(pool2)
drop2 = keras.layers.Dropout(rate=0.2)(norm2)

flat = keras.layers.Flatten()(drop2)  #Flatten the matrix to get it ready for dense.

hidden1 = keras.layers.Dense(512, activation='relu')(flat)
norm3 = keras.layers.BatchNormalization(axis = -1)(hidden1)
drop3 = keras.layers.Dropout(rate=0.2)(norm3)
hidden2 = keras.layers.Dense(256, activation='relu')(drop3)
norm4 = keras.layers.BatchNormalization(axis = -1)(hidden2)
drop4 = keras.layers.Dropout(rate=0.2)(norm4)

out = keras.layers.Dense(2, activation='sigmoid')(drop4)

l=len(dataset)
#splliting the dataset into testing and training
#ration of 80 to 20 where x and y are the different labels of uninfected and parasitic class
from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test=train_test_split(dataset,keras.utils.to_categorical(np.array(labels)),test_size=0.20,train_size=0.80,random_state=0)

print(len(X_train))
print(len(Y_train))
print(len(X_test))
print(len(Y_test))
print(X_train.shape)

X_train=np.array(X_train)
Y_train=np.array(Y_train)
cnt=0
cnt2=0
for i in X_train:
    if(i is None):
      cnt+=1
for i in X_train:
    if(i is None):
      cnt2+=1
print(cnt)
print(cnt2)
print(len(X_train)-cnt)
print(len(X_train))

[print(i.shape, i.dtype) for i in model.inputs]
[print(o.shape, o.dtype) for o in model.outputs]
[print(l.name, l.input_shape, l.dtype) for l in model.layers]

model=keras.Model(inputs=input,outputs=out)
model.compile(optimizer="Adam",loss='categorical_cross_entropy',metrics=['accuracy'])
print(model.summary())

history=model.fit(np.array(X_train),Y_train,batch_size=50,epochs=10,validation_split=0.1)