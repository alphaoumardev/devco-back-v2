import math
import matplotlib.pyplot as plt
from random import random, randint, uniform


def func(x, y):
    num = 6.452 * (x + 0.125 * y) * (math.cos(x) - math.cos(2 * y)) ** 2
    den = math.sqrt(0.8 + (x - 4.2) ** 2 + 2 * (y - 7) ** 2)
    return num / den + 3.226 * y


class GeneticAlgorithm:
    def __init__(self, function, M, gen, Pc=0.85, Pm=0.05):
        """
        :param function: fitness function
        :param M: population
        :param gen: total generations
        :param Pc: probability of crossover
        :param Pm: probability of mutation
        """
        self.func = function
        self.Pc = Pc
        self.Pm = Pm
        self.M = M
        self.gen = gen
        self.dec_num = 3
        self.X = []
        self.Y = []
        self.chr = []
        self.f = []
        self.rank = []
        self.history = {
            'f': [],
            'x': [],
            'y': []
        }

    def num2str(self, num):
        # return str(int(num)) + str(int(num - int(num)) * 1e3)
        s = str(num).replace('.', '')
        s += '0' * abs(int(num) // 10 + 1 + self.dec_num - len(s))
        return s

    def encoder(self, x, y):
        chr_list = []
        for i in range(len(x)):
            chrs = self.num2str(x[i]) + self.num2str(y[i])
            chr_list.append(chrs)
        return chr_list

    def str2num(self, s):
        num = int(s[:-self.dec_num]) + float(s[-self.dec_num:]) / 10 ** self.dec_num
        return round(num, self.dec_num)

    def decoder(self, chr):
        cut = int(len(chr[0]) / 2)
        x = [self.str2num(chr[i][:cut]) for i in range(len(chr))]
        y = [self.str2num(chr[i][cut:]) for i in range(len(chr))]
        return x, y

    def choose(self):
        # calculate percentage
        s = sum(self.f)
        p = [self.f[i] / s for i in range(self.M)]
        chosen = []
        # choose M times
        for i in range(self.M):
            cum = 0
            m = random()
            # Roulette
            for j in range(self.M):
                cum += p[j]
                if cum >= m:
                    chosen.append(self.chr[j])
                    break
        return chosen

    def crossover(self, chr):
        crossed = []
        # if chr list is odd
        if len(chr) % 2:
            crossed.append(chr.pop())
        for i in range(0, len(chr), 2):
            a = chr[i]
            b = chr[i + 1]
            # 0.85 probability of crossover
            if random() < self.Pc:
                loc = randint(1, len(chr[i]) - 1)
                temp = a[loc:]
                a = a[:loc] + b[loc:]
                b = b[:loc] + temp
            # add to crossed
            crossed.append(a)
            crossed.append(b)
        return crossed

    def mutation(self, chr):
        res = []
        for i in chr:
            l = list(i)
            for j in range(len(l)):
                # 0.05 probability of mutation on each location
                if random() < self.Pm:
                    while True:
                        r = str(randint(0, 9))
                        if r != l[j]:
                            l[j] = r
                            break
            res.append(''.join(l))
        return res

    def run(self):
        # initialization
        x = []
        y = []
        for i in range(self.M):
            x.append(round(uniform(0, 10), self.dec_num))
            y.append(round(uniform(0, 10), self.dec_num))
        self.X = x
        self.Y = y
        self.chr = self.encoder(x, y)
        # iteration
        for iter in range(self.gen):
            self.f = [func(self.X[i], self.Y[i]) for i in range(self.M)]
            fitness_sort = sorted(enumerate(self.f), key=lambda x: x[1], reverse=True)
            # 1st : fitness[rank[0]]
            self.rank = [i[0] for i in fitness_sort]
            winner = self.f[self.rank[0]]
            print(f'Iter={iter + 1}, Max-Fitness={winner}')
            # save to history
            self.history['f'].append(winner)
            self.history['x'].append(self.X[self.rank[0]])
            self.history['y'].append(self.Y[self.rank[0]])
            # choose, crossover and mutation
            chosen = self.choose()
            crossed = self.crossover(chosen)
            self.chr = self.mutation(crossed)
            self.X, self.Y = self.decoder(self.chr)


if __name__ == '__main__':
    # run
    ga = GeneticAlgorithm(func, 10, 100)
    ga.run()
    # plot
    plt.plot(ga.history['f'])
    plt.title('Fitness value')
    plt.xlabel('Iter')
    plt.show()
