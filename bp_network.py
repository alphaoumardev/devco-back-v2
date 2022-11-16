import numpy as np


class BP_network:
    def __int__(self, input_num, hidden, output):
        self.hidden = hidden
        self.input_num = input_num
        self.output = output
        self.weight = np.random.uniform(-1, 1, (self.hidden, self.input_num))
        self.bias = np.zeros(1, self.hidden)
        self.weis = np.random.uniform(-1, 1, (self.output, self.hidden))
        self.bia = np.zeros(1, 1)

    @staticmethod
    def sigmoid(x):
        y = 1 / (1 + np.exp(-x))
        return y

    def forward(self, x):
        self.inputs = x
        self.hidden_out = np.dot(self.weight, x) + self.bias
        self.hidden_out = self.sigmoid(self.hidden_out)
        self.final_out = np.dot(self.weis, self.hidden_out.T) + self.bia
        return self.sigmoid(self.final_out)

    def backward(self, lrate, hat, exact_tag):
        yloss = -(exact_tag - hat)
        dydx_final = hat * (1 - hat)
        dldx_final = yloss * dydx_final

        self.bia -= lrate * dldx_final
        for i in range(self.hidden):
            dx_final_ldwi = self.hidden_out[0][i]
            dx_final_ldxi = self.weis[0][i]
            self.weis[0][i] -= lrate * dldx_final * dx_final_ldwi
            dxi_hidden_out = self.hidden_out[0][i] * (1 - self.hidden_out[0][i])
            self.bias[0][i] -= lrate * dldx_final * dx_final_ldxi * dxi_hidden_out
            for j in range(self.input_num):
                d_hidden_out_dwij = self.inputs[j]
                self.weight[i][j] -= lrate * dldx_final * dx_final_ldxi * dxi_hidden_out * d_hidden_out_dwij


if __name__ == '__main__':
    BP_network()
