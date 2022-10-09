import pandas as pd
import numpy as np

class calc_first : 
    # 수온
    def calc_water_temp(self, n):
        weight = 0.7
        if n >= 24 : return weight * 5/5
        elif 24 > n >= 22 : return weight * 4/5
        elif 22 > n >= 21 : return weight * 3/5
        elif 21 > n >= 20: return weight * 2/5
        elif 20 > n : return weight * 1/5


    #파고 
    def calc_digging(self, n):
        weight = 2
        if 0.5 > n : return weight * 5/5
        elif 0.5 > n >= 1.0 : return weight * 4/5
        elif 1.0 > n >= 1.3 : return weight * 3/5
        elif 1.3 > n >= 1.7 : return weight * 2/5
        elif n >= 1.7 : return weight * 1/5

    #기온
    def calc_air_temp(self, n):
        weight = 0.3
        if n >= 30 : return weight * 5/5
        elif 30 > n >= 27 : return weight * 4/5
        elif 27 > n >= 25 : return weight * 3/5
        elif 25 > n >= 22 : return weight * 2/5
        elif 22 > n : return weight * 1/5


    #강수량
    def calc_rain(self, n):
        weight = 1.9
        if n == -1 : return weight * 5/5
        elif n == 0 : return weight * 4/5
        elif 0.1 > n : return weight * 3/5
        elif 1.0 > n : return weight * 2/5
        elif 1.0 <= n : return weight * 1/5



    #풍속
    def calc_wind(self, n):
        weight = 1
        if 2 >= n : return weight * 5/5
        elif 5 >= n > 2 : return weight * 4/5
        elif 8 >= n > 5 : return weight * 3/5
        elif 10 >= n > 8 : return weight * 2/5
        elif n > 10 : return weight * 1/5


    # 해수욕지수
    def result_score(self, n):
        if n >= 5.5 : return 5
        elif 5.5 > n >= 4 : return 4
        elif 4 > n >= 3 : return 3
        elif 3 > n >= 1.5 : return 2
        elif 1.5 > n : return 1

    def calc_all(self):
        if df['강수량'].apply(lambda x : calc_rain(x)) : 
        df_water_temp=df['수온'].apply(lambda x : calc_water_temp(x))
        df_digging=df['파고'].apply(lambda x : calc_digging(x))
        df_air_temp=df['기온'].apply(lambda x : calc_air_temp(x))
        df_rain=df['강수량'].apply(lambda x : calc_rain(x))
        df_wind=df['풍속'].apply(lambda x : calc_wind(x))

        df_water_temp= df_water_temp.rename("수온계산결과")
        df_digging= df_digging.rename("파고계산결과")
        df_air_temp= df_air_temp.rename("기온계산결과")
        df_rain= df_rain.rename("강수량계산결과")
        df_wind= df_wind.rename("풍속계산결과")

        df_list = [df, df_water_temp, df_digging, df_air_temp, df_rain, df_wind]
        df= pd.concat(df_list, axis=1)
        

        df_sum = df_water_temp+df_digging+df_air_temp+df_rain+df_wind
        df_sum = df_sum.rename("결과합계")
        df =pd.concat([df,df_sum], axis=1)

        df_result=df['결과합계'].apply(lambda x : result_score(x))
