# -*- coding: utf-8 -*-
"""CSCE636_test_part8.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ab-VuJaDarPXHzIwo59Vl11cfF-Rmi83
"""

from google.colab import drive
drive.mount('/content/drive/')

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 1.x

from keras.models import model_from_json
# load json and create model
path = '/content/drive/My Drive'
json_file = open(path+'/model_part8.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights(path+"/model_part8.h5")
print("Loaded model from disk")
 # evaluate loaded model on test data
loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

import os
import cv2
import random
import numpy as np
import tensorflow as tf
path_test = '/content/drive/My Drive/video_test1.mp4'
videoCapture = cv2.VideoCapture(path_test)
t = 31
l = 30
m = 6
frames = []
X = []
while 1 :
    success, frame = videoCapture.read()
    if not success:
        break
    frame = cv2.resize(frame,(299,299),interpolation = cv2.INTER_AREA)
    frames.append(frame)
for j in range(0,len(frames)-t,l):
    data = frames[j:j+t:m]
    X.append(data)
X = np.asarray(X)
res1 = loaded_model.predict(X)
res = []
for i in range(len(res1)):
  res.append(res1[i][0])
print(res)

'''
print('binary-classification result:',res)
jsontext = {'points':[]}
for i in range(len(res)):
    jsontext['points'].append({'Time':str(i), 'Label result':str(res[i])})
import json
jsondata = json.dumps(jsontext,indent=4,separators=(',', ': '))
f = open('/content/drive/My Drive/video_test3.json', 'w')
f.write(jsondata)
f.close()
'''
pre = 0
start = []
end = []

for i in range(len(res)):
  if pre <= 0.5 and res[i] >0.5:
    start.append(i)
  elif pre >= 0.5 and res[i] < 0.5:
    end.append(i)
  pre = res[i]
print('start time:',start)
print('end time:',end)


import matplotlib.pyplot as plt
plt.plot(range(1, len(res) + 1), res)
plt.xlabel('Time')
plt.ylabel('Label')
plt.show()

print(len(res))