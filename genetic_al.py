import math
from random import random, randint, uniform
import matplotlib.pyplot as plt


def func(x, y):
    number = 6.432 * (x + 0.253 * y) * (math.cos(x) - math.cos(2 * y)) ** 2
    density = math.sqrt(0.8 + (x - 4.2) ** 2 + 2 * (y - 7) ** 2)
    return number / density + 3.226 * y


class GeneticAlgorithm:
    def __int__(self, func, populations, generations, Pc=0.85, Pm=0.06):
        self.func = func
        self.Pc = Pc
        self.Pm = Pm
        self.populations = populations
        self.generations = generations
        self.dec_number = 3
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

    def number_to_string(self, number):
        string = str(number).replace('.', '')
        string += '0' * abs(int(number) // 10 + 1 + self.dec_number - len(string))
        return string

    def encoder(self, x, y):
        char_list = []
        for i in range(len(x)):
            chra = self.number_to_string(x[i]) + self.number_to_string(y[i])
            char_list.append(chra)
        return char_list

    def string_to_number(self, something):
        number = int(something[: -self.dec_number]) + float(something[self.dec_number:]) / 10 ** self.dec_number
        return round(number, self.dec_number)

    def decoder(self, char):
        cut = int(len(char[0] / 2))
        ax = [self.string_to_number(char[i][:cut]) for i in range(len(char))]
        ay = [self.string_to_number(char[i][cut:]) for i in range(len(char))]
        return ax, ay

    def choose(self):
        something = sum(self.f)
        pourcentage = [self.f[i] / something for i in range(self.populations)]
        chosen = []
        for i in range(self.populations):
            cum = 0
            for j in range(self.populations):
                cum += pourcentage[j]
                if cum >= random():
                    chosen.append(self.chr[j])
                    break
        return chosen

    def crossover(self, char):
        crossed = []
        # if char is odd
        if len(char) % 2:
            crossed.append(char.pop())
        for i in range(0, len(char), 2):
            alpha = char[i]
            beta = char[i + 1]
            if random() < self.Pc:
                location = randint(1, len(char[i]) - 1)
                temp = alpha[location:]
                alpha = alpha[:location] + beta[location:]
                beta = alpha[:location] + temp
                # add to crossed
            crossed.append(alpha)
            crossed.append(beta)
        return crossed

    def mutation(self, char):
        res = []
        for i in char:
            the_list = list(i)
            for j in range(len(the_list)):
                # the 0.5 probability of mutation on each location
                if random() < self.Pm:
                    while True:
                        ratio = str(randint(0, 9))
                        if ratio != the_list[j]:
                            the_list[j] = ratio
                            break
            res.append("".join(the_list))
        return res

    def run(self):
        """initialization"""
        ax = []
        ay = []
        for i in range(self.populations):
            ax.append(round(uniform(0, 10), self.dec_number))
            ay.append(round(uniform(0, 10), self.dec_number))
        self.X = ax
        self.Y = ay
        self.chr = self.encoder(ax, ay)
        """Iterations"""
        for iteration in range(self.generations):
            self.f = [func(self.X[i], self.Y[i]) for i in range(self.populations)]
            fitness_sort = sorted(enumerate(self.f), key=lambda x: x[1], reverse=True)
            # first fitness rank[0]
            self.rank = [i[0] for i in fitness_sort]
            winner = self.f[self.rank[0]]
            self.history['f'].append(winner)
            self.history['x'].append(self.X[self.rank[0]])
            self.history['y'].append(self.Y[self.rank[0]])

            # choose crossover and mutations
            chosen = self.choose()
            crossed = self.crossover(chosen)
            self.chr = self.mutation(crossed)
            self.X, self.Y = self.decoder(self.chr)


if __name__ == "__main__":
    genetic_algo = GeneticAlgorithm(func, 10, 100)
    genetic_algo.run()
    plt.plot(genetic_algo.history['f'])
    plt.title("The fitness value")
    plt.xlabel("Iteration")
    plt.show()
