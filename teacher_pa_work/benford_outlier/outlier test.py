# -*- encoding:utf-8 -*-
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.datasets import load_boston

class OutlierTest(object):
    '''
    calculate 5 index values which test  if points are outlier
    '''
    def __init__(self, GDP, K, L):
        '''
        input train data, create new data(date), and model error
        Y=ln(GDP/L), X1=ln(K/L), X2=T=range(1,len(date));
        b1=资金投入弹性系数, b2=技术进步率, b0=ln(初始技术水平);
        :param GDP: GDP(List)
        :param K: Capital investment(List)
        :param L: Labor input(List)
        '''
        self.GDP = np.array(GDP)
        self.K = np.array(K)
        self.L = np.array(L)
        self.train_data_tranlate()
        self.hii_list = self.hii()      # calculate leverage value list
        self.fit_LinearRegression()


    def train_data_tranlate(self):
        '''
        translate X and Y, to fit the linear Regression
        '''
        self.Y = np.log(np.array(self.GDP)/np.array(self.L))
        self.n = len(self.Y)                 # get the number of date
        X1 = np.log(self.K/self.L)
        X2 = np.arange(1, self.n+1)
        self.X = np.array([X1, X2]).T


    def hii(self):
        '''
        Calculate the leverage value of each training data
        :return: leverage value (np.array)
        '''
        X_mat = np.mat(self.X)       # translate matrix
        H_mat = X_mat * (X_mat.T * X_mat).I * X_mat.T
        return np.diag(H_mat)


    def fit_LinearRegression(self):
        '''
        fit LinearRegression to calculate model error
        '''
        model = LinearRegression(fit_intercept=True)
        model.fit(self.X, self.Y)
        Y_predict = model.predict(self.X)
        self.para = model.coef_             # Linear regression parameters

        # calculate error and std(error)
        self.model_error = self.Y - Y_predict
        self.error_std = np.std(self.model_error)


    def r_t_wk(self, index):
        '''
        calculate Studentized residual, kw values
        Studentized residuals(r), Student external residual(t)
        :param: index(int) sample index, 0->n
        :return: r, t, kw (3 len list)
        '''
        r = self.model_error[index]/(self.error_std * np.sqrt(1 - self.hii_list[index]))
        t = np.sqrt( (self.n - 3) * np.power(r, 2) / (self.n - 2 - np.power(r,2)) )
        wk = np.sqrt(self.hii_list[index] / (1 - self.hii_list[index])) * t
        return r, t, wk


    def cook(self, index):
        '''
        calculate cook values
        :param index: index(int) sample index
        :return: cook value(int), 0->n
        '''
        model = LinearRegression(fit_intercept=True)
        model.fit(np.delete(self.X, index, 0), np.delete(self.Y, index))
        new_para = np.mat(model.coef_)
        cook = (new_para-np.mat(self.para)) * np.mat(self.X).T * np.mat(self.X) * \
               (new_para-np.mat(self.para)).T / (2 * np.var(self.model_error))
        return float(cook)


    def calculate_all_index(self, index):
        '''
        Integrate all statistical indicators, [r, t, wk, cook]
        :param index: index(int) sample index
        :return: [r, t, wk, h, cook](list)
        '''
        index_value = [self.r_t_wk(index)[1], self.cook(index), self.hii_list[index], self.r_t_wk(index)[2]]
        return [round(i,2) for i in index_value]


if __name__ == "__main__":
    data = '''198783.1
    827121.7
    592539.5
    380944
    180385.3
    743585.5
    532434
    342071.4
    161456.3
    689052.1
    496200.2
    319489.7
    150986.7
    643974
    462791.5
    297079.7
    140618.3
    595244.4
    426619.3
    273713.9
    129747
    7815
    25974
    19342
    12932
    7184
    23821
    17735
    11886
    6619
    21966
    16367
    10931
    6087
    20167
    14986
    10025
    5562
    18311
    13557
    9049
    5006
    '''
    data = [float(i) for i in data.strip().split("\n")]
    x = data[:21][::-1]
    y = data[21:][::-1]
    a = OutlierTest(y, x, np.ones(len(x)))
    for i in range(len(x)):
        print(a.calculate_all_index(i))

























