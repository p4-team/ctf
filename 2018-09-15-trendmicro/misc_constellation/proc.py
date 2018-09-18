import matplotlib.pyplot as plt
import seaborn as sns; sns.set()  # for plot styling
import numpy as np
from sklearn.datasets.samples_generator import make_blobs
from numpy import genfromtxt

#humm, encontre este codigo en un servidor remoto
#estaba junto con el "traffic.pcap"
# que podria ser?, like some sample code 

my_data2 = np.genfromtxt('test_2.txt', delimiter=',')
db = DBSCAN(eps=10000, min_samples=100000).fit(my_data2)
labels = db.labels_
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
          for each in np.linsspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):   
    class_member_mask = (labels == k)
    xy = X[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=14)
			 

			 
#NOTE: what you see in the sky put it format TMCTF{replace_here}
#where "replace_here" is what you see
plt.title('aaaaaaaa: %d' % n_clusters_)
plt.show()

