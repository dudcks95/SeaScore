import pandas as pd
import numpy as np

class Calc_score : 
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


    #풍속
    def calc_wind(self, n):
        weight = 1
        if 2 > n : return weight * 5/5
        elif 5 > n >= 2 : return weight * 4/5
        elif 8 > n >= 5 : return weight * 3/5
        elif 10 > n >= 8 : return weight * 2/5
        elif n >= 10 : return weight * 1/5

    # 강수량 확인
    def calc_rain(self, n):
        if -1 : return 0
        elif 1.0 > n >= 0 : return 10
        elif n >= 1 : return 20

    # 해수욕지수
    def result_score(self, n):
        if n >= 20 return 1 # 강수량이 1mm 이상
        elif n >= 10 return 2 # 강수량이 0~1mm
        elif n >= 3 : return 3 
        elif 3 > n >= 2 : return 2
        elif 2 > n : return 1

    def calc_all(self, file):
        df = pd.read_csv(file, encoding='utf-8') # csv로 일단 받음
        df_water_temp=df['수온'].apply(lambda x : calc_water_temp(x))
        df_digging=df['파고'].apply(lambda x : calc_digging(x))
        df_air_temp=df['기온'].apply(lambda x : calc_air_temp(x))
        df_wind=df['풍속'].apply(lambda x : calc_wind(x))
        df_rain=df['강수량'].apply(lambda x : calc_rain(x))

        df_water_temp= df_water_temp.rename("수온계산결과")
        df_digging= df_digging.rename("파고계산결과")
        df_air_temp= df_air_temp.rename("기온계산결과")
        df_wind= df_wind.rename("풍속계산결과")
        df_rain= df_rain.rename("강수량계산결과")

        df_list = [df, df_water_temp, df_digging, df_air_temp, df_wind, df_rain]
        df= pd.concat(df_list, axis=1)
        

        df_sum = df_water_temp+df_digging+df_air_temp+df_wind+df_rain
        df_sum = df_sum.rename("결과합계")
        df =pd.concat([df,df_sum], axis=1)
        
        df_result=df['결과합계'].apply(lambda x : result_score(x))
        df_result= df_result.rename("해수욕지수")
        return df

calc_score = Calc_score()
calc_score.calc_all('해운대.csv')

        
