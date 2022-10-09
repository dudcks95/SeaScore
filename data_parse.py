from datetime import date, timedelta
import requests
import pandas as pd
import numpy as np
# import json # requests에 내장 .json()이 있다
from bs4 import BeautifulSoup as bs


def daterange(start_date, end_date):  # 날짜 구하는 함수
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
day_list = [] # 총 리스트
for i in range(2012, 2023):  # 원하는 기간 배열로 생성
    year_list=[] # 1년단위로 끊기 위한 리스트
    start_date = date(i, 1, 1)  # 시작 날짜
    end_date = date(i+1, 1, 1)  # 끝 날짜의 다음 날
    for single_date in daterange(start_date, end_date):  
    #     print(single_date.strftime("%Y%m%d"))
        year_list.append(single_date.strftime("%Y%m%d")) # 날짜 형식 포맷
        year_list = [int(i) for i in year_list]  # str 형태를 int로 변환
        
    day_list.append(year_list)

print(day_list)

# 수온
a_list = []
for i in range(len(day_list)):
    for day in day_list[i]:     
            req = requests.get("https://www.khoa.go.kr/api/oceangrid/tidalBuTemp/search.do?ServiceKey=6tMtfhu2UhiktZk16RGGgA==&ObsCode=TW_0062&Date=%d&ResultType=json" %day)
            data = bs(req.text, 'html.parser')
            jsonData = req.json()

            result = []
            try:
                for i in jsonData.get("result").get("data"):
                    result.append(i['water_temp'])
            except Exception: # 중간에 비는 날이 있다면
                pass
            result_a = [float(i) for i in result] # 실수형으로 변환
#             for i in result_a:
#                 print(i)
            print(day,"-------------------------------------------")
            avg = np.round(np.mean(result_a),2)
            print(avg)
            a_list.append([day,avg])

print(a_list)
df1 = pd.DataFrame(a_list, columns=['날짜','수온'])
df1.to_csv('water_temp(2012~2022).csv', header='False', encoding='utf-8-sig')



# 파고
b_list = []
for i in range(len(day_list)):
    for day in day_list[i]:     
            req = requests.get("https://www.khoa.go.kr/api/oceangrid/obsWaveHight/search.do?ServiceKey=6tMtfhu2UhiktZk16RGGgA==&ObsCode=TW_0062&Date=%d&ResultType=json" %day)
            data = bs(req.text, 'html.parser')
            jsonData = req.json()

            result = []
            try:
                for i in jsonData.get("result").get("data"):
                    result.append(i['wave_height'])
            except Exception: # 중간에 비는 날이 있다면
                pass
            result_a = [float(i) for i in result]
            print(day,"-------------------------------------------")
            avg = np.round(np.mean(result_a),2)
            print(avg)
            b_list.append([avg])

print(b_list)

df2 = pd.DataFrame(b_list, columns=['파고'])
df2.to_csv('wave(2012~2022).csv', header='False', encoding='utf-8-sig')


# 풍속
c_list = []
for i in range(len(day_list)):
    for day in day_list[i]:     
            req = requests.get("http://www.khoa.go.kr/api/oceangrid/tidalBuWind/search.do?ServiceKey=6tMtfhu2UhiktZk16RGGgA==&ObsCode=TW_0062&Date=%d&ResultType=json" %day)
            data = bs(req.text, 'html.parser')
            jsonData = req.json()

            result = []
            try:
                for i in jsonData.get("result").get("data"):
                    result.append(i['wind_speed'])
            except Exception: # 중간에 비는 날이 있다면
                pass
            result_a = [float(i) for i in result]
            print(day,"-------------------------------------------")
            avg = np.round(np.mean(result_a),2)
            print(avg)
            c_list.append([day,avg])

print(c_list)

df3 = pd.DataFrame(c_list, columns=['day','wind'])
df3.to_csv('wind_speed(2012~2022).csv', header='False', encoding='utf-8-sig')


# 기온
d_list = []
for i in range(len(day_list)):
    for day in day_list[i]:     
            req = requests.get("http://www.khoa.go.kr/api/oceangrid/tidalBuAirTemp/search.do?ServiceKey=6tMtfhu2UhiktZk16RGGgA==&ObsCode=TW_0062&Date=%d&ResultType=json" %day)
            data = bs(req.text, 'html.parser')
            jsonData = req.json()

            result = []
            try:
                for i in jsonData.get("result").get("data"):
                    result.append(i['air_temp'])
            except Exception: # 중간에 비는 날이 있다면
                pass
            result_a = [float(i) for i in result]
            print(day,"-------------------------------------------")
            avg = np.round(np.mean(result_a),2)
            print(avg)
            d_list.append([day,avg])

print(d_list)

df4 = pd.DataFrame(d_list, columns=['day','wind'])
df4.to_csv('air_temp(2012~2022).csv', header='False', encoding='utf-8-sig')

# dataframe 병합
df_all = pd.concat([df1,df2,df3,df4],axis=1)
df_all.to_csv('sea_data(2012~2022).csv', header='False', encoding='utf-8-sig')

# 지수 리스트   
req = requests.get("https://www.khoa.go.kr/api/oceangrid/fcIndexOfType/search.do?ServiceKey=6tMtfhu2UhiktZk16RGGgA==&Type=BE&ResultType=json")
data = bs(req.text, 'html.parser')
jsonData = req.json()

d_list = []
try:
    for i in jsonData.get("result").get("data"):
        
        print(i)
        print(i['date'])
        print("------------------------------")
        
        result = []
        result.append(i['date'])
        result.append(i['time_type'])
        result.append(i['name'])
        result.append(i['air_temp'])
        result.append(i['water_temp'])
        result.append(i['wave_height'])
        result.append(i['total_score'])
        d_list.append(result)
except Exception: # 중간에 비는 날이 있다면
    pass
print(d_list)

df4 = pd.DataFrame(d_list, columns=['날짜','오전/오후','위치','기온','수온','파고','해수욕지수'])
df4.to_csv('swim.csv', header='False', encoding='utf-8-sig')
