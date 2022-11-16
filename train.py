import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn import linear_model
import numpy as np

plt.style.use('ggplot')

# Load data
# boston = datasets.load_boston()
# yb = boston.target.reshape(-1, 1)
# Xb = boston['data'][:, 5].reshape(-1, 1)
# # Plot data
# plt.scatter(Xb, yb)
# plt.ylabel('value of house /1000 ($)')
# plt.xlabel('number of rooms')
# # Create linear regression object
# regr = linear_model.LinearRegression()
# # Train the model using the training sets
# regr.fit(Xb, yb)
# # Plot outputs
# plt.scatter(Xb, yb, color='black')
# plt.plot(Xb, regr.predict(Xb), color='blue',
#          linewidth=3)
# plt.show()

"""plt.axes()"""
# create some data to use for the plot
# dt = 0.001
# t = np.arange(0.0, 10.0, dt)
# r = np.exp(-t[:1000] / 0.05)  # impulse response
# x = np.random.randn(len(t))
# s = np.convolve(x, r)[:len(x)] * dt  # colored noise
#
# # the main axes is subplot(111) by default
# plt.plot(t, s)
# plt.axis([0, 1, 1.1 * np.amin(s), 2 * np.amax(s)])
# plt.xlabel('time (s)')
# plt.ylabel('current (nA)')
# plt.title('Gaussian colored noise')
#
# # this is an inset axes over the main axes
# a = plt.axes([.65, .6, .2, .2],)
# n, bins, patches = plt.hist(s, 400, )
# plt.title('Probability')
# plt.xticks([])
# plt.yticks([])
#
# # this is another inset axes over the main axes
# a = plt.axes([0.2, 0.6, .2, .2], )
# plt.plot(t[:len(r)], r)
# plt.title('Impulse response')
# plt.xlim(0, 0.2)
# plt.xticks([])
# plt.yticks([])

# plt.show()
""" """
# ax = plt.subplot(111)
#
# t = np.arange(0.0, 5.0, 0.01)
# s = np.cos(2 * np.pi * t)
# line, = plt.plot(t, s, lw=2)
#
# plt.annotate('local max', xy=(2, 1), xytext=(3, 1.5),
#              arrowprops=dict(facecolor='black', shrink=0.05),
#              )
#
# plt.ylim(-2, 2)
# plt.show()

""" """

# mu, sigma = 100, 15
# x = mu + sigma * np.random.randn(1000)
#
# # 数据的直方图
# n, bins, patches = plt.hist(x, 5, facecolor='g', alpha=0.75)
#
# plt.xlabel('Smarts')
# plt.ylabel('Probability')
# # 添加标题
# plt.title('Histogram of IQ')
# # 添加文字
# plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
# plt.axis([40, 160, 0, 0.03])
# plt.grid(True)
# plt.show()


""" """

# evenly sampled time at 200ms intervals
t = np.arange(0., 5., 0.2)

# red dashes, blue squares and green triangles
plt.plot(t, t, 'r--', t, t ** 2, 'bs', t, t ** 3, 'g^')
plt.show()
