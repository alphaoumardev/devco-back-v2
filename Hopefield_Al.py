
import numpy as np
import random
from PIL import Image
import os
import re
import matplotlib.pyplot as plt
from IPython.core.interactiveshell import InteractiveShell

InteractiveShell.ast_node_interactivity = "all"


# 将jpg格式或者jpeg格式的图片转换为二值矩阵。先生成x这个全零矩阵，从而将image_array中的色度值分类，获得最终的二值矩阵。
def read_image_array(file, size, threshold=145):
    # file is jpg or jpeg pictures
    # size is a 1*2 vector,eg (40,40)
    pil_in = Image.open(file).convert(mode="L")
    pil_in = pil_in.resize(size)
    # pil_in.thumbnail(size,Image.ANTIALIAS)
    image_array = np.asarray(pil_in, dtype=np.uint8)
    x = np.zeros(image_array.shape, dtype=np.float)
    x[image_array > threshold] = 1
    x[x == 0] = -1
    return x


def create_w_patternsingle_pattern(x):
    # x is a vector
    if len(x.shape) != 1:
        print("The input is not vector")
        return
    else:
        w = np.zeros([len(x), len(x)])
        for i in range(len(x)):
            for j in range(i, len(x)):
                if i == j:
                    w[i, j] = 0
                else:
                    w[i, j] = x[i] * x[j]
                    w[j, i] = w[i, j]
    return w


# 逆变换
def array2img(data, outFile=None):
    # data is 1 or -1 matrix
    y = np.zeros(data.shape, dtype=np.uint8)
    y[data == 1] = 255
    y[data == -1] = 0
    img = Image.fromarray(y, mode="L")
    if outFile is not None:
        img.save(outFile)
    return img


# 利用x.shape得到矩阵x的每一维个数，从而得到m个元素的全零向量。将x按i\j顺序赋值给向量tmp1. 最后得到从矩阵转换的向量。
def mat2vec(x):
    # x is a matrix
    m = x.shape[0] * x.shape[1]
    tmp1 = np.zeros(m)

    c = 0
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            tmp1[c] = x[i, j]
            c += 1
    return tmp1


# 创建权重矩阵根据权重矩阵的对称特性，可以很好地减少计算量。
# 请填写代码

# 输入test picture之后对神经元的随机升级。利用异步更新，获取更新后的神经元向量以及系统能量。
# randomly update
def update_asynch(weight, vector, theta=0.5, times=100):
    energy_ = []
    times_ = []
    energy_.append(energy(weight, vector))
    times_.append(0)
    for i in range(times):
        length = len(vector)
        update_num = random.randint(0, length - 1)
        next_time_value = np.dot(weight[update_num][:], vector) - theta
        if next_time_value >= 0:
            vector[update_num] = 1
        if next_time_value < 0:
            vector[update_num] = -1
        times_.append(i)
        energy_.append(energy(weight, vector))

    return vector, times_, energy_


# 为了更好地看到迭代对系统的影响，我们按照定义计算每一次迭代后的系统能量，最后画出E的图像，便可验证。

def energy(weight, x, bias=0):
    # weight: m*m weight matrix
    # x: 1*m data vector
    # bias: outer field
    energy = -x.dot(weight).dot(x.T) + sum(bias * x)
    # E is a scalar
    return energy


# 调用前文定义的函数把主函数表达清楚。可以调整size和threshod获得更好的输入效果为了增加泛化能力，正则化之后打开训练图片，并且通过该程序获取权重矩阵。
# 请输入代码
# 测试图片
# 请输入代码
# 利用对测试图片的矩阵（神经元状态矩阵）进行更新迭代，直到满足我们定义的迭代次数。最后将迭代末尾的矩阵转换为二值图片输出。
# plt.show()
size_global = (80, 80)
threshold_global = 60

train_paths = []
# train_path = "/Users/admin/Desktop/train_pics/"
train_path = "/Users/alpha/Desktop/test/"

# train_path = "test.jpg"
for i in os.listdir(train_path):
    if re.match(r'[0-9 a-z A-Z-_]*.jp[e]*g', i):
        train_paths.append(train_path + i)
flag = 0
for path in train_paths:
    matrix_train = read_image_array(path, size=size_global, threshold=threshold_global)
    vector_train = mat2vec(matrix_train)
    plt.imshow(array2img(matrix_train))
    plt.title("train picture" + str(flag + 1))
    plt.show()
    if flag == 0:
        w_pattern = create_w_patternsingle_pattern(vector_train)
        flag = flag + 1
    else:
        w_pattern = w_pattern + create_w_patternsingle_pattern(vector_train)
        flag = flag + 1

w_pattern = w_pattern / flag
print("weight matrix is prepared!!!!!")
test_paths = []
test_path = "/Users/alpha/Desktop/test/"
# test_path = "test.jpg"
for i in os.listdir(test_path):
    if re.match(r'[0-9 a-z A-Z-_]*.jp[e]*g', i):
        test_paths.append(test_path + i)
num = 0
for path in test_paths:
    num = num + 1
    matrix_test = read_image_array(path, size=size_global, threshold=threshold_global)
    vector_test = mat2vec(matrix_test)
    plt.subplot(221)
    plt.imshow(array2img(matrix_test))
    plt.title("test picture" + str(num))
    oshape = matrix_test.shape
    aa = update_asynch(weight=w_pattern, vector=vector_test, theta=0.5, times=8000)
    vector_test_update = aa[0]
    matrix_test_update = vector_test_update.reshape(oshape)
    # matrix_test_update.shape
    # print(matrix_test_update)
    plt.subplot(222)
    plt.imshow(array2img(matrix_test_update))
    plt.title("recall" + str(num))

    # plt.show()
    plt.subplot(212)
    plt.plot(aa[1], aa[2])
    plt.ylabel("energy")
    plt.xlabel("update times")

    plt.show()
