import pandas as pd

from m00_general_function import subtotal
from m01_assumption import assumption
from m02_index import index
from m04_operating_income import operating_income


facility_cost = {}

#### 1. 통상수선비
data = []
for dt in index['model']:
    dct = {}
    dct['TypeA'] = int(
        operating_income['TypeA'].loc[dt, '판매객실수'] * 
        assumption['facility_cost']['통상수선비']['TypeA'] *
        index['연간인상률'].loc[dt, '운영비']
    )
    dct['TypeB'] = int(
        operating_income['TypeB'].loc[dt, '판매객실수'] * 
        assumption['facility_cost']['통상수선비']['TypeB'] *
        index['연간인상률'].loc[dt, '운영비']
    )
    dct['TypeC'] = int(
        operating_income['TypeC'].loc[dt, '판매객실수'] * 
        assumption['facility_cost']['통상수선비']['TypeC'] *
        index['연간인상률'].loc[dt, '운영비']
    )
    dct['Total'] = dct['TypeA'] + dct['TypeB'] + dct['TypeC']
    data.append(dct)

facility_cost['통상수선비'] = pd.DataFrame(data, index=index['model'])


#### 2. 대수선공사비
data = []
for dt in index['model']:
    dct = {}
    if dt in index['수선TypeA']:
        dct['TypeA'] = int(
            assumption['business_overview']['객실수']['TypeA'] * 
            assumption['facility_cost']['대수선공사비']['TypeA']
        )
    else:
        dct['TypeA'] = 0

    if dt in index['수선TypeB']:
        dct['TypeB'] = int(
            assumption['business_overview']['객실수']['TypeB'] * 
            assumption['facility_cost']['대수선공사비']['TypeB']
        )
    else:
        dct['TypeB'] = 0

    if dt in index['수선TypeC']:
        dct['TypeC'] = int(
            assumption['business_overview']['객실수']['TypeC'] * 
            assumption['facility_cost']['대수선공사비']['TypeC']
        )
    else:
        dct['TypeC'] = 0
    
    dct['Total'] = dct['TypeA'] + dct['TypeB'] + dct['TypeC']
    data.append(dct)

facility_cost['대수선공사비'] = pd.DataFrame(data, index=index['model'])


#### 3. SubTotal
facility_cost['TypeA'] = subtotal(facility_cost, 'TypeA')
facility_cost['TypeB'] = subtotal(facility_cost, 'TypeB')
facility_cost['TypeC'] = subtotal(facility_cost, 'TypeC')
facility_cost['Total'] = subtotal(facility_cost, 'Total')