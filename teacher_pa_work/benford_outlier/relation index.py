# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_white
from statsmodels.stats.stattools import durbin_watson


class relation_index():
    '''
    对输入的数据计算对应的指标, 并检验是否存在异常值.
    1. 先检验模型的残差是否有自相关性, 若有, 则修正; 若没有, 不做任何处理
    2. 计算对应方程的相关指标
    3. 计算得到所有异常点
    '''
    def __init__(self, X, y):
        '''
        :param X: array-like, GDP
        :param y: array-like, 居民人均收入
        '''
        self.X = X
        self.y = y
        self.para_dict = {}     # 参数字典属性


    def dw_test_correction(self):
        '''
        检验拟合的回归方程残差是否有自相关性
        '''
        results = self.fit_LinearRegression(self.X, self.y)     # 拟合方程
        self.coef_p_rsqr_white_values(results)      # 填充参数字典
        dw = self.dw_test(self.X, self.y)          # 计算dw统计量

        self.para_dict = {}

        # 对X, y进行差分转化
        n = len(self.y)
        p = (np.power(n, 2) * (1 - dw/2) + 4) / (np.power(n, 2) - 4)
        y_new = np.array([self.y[i+1]-self.y[i]*p  for i in range(n-1)])
        X_new = np.array([self.X[i+1]-self.X[i]*p  for i in range(n-1)])

        # 拟合修正方程, 填充参数字典
        corr_results = self.fit_LinearRegression(X_new, y_new)
        self.coef_p_rsqr_white_values(corr_results)
        # 修改回归方程系数
        self.dw_test(X_new, y_new)          # 添加新的DW值
        self.para_dict["const_coef"] /= (1 - p)
        self.para_dict["corr_coef"] = p

        # 检验异常值
        self.outlier = self.outlier_test(results)


    def fit_LinearRegression(self, x, y):
        '''
        进行线性回归方程的拟合
        :param x: array-like (1,)
        :param y: array-like (1,)
        :return: OLS的拟合结果，方便后续调用
        '''
        x_extant = sm.add_constant(x)
        results = sm.OLS(y, x_extant).fit()
        return results


    def coef_p_rsqr_white_values(self, results):
        '''
        对参数字典进行数据填充
        '''
        white = het_white(results.resid, exog=results.model.exog)[1]
        self.para_dict["f_p"] = results.f_pvalue
        self.para_dict["const_coef"] = results.params[0]
        self.para_dict["x1_coef"] = results.params[1]
        self.para_dict["const_p"] = results.pvalues[0]
        self.para_dict["x1_p"] = results.pvalues[1]
        self.para_dict["r_squared"] = results.rsquared_adj
        self.para_dict["white_p"] = white


    def dw_test(self, x, y):
        '''
        计算dw统计量, 并存入参数字典.
        :param X: array-like, GDP
        :param y: array-like, 居民人均收入
        :return: float, dw_value
        '''
        x1 ,const = self.para_dict["x1_coef"], self.para_dict["const_coef"]
        error = y - (x * x1 + const)
        dw = durbin_watson(error)
        self.para_dict["dw_value"] = dw
        return dw


    def outlier_test(self, results):
        '''
        离群值检验
        :param results: OLS.fit()
        :return: (DataFrame). 包含所有异常值统计量，以及是否为异常值的列. 0(非), 1(是)
        '''
        # 计算异常值检验的统计量
        outliers = results.get_influence()
        leverage = outliers.hat_matrix_diag         # 杠杆值
        resid_stu = outliers.resid_studentized_external         # 学生化残差
        cook = outliers.cooks_distance[0]           # cook距离
        w_k = outliers.dffits[0]           # w-k统计量
        outlier_df = pd.DataFrame({"ti":resid_stu, "cook":cook, "hi":leverage, "wk":w_k})
        outlier_df = outlier_df.applymap(lambda x: round(x, 2))         # 结果保留两位小数

        # 检验是否是异常值, n为数据量, k为解释变量个数, 这里k=1.
        n = len(self.y)
        outlier_df["ti_is_outlier"] = [1 if np.abs(i)>1.729 else 0 for i in outlier_df["ti"]]           # t(n-k-1)=t(19)
        outlier_df["cook_is_outlier"] = [1 if i > 4/n else 0 for i in outlier_df["cook"]]           # 4/n
        outlier_df["hi_is_outlier"] = [1 if i > (2/n) else 0 for i in outlier_df["hi"]]         # 2*k/n
        outlier_df["wk_is_outlier"] = [1 if i > 2*np.sqrt(2/n) else 0 for i in outlier_df["wk"]]            # 2*sqrt((k+1)/n)
        return outlier_df


    def output(self):
        '''
        输出参数 DataFrame
        '''
        self.dw_test_correction()
        df_output = pd.Series(self.para_dict).apply(lambda x: round(x, 2))
        return df_output


if __name__ == "__main__":
    data = pd.read_excel("C:/Users/Administrator/Desktop/111.xls", encoding="utf-8", sheet_name=4)
    data.fillna(method="ffill", inplace=True)

    txtfile = open("C:/Users/Administrator/Desktop/111.txt", 'w')
    x = np.log(np.array(data["GDP"]))
    y_city = np.log(np.array(data["城镇"]))
    y_side = np.log(np.array(data["农村"]))
    y_mean = np.log(np.array(data["居民"]))
    a_city = relation_index(x, y_city)
    a_side = relation_index(x, y_side)
    a_mean = relation_index(x, y_mean)
    b_city = a_city.output()
    b_side = a_side.output()
    b_mean = a_mean.output()
    print(b_city)  # 输出表1
    a_city.outlier[::-1].to_csv("C:/Users/Administrator/Desktop/outlier1.csv", encoding="utf-8", index=False)
    formula1 = '''log(yt) = {} + {} * log(xt) + et
                    et = {} * et-1 + ut'''.format(b_city["const_coef"], b_city["x1_coef"], b_city["corr_coef"])
    txtfile.write('城市居民收入：' + formula1 + "\n")

    print(b_side)  # 输出表1
    a_side.outlier[::-1].to_csv("C:/Users/Administrator/Desktop/outlier2.csv", encoding="utf-8", index=False)
    formula2 = '''log(yt) = {} + {} * log(xt) + et
                    et = {} * et-1 + ut'''.format(b_side["const_coef"], b_side["x1_coef"], b_side["corr_coef"])
    txtfile.write('农村居民收入：' + formula2 + "\n")

    print(b_mean)  # 输出表1
    a_mean.outlier[::-1].to_csv("C:/Users/Administrator/Desktop/outlier3.csv", encoding="utf-8", index=False)
    formula3 = '''log(yt) = {} + {} * log(xt) + et
                    et = {} * et-1 + ut'''.format(b_mean["const_coef"], b_mean["x1_coef"], b_mean["corr_coef"])
    txtfile.write('居民收入：' + formula3 + "\n")

    txtfile.close()

    # # 输出重要的数据
    # txtfile = open("C:/Users/Administrator/Desktop/111.txt", 'w')
    # convince = ["北京","江苏","浙江","山东","湖北","青海","新疆"]
    # for con in convince:
    #     x = np.log(np.array(data.loc[data["地区"]==con, "GDP"]))
    #     y_cost = np.log(np.array(data.loc[data["地区"]==con, "支出"]))
    #     y_in = np.log(np.array(data.loc[data["地区"]==con, "收入"]))
    #     a_cost = relation_index(x, y_cost)
    #     a_in = relation_index(x, y_in)
    #     b_cost = a_cost.output()
    #     b_in = a_in.output()
    #     print("{}......................收入..................".format(con))
    #     print(b_in)        # 输出表1
    #     print("log(y) = {} + {} * log(x)".format(b_in["const_coef"], b_in["x1_coef"]))
    #     print()
    #     print("{}......................支出..................".format(con))
    #     print(b_cost)        # 输出表1
    #
    #     a_in.outlier[::-1].to_csv("C:/Users/Administrator/Desktop/data/{}outlier_收入.csv".format(con), encoding="utf-8", index=False)
    #     a_cost.outlier[::-1].to_csv("C:/Users/Administrator/Desktop/data/{}outlier_支出.csv".format(con), encoding="utf-8", index=False)
    #
    #     formula_in = '''log(yt) = {} + {} * log(xt) + et
    #                     et = {} * et-1 + ut'''.format(b_in["const_coef"], b_in["x1_coef"], b_in["corr_coef"])
    #     txtfile.write('{}农村居民收入：'.format(con) + formula_in + "\n")
    #     formula_cost = '''log(yt) = {} + {} * log(xt) + et
    #                     et = {} * et-1 + ut'''.format(b_cost["const_coef"], b_cost["x1_coef"], b_cost["corr_coef"])
    #     txtfile.write('{}农村居民支出：'.format(con) + formula_cost + "\n")
    # txtfile.close()



