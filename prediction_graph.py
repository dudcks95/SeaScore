from sklearn.preprocessing import RobustScaler
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings 

rb = RobustScaler()
df_train = pd.read_csv('water_temp(2012~2022)_full.csv', encoding='utf-8-sig')
df_train = df_train[['day','water_temp']]

# 숫자를 문자로 변경후 날짜 정보로 변경



# df['날짜']
for i in df_train['day'] :
    day = str(i)
    day = datetime.strptime(day, '%Y%m%d')
    print(type(day))
#     df_train = df_train.loc[df_train['날짜']==i, '날짜'] == day
    df_train = df_train.replace(i, day)
    
df_train.columns = ['day','water_temp']
df_train = df_train.interpolate(method='linear',limit_direction='forward')
df_train['day'] = pd.to_datetime(df_train['day'])

df_train.index = df_train['day']
df_train.set_index('day', inplace=True)

water_temp_scaled = rb.fit_transform(df_train[['water_temp']])
df_train['water_temp'] = water_temp_scaled
print(df_train.head()) # 스케일링 결과 확인(-1~1 사이의 값으로 스케일링)

# train, test set 분리
test_size = 100 # data split size
train_data = df_train[:-test_size]
test_data = df_train[-test_size:]

# 당일 데이터 예측에 +n일의 과거 데이터를 반영한다.
import pandas as pd
window_size = 15 # 예측에 반영할 과거 데이터 일수
for i in range(1, 15) :
    train_data[f'water_temp_{i}'] = train_data['water_temp'].shift(i)
    test_data[f'water_temp_{i}'] = test_data['water_temp'].shift(i)
        # train, test 데이터를 하루 씩 옮기면서 과거 데이터를 형성

# 데이터 확인
print(train_data.head(3))


# 과거 데이터가 채워지지 않으면 drop함
train_data.dropna(inplace=True)
X_train = train_data.drop('water_temp', axis=1)
y_train = train_data[['water_temp']]
test_data.dropna(inplace=True)
X_test = test_data.drop('water_temp', axis=1)
y_test = test_data[['water_temp']]

# train, test 사이즈를 확인하고, 신경망 학습을 위해 reshape한다
X_train= X_train.values
X_test= X_test.values
y_train = y_train.values
y_test = y_test.values
print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)


X_train = X_train.reshape(X_train.shape[0], 14, 1 )
X_test= X_test.reshape(X_test.shape[0], 14, 1 )

# *-- 신경망 생성 --*
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras import backend as K
K.clear_session()

model = Sequential()
model.add(LSTM(14, return_sequences = True, input_shape = (14, 1)))
model.add(LSTM(28, return_sequences=False))
model.add(Dense(3, activation='linear'))

model.compile(loss='mean_squared_error', optimizer='adam')
model.summary()

# 모델 학습
es = EarlyStopping(monitor='loss', patience=5, verbose= 1)
model.fit(X_train, y_train, epochs = 50, batch_size=16, verbose=1,
         callbacks=[es])

# 모델 예측
y_pred = model.predict(X_test)

# *-- 결과 시각화 --*
# 예측 결과와 실제 값을 시각화
y_test_val = pd.DataFrame(y_test, index=test_data.index)
y_pred_val = pd.DataFrame(y_pred, index=test_data.index)

import matplotlib.pyplot as plt
ax1 = y_test_val.plot()
y_pred_val.plot(ax=ax1)
plt.legend(['test','pred'])
