import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def func(X, Y):
    return np.exp((-(X + 3) ** 2 - (Y - 3) ** 2) / 10) * 2 + np.exp((-(X - 3) ** 2 - (Y + 3) ** 2) / 10) * 1.2 + np.exp(
        -np.cos(X * 3) - np.sin(Y * 3)) / 5


# %%遗传算法
time_start = time.time()
dim = 2
iterate_times = 150
individual_n = 200
p_c = 0.4
p_m = 0.15
std_var = 20
num_range = [-100, 100]


def initialize(individual_n, num_range):
    return np.random.uniform(num_range[0], num_range[1], size=[individual_n, dim])


def overlapping(a, b, pc, dim):
    T = np.random.choice(a=2, size=dim, p=[1 - pc, pc])
    for i in range(dim):
        if T[i] == 1:
            a[i], b[i] = b[i], a[i]


def variation(a, pm, dim, num_range):
    T = np.random.choice(a=2, size=dim, p=[1 - pm, pm])
    for i in range(dim):
        if T[i] == 1:
            a[i] = np.clip(np.random.normal(loc=a[i], scale=std_var), num_range[0], num_range[1])


def get_select_p(v):
    exp_v = np.exp(v)
    sum_exp_v = np.sum(exp_v)
    return exp_v / sum_exp_v


def select_and_reproduction(population, num_range):
    values = func(population[:, 0], population[:, 1])
    select_p = get_select_p(values)

    choices = np.random.choice(a=len(population), size=len(population), replace=True, p=select_p)
    new_population = population[choices]
    for i in range(int(len(new_population) / 2)):
        overlapping(new_population[2 * i], new_population[2 * i + 1], p_c, dim)
        variation(new_population[2 * i], p_m, dim, num_range)
        variation(new_population[2 * i + 1], p_m, dim, num_range)
    argmax_value = np.argmax(values)
    return values[argmax_value], population[argmax_value], new_population


population = initialize(individual_n, num_range)
times_population = np.empty([iterate_times, individual_n, dim])
max_value = 0
max_value_coordinate = []
for i in range(iterate_times):
    times_population[i] = population
    last_max_value, last_max_value_pos, population = select_and_reproduction(population, num_range)
    if last_max_value > max_value:
        max_value = last_max_value
        max_value_coordinate = last_max_value_pos
    print(i, ":  ", last_max_value)

time_end = time.time()
print('总共耗时：', time_end - time_start)
print('迭代最大值：', max_value)
print('对应坐标：', max_value_coordinate)

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'ro', animated=True, color='black', markersize=2)


def init():
    ax.set_xlim(num_range[0], num_range[1])
    ax.set_ylim(num_range[0], num_range[1])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    return ln,


def update(frame):
    frame = int(frame)
    xdata = times_population[frame, :, 0]
    ydata = times_population[frame, :, 1]
    ln.set_data(xdata, ydata)
    return ln,


anim = animation.FuncAnimation(fig, update, frames=np.linspace(0, iterate_times - 1, iterate_times), interval=100,
                               init_func=init, blit=True)
plt.show()
