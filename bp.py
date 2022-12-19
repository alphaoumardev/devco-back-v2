import numpy as np

#定义sigmoid函数
def sigmoid(x, deriv = False):
    if deriv:
        return x*(1-x)
    else:
        return 1/(1+np.exp(-x))

#input dataset
X = np.array([[0,0,1],
              [0,1,1],
              [1,0,1],
              [1,1,1]])

#output dataset
y = np.array([[0,1,1,0]]).T

#初始化权重
weight01 = 2*np.random.random((3,4)) - 1
weight12 = 2*np.random.random((4,2)) - 1
weight23 = 2*np.random.random((2,1)) - 1

#初始化偏倚
b1 = 2*np.random.random((1,4)) - 1
b2 = 2*np.random.random((1,2)) - 1
b3 = 2*np.random.random((1,1)) - 1
bias1=np.array([b1[0],b1[0],b1[0],b1[0]])
bias2=np.array([b2[0],b2[0],b2[0],b2[0]])
bias3=np.array([b3[0],b3[0],b3[0],b3[0]])

#开始训练
for j in range(60000):
    I0 = X
    O0=I0
    I1=np.dot(O0,weight01)+bias1
    O1=sigmoid(I1)
    I2=np.dot(O1,weight12)+bias2
    O2=sigmoid(I2)
    I3=np.dot(O2,weight23)+bias3
    O3=sigmoid(I3)

    f3_error = y-O3

    if(j%10000) == 0:
        print ("Error:"+str(np.mean(f3_error)))




    f3_delta = f3_error*sigmoid(O3,deriv = True)

    f2_error = f3_delta.dot(weight23.T)

    f2_delta = f2_error*sigmoid(O2,deriv = True)

    f1_error = f2_delta.dot(weight12.T)

    f1_delta = f1_error*sigmoid(O1,deriv = True)


    weight23 += O2.T.dot(f3_delta) #调整权重
    weight12 += O1.T.dot(f2_delta)
    weight01 += O0.T.dot(f1_delta)

    bias3 += f3_delta #调整偏倚
    bias2 += f2_delta
    bias1 += f1_delta

print ("outout after Training:")
# print (O3)

