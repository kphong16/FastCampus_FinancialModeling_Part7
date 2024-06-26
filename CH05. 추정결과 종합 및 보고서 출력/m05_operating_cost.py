import pandas as pd

from m00_general_function import subtotal
from m01_assumption import assumption
from m02_index import index
from m04_operating_income import operating_income


operating_cost = {}

#### 1. 객실운영비
operating_cost['객실운영비'] = {}

## 1-1. 청소세탁비
data = []
for dt in index['model']:
    dct = {}
    dct['TypeA'] = int(
        operating_income['TypeA'].loc[dt, '판매객실수'] * 
        assumption['room_operating_cost']['청소세탁비']['TypeA'] *
        index['연간인상률'].loc[dt, '운영비']
    )
    dct['TypeB'] = int(
        operating_income['TypeB'].loc[dt, '판매객실수'] * 
        assumption['room_operating_cost']['청소세탁비']['TypeB'] *
        index['연간인상률'].loc[dt, '운영비']
    )
    dct['TypeC'] = int(
        operating_income['TypeC'].loc[dt, '판매객실수'] * 
        assumption['room_operating_cost']['청소세탁비']['TypeC'] *
        index['연간인상률'].loc[dt, '운영비']
    )
    dct['Total'] = dct['TypeA'] + dct['TypeB'] + dct['TypeC']
    data.append(dct)

operating_cost['객실운영비']['청소세탁비'] = pd.DataFrame(data, index=index['model'])


## 1-2. 수도광열비
data = []
for dt in index['model']:
    dct = {}
    dct['TypeA'] = int(
        operating_income['TypeA'].loc[dt, '판매객실수'] * 
        assumption['room_operating_cost']['수도광열비']['TypeA'] *
        index['연간인상률'].loc[dt, '운영비']
    )
    dct['TypeB'] = int(
        operating_income['TypeB'].loc[dt, '판매객실수'] * 
        assumption['room_operating_cost']['수도광열비']['TypeB'] *
        index['연간인상률'].loc[dt, '운영비']
    )
    dct['TypeC'] = int(
        operating_income['TypeC'].loc[dt, '판매객실수'] * 
        assumption['room_operating_cost']['수도광열비']['TypeC'] *
        index['연간인상률'].loc[dt, '운영비']
    )
    dct['Overhead'] = int(
        assumption['room_operating_cost']['수도광열비']['Overhead'] *
        index['연간인상률'].loc[dt, '운영비']
    )
    dct['Total'] = (
        dct['TypeA'] + 
        dct['TypeB'] + 
        dct['TypeC'] +
        dct['Overhead']
    )
    data.append(dct)

operating_cost['객실운영비']['수도광열비'] = pd.DataFrame(data, index=index['model'])


## 1-3. 예약수수료
data = []
for dt in index['model']:
    dct = {}
    dct['TypeA'] = int(
        operating_income['TypeA'].loc[dt, '객실수입'] * 
        assumption['room_operating_cost']['예약수수료율']['TypeA']
    )
    dct['TypeB'] = int(
        operating_income['TypeB'].loc[dt, '객실수입'] * 
        assumption['room_operating_cost']['예약수수료율']['TypeB']
    )
    dct['TypeC'] = int(
        operating_income['TypeC'].loc[dt, '객실수입'] * 
        assumption['room_operating_cost']['예약수수료율']['TypeC']
    )
    dct['Total'] = dct['TypeA'] + dct['TypeB'] + dct['TypeC']
    data.append(dct)

operating_cost['객실운영비']['예약수수료'] = pd.DataFrame(data, index=index['model'])


## 1-4. SubTotal
operating_cost['객실운영비']['TypeA'] = subtotal(operating_cost['객실운영비'], 'TypeA')
operating_cost['객실운영비']['TypeB'] = subtotal(operating_cost['객실운영비'], 'TypeB')
operating_cost['객실운영비']['TypeC'] = subtotal(operating_cost['객실운영비'], 'TypeC')
operating_cost['객실운영비']['Overhead'] = subtotal(operating_cost['객실운영비'], 'Overhead')
operating_cost['객실운영비']['Total'] = subtotal(operating_cost['객실운영비'], 'Total')


#### 2. 관리운영비
operating_cost['관리운영비'] = {}

## 2-1. 관리운영비
data = []
for dt in index['model']:
    dct = {}
    dct['광고홍보비'] = int(
        assumption['management_cost']['광고홍보비예산']['amount'] *
        assumption['management_cost']['광고홍보비'][dt.month] *
        index['연간인상률'].loc[dt, '운영비']
    )
    dct['기타운영비'] = int(
        assumption['management_cost']['기타운영비']['amount'] *
        index['연간인상률'].loc[dt, '운영비']
    )
    dct['Total'] = dct['광고홍보비'] + dct['기타운영비']
    data.append(dct)

operating_cost['관리운영비']['관리운영비'] = pd.DataFrame(data, index=index['model'])

## 2-2. SubTotal
operating_cost['관리운영비']['Total'] = subtotal(operating_cost['관리운영비'], 'Total')


#### 3. 인건비
operating_cost['인건비'] = {}

## 3-1. 객실운영팀
data = []
for dt in index['model']:
    dct = {}
    dct['정규직'] = int(
        assumption['salary_cost']['employee_count']['객실운영팀_정규직'] *
        assumption['salary_cost']['annual_salary']['객실운영팀_정규직'] *
        index['days'].loc[dt, '월간일수'] / index['days'].loc[dt, '연간일수'] *
        index['연간인상률'].loc[dt, '인건비']
    )
    dct['임시직'] = int(
        assumption['salary_cost']['employee_count']['객실운영팀_임시직'] *
        assumption['salary_cost']['annual_salary']['객실운영팀_임시직'] *
        index['days'].loc[dt, '월간일수'] / index['days'].loc[dt, '연간일수'] *
        index['연간인상률'].loc[dt, '인건비']
    )
    dct['Total'] = dct['정규직'] + dct['임시직']
    data.append(dct)
operating_cost['인건비']['객실운영팀'] = pd.DataFrame(data, index=index['model'])

## 3-2. 경영지원팀
data = []
for dt in index['model']:
    dct = {}
    dct['정규직'] = int(
        assumption['salary_cost']['employee_count']['경영지원팀_정규직'] *
        assumption['salary_cost']['annual_salary']['경영지원팀_정규직'] *
        index['days'].loc[dt, '월간일수'] / index['days'].loc[dt, '연간일수'] *
        index['연간인상률'].loc[dt, '인건비']
    )
    dct['임원'] = int(
        assumption['salary_cost']['employee_count']['경영지원팀_임원'] *
        assumption['salary_cost']['annual_salary']['경영지원팀_임원'] *
        index['days'].loc[dt, '월간일수'] / index['days'].loc[dt, '연간일수'] *
        index['연간인상률'].loc[dt, '인건비']
    )
    dct['Total'] = dct['정규직'] + dct['임원']
    data.append(dct)
operating_cost['인건비']['경영지원팀'] = pd.DataFrame(data, index=index['model'])

## 3-3. 마케팅팀
data = []
for dt in index['model']:
    dct = {}
    dct['정규직'] = int(
        assumption['salary_cost']['employee_count']['마케팅팀_정규직'] *
        assumption['salary_cost']['annual_salary']['마케팅팀_정규직'] *
        index['days'].loc[dt, '월간일수'] / index['days'].loc[dt, '연간일수'] *
        index['연간인상률'].loc[dt, '인건비']
    )
    dct['Total'] = dct['정규직']
    data.append(dct)
operating_cost['인건비']['마케팅팀'] = pd.DataFrame(data, index=index['model'])

## 3-4. 시설관리팀
data = []
for dt in index['model']:
    dct = {}
    dct['정규직'] = int(
        assumption['salary_cost']['employee_count']['시설관리팀_정규직'] *
        assumption['salary_cost']['annual_salary']['시설관리팀_정규직'] *
        index['days'].loc[dt, '월간일수'] / index['days'].loc[dt, '연간일수'] *
        index['연간인상률'].loc[dt, '인건비']
    )
    dct['임시직'] = int(
        assumption['salary_cost']['employee_count']['시설관리팀_임시직'] *
        assumption['salary_cost']['annual_salary']['시설관리팀_임시직'] *
        index['days'].loc[dt, '월간일수'] / index['days'].loc[dt, '연간일수'] *
        index['연간인상률'].loc[dt, '인건비']
    )
    dct['Total'] = dct['임시직']
    data.append(dct)
operating_cost['인건비']['시설관리팀'] = pd.DataFrame(data, index=index['model'])

## 3-5. SubTotal
operating_cost['인건비']['정규직'] = subtotal(operating_cost['인건비'], '정규직')
operating_cost['인건비']['임시직'] = subtotal(operating_cost['인건비'], '임시직')
operating_cost['인건비']['임원'] = subtotal(operating_cost['인건비'], '임원')
operating_cost['인건비']['Total'] = subtotal(operating_cost['인건비'], 'Total')