# -*- coding: utf-8 -*-
"""Nhom10.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19S_WFjN0KgB-q8XEAaHw_NQZTYg3aGHV
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
import matplotlib.pyplot as plt

from google.colab import drive
drive.mount('/content/drive')

customer_data = pd.read_csv('/content/drive/My Drive/data_shop.csv', encoding='latin1')
customer_data.head()

#### chiều dữ liệu
print(customer_data.shape)

X = customer_data.iloc[:, 2:4].values
print(X.shape)

plt.figure(figsize=(12, 8))
plt.scatter(X[:,0], X[:,1], lw=1, s=40)
plt.title('Biểu đồ phân phối dữ liệu')

data = customer_data.drop(columns= ["IDKhachHang","GioiTinh"], axis=1)

data.head()

data.shape

##### Chuẩn hóa dữ liệu
from sklearn.preprocessing import normalize
data = pd.DataFrame( normalize(data) , columns=data.columns)
data.head()

### Trực quan hóa dendrogram
import scipy.cluster.hierarchy as shc
plt.figure(figsize=(10, 7))
plt.title("Dendrograms")
dend = shc.dendrogram(shc.linkage(data, method='ward'))

#Cắt biểu đồ
plt.figure(figsize=(10, 7))
plt.title("Dendrograms")
dend = shc.dendrogram(shc.linkage(data, method='ward'))
plt.axhline(y=2, color='r', linestyle='--')
plt.show()

#Xây dựng mô hình phân cụm phân cấp hợp nhất
from sklearn.cluster import AgglomerativeClustering
AgglomerativeClustering(
  n_clusters=2,  #Trong đó n_clusters là số lượng cụm cần phân chia
  affinity='euclidean', #là phương pháp tính khoảng cách giữa các quan sát
  compute_full_tree='auto', 
  linkage='ward', #phương pháp áp dụng để tính khoảng cách giữa các cụm
  distance_threshold=None, 
  compute_distances=False)

#Tạo cụm với phân cụm kết tụ
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import MinMaxScaler
std = MinMaxScaler()
X_std = std.fit_transform(X)
#sử dụng khoảng các cụm là ward linkage và phương pháp tính khoảng cách giữa các điểm là euclidean.
cluster = AgglomerativeClustering(n_clusters=5, affinity='euclidean', linkage='ward')
labels = cluster.fit_predict(X_std)

cluster.fit_predict(data)

import seaborn as sns
import matplotlib.patheffects as PathEffects
def hierarchical_clustering(X, labels):
    '''
    X: dữ liệu đầu vào
    labels: nhãn dự báo
    '''
    # lựa chọn màu sắc
    num_classes = len(np.unique(labels))
    palette = np.array(sns.color_palette("hls", num_classes))

    fig = plt.figure(figsize=(12, 8))
    ax = plt.subplot()
    sc = ax.scatter(X[:,0], X[:,1], lw=0, s=40, c=palette[labels.astype(np.int)])
    txts = []
    
    for i in range(num_classes):
        # Vẽ text tên cụm tại trung vị của mỗi cụm
        xtext, ytext = np.median(X[labels == i, :], axis=0)
        txt = ax.text(xtext, ytext, str(i), fontsize=24)
        txt.set_path_effects([
            PathEffects.Stroke(linewidth=5, foreground="w"),
            PathEffects.Normal()])
        txts.append(txt)
    plt.title('t-sne visualization')

hierarchical_clustering(X_std, labels)