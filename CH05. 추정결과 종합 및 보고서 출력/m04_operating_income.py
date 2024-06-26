import pandas as pd

from m01_assumption import assumption
from m02_index import index


operating_income = {}

#### 1. 객실별 운영수입 계산
room_type_list = list(assumption['business_overview']['객실수'].keys())
for room_type in room_type_list:
    data = []
    for dt in index['model']:
        dct = {}

        if dt in index['operating']:
            # 총객실수
            dct['총객실수'] = (
                assumption['business_overview']['객실수'][room_type] *
                index['days'].loc[dt, '월간일수']
            )

            # 사용불가객실수(대수선 기간)
            if dt in index['수선' + room_type]:
                dct['사용불가객실수'] = (
                    assumption['business_overview']['객실수'][room_type] *
                    index['days'].loc[dt, '월간일수']
                )
            else:
                dct['사용불가객실수'] = 0

            # 판매가능객실수
            dct['판매가능객실수'] = dct['총객실수'] - dct['사용불가객실수']

            # 객실판매비율(OCC rate)
            dct['객실판매비율'] = assumption['monthly_occ_rate'][room_type][dt.month]

            # 판매객실수
            dct['판매객실수'] = round(dct['판매가능객실수'] * dct['객실판매비율'])

            # 판매단가
            dct['판매단가'] = assumption['monthly_price'][room_type][dt.month]

            # 객실수입
            dct['객실수입'] = dct['판매객실수'] * dct['판매단가']
        else:
            dct['총객실수'] = 0
            dct['사용불가객실수'] = 0
            dct['판매가능객실수'] = 0
            dct['객실판매비율'] = 0.0
            dct['판매객실수'] = 0
            dct['판매단가'] = 0
            dct['객실수입'] = 0

        data.append(dct)
    operating_income[room_type] = pd.DataFrame(data, index=index['model'])


#### 2. 운영수입 합계 계산
data = {}
data['총객실수'] = (
    operating_income['TypeA']['총객실수']
    + operating_income['TypeB']['총객실수'] 
    + operating_income['TypeC']['총객실수']
)
data['사용불가객실수'] = (
    operating_income['TypeA']['사용불가객실수']
    + operating_income['TypeB']['사용불가객실수'] 
    + operating_income['TypeC']['사용불가객실수']
)
data['판매가능객실수'] = (
    operating_income['TypeA']['판매가능객실수']
    + operating_income['TypeB']['판매가능객실수'] 
    + operating_income['TypeC']['판매가능객실수']
)
data['판매객실수'] = (
    operating_income['TypeA']['판매객실수']
    + operating_income['TypeB']['판매객실수'] 
    + operating_income['TypeC']['판매객실수']
)
data['객실수입'] = (
    operating_income['TypeA']['객실수입']
    + operating_income['TypeB']['객실수입'] 
    + operating_income['TypeC']['객실수입']
)
data['객실판매비율'] = pd.Series(
    [(data['판매객실수'].loc[idx] / data['판매가능객실수'].loc[idx]
        if data['판매가능객실수'].loc[idx] != 0
        else 0
        ) for idx in index['model']
    ],
    index = index['model']
)
data['판매단가'] = pd.Series(
    [(int(round(data['객실수입'].loc[idx] / data['판매객실수'].loc[idx]))
        if data['판매객실수'].loc[idx] != 0
        else 0
        ) for idx in index['model']
    ],
    index = index['model']
)

df_temp = pd.DataFrame(data)
df_temp = df_temp[['총객실수', '사용불가객실수', '판매가능객실수', '객실판매비율', '판매객실수', '판매단가', '객실수입']]

operating_income['Total'] = df_temp