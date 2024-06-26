import pandas as pd
from datetime import timedelta

from m00_general_function import (
    list_end_of_months,
    calculate_inflation_rate,
)
from m01_assumption import assumption


#### 1. 기간인덱스
index = {}

index["model"] = list_end_of_months(
    assumption['period_assumptions']['기본기간가정']['모델시작일'],
    assumption['period_assumptions']['기본기간가정']['모델종료일']
)

index["operating"] = list_end_of_months(
    assumption['period_assumptions']['기본기간가정']['운영시작일'],
    assumption['period_assumptions']['기본기간가정']['운영종료일']
)

index["이자지급"] = list_end_of_months(
    assumption['period_assumptions']['자금조달일정']['이자지급시작일'],
    assumption['period_assumptions']['자금조달일정']['이자지급종료일']
)

index["원금상환"] = list_end_of_months(
    assumption['period_assumptions']['자금조달일정']['원금상환시작일'],
    assumption['period_assumptions']['자금조달일정']['원금상환종료일']
)

index["수선TypeA"] = list_end_of_months(
    assumption['facility_cost']['수선시작일']['TypeA'],
    assumption['facility_cost']['수선종료일']['TypeA']
)

index["수선TypeB"] = list_end_of_months(
    assumption['facility_cost']['수선시작일']['TypeB'],
    assumption['facility_cost']['수선종료일']['TypeB']
)

index["수선TypeC"] = list_end_of_months(
    assumption['facility_cost']['수선시작일']['TypeC'],
    assumption['facility_cost']['수선종료일']['TypeC']
)


#### 2. 연간인상률 인덱스
base_year = assumption['period_assumptions']['기본기간가정']['운영시작일'].year

data = []
for dt in index['model']:
    dct = {}
    dct['판매단가'] = calculate_inflation_rate(
        dt.year, 
        base_year, 
        assumption['period_assumptions']['연간인상률']['판매단가']
    )
    dct['운영비'] = calculate_inflation_rate(
        dt.year, 
        base_year, 
        assumption['period_assumptions']['연간인상률']['운영비']
    )
    dct['인건비'] = calculate_inflation_rate(
        dt.year, 
        base_year, 
        assumption['period_assumptions']['연간인상률']['인건비']
    )
    data.append(dct)
index["연간인상률"] = pd.DataFrame(data, index=index['model'])


#### 3. 기간별 계산일수
data = []
for dt in index['model']:
    dct = {}
    dct['월간일수'] = (dt - dt.replace(day=1) + timedelta(days=1)).days
    dct['연간일수'] = 366 if dt.year % 4 == 0 else 365
    data.append(dct)
index["days"] = pd.DataFrame(data, index=index['model'])