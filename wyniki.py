import numpy as np
import matplotlib.pyplot as plt
CCA_mod=np.array([72,67,65,65])
CCA_GA=np.array([83,68,54,74])
subj=np.arange(4)
plt.bar(subj ,CCA_mod,color='b',label='CCA',width = 0.4)
plt.bar(subj +0.4,CCA_GA,color='r',label='CCA + GA',width = 0.4)
podpisy=['Subject 1','Subject 2','Subject 3','Subject 4']
plt.xticks(subj+0.25,podpisy)
plt.xlabel('Subject')
plt.ylabel('Accuracy [%]')
plt.legend()
plt.show()
