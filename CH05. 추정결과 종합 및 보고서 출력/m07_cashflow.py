import pandas as pd
pd.set_option('display.max_rows', 30)
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_colwidth', 20)
pd.set_option('display.width', 300)

# DataFrame의 출력을 확장하여 한 줄로 계속 출력되도록 설정
pd.set_option('display.expand_frame_repr', True)

from m00_general_function import df_seperator
from m01_assumption import assumption
from m02_index import index
from m03_funding import funding
from m04_operating_income import operating_income
from m05_operating_cost import operating_cost
from m06_facility_cost import facility_cost


#### cashflow, balance 객체 초기화 ####
cashflow = pd.DataFrame(
    columns = ['date', 'categoryA', 'categoryB', 'categoryC', '입금금액', '출금금액']
)

balance = pd.DataFrame({
    '기초현금': [0] * len(index['model']),
    '입금금액': [0] * len(index['model']),
    '출금금액': [0] * len(index['model']),
    '기말현금': [0] * len(index['model']), 
},
    index=index['model']
)
room_type_list = list(assumption['business_overview']['객실수'].keys())


#### cashflow, balance 작성 ####
idx = 0
cash_balance = 0
for dt in index['model']:
    #### 0. 기초현금 계산
    balance.loc[dt, '기초현금'] = cash_balance

    #### 1. 자금조달소요
    ## 1-1. 자기자본 유입
    amount = funding['자기자본'].loc[dt, '자기자본유입']
    if amount > 0:
        cashflow.loc[idx] = [dt, '자금조달', '자기자본', '자기자본유입', amount, 0]
        balance.loc[dt, '입금금액'] += amount
        idx += 1

    ## 1-2. 차입금 유입
    amount = funding['차입금'].loc[dt, '차입금유입']
    if amount > 0:
        cashflow.loc[idx] = [dt, '자금조달', '차입금', '차입금유입', amount, 0]
        balance.loc[dt, '입금금액'] += amount
        idx += 1

    ## 1-3. 자산매입
    amount = funding['자산매입'].loc[dt, '자산매입']
    if amount > 0:
        cashflow.loc[idx] = [dt, '자산매입', '자산매입', '매입대금지출', 0, amount]
        balance.loc[dt, '출금금액'] += amount
        idx += 1
    amount = funding['자산매입'].loc[dt, '매입부수비용']
    if amount > 0:
        cashflow.loc[idx] = [dt, '자산매입', '매입부수비용', '부수비용지출', 0, amount]
        balance.loc[dt, '출금금액'] += amount
        idx += 1

    #### 2. 운영수입
    for room_type in room_type_list:
        amount = operating_income[room_type].loc[dt, '객실수입']
        if amount > 0:
            cashflow.loc[idx] = [dt, '운영수입', '객실수입', room_type, amount, 0]
            balance.loc[dt, '입금금액'] += amount
            idx += 1

    #### 3. 운영비용 - 객실운영비
    ## 3-1. 청소세탁비
    for room_type in room_type_list:
        amount = operating_cost['객실운영비']['청소세탁비'].loc[dt, room_type]
        if amount > 0:
            cashflow.loc[idx] = [dt, '객실운영비', '청소세탁비', room_type, 0, amount]
            balance.loc[dt, '출금금액'] += amount
            idx += 1
    
    ## 3-2. 수도광열비
    for room_type in room_type_list:
        amount = operating_cost['객실운영비']['수도광열비'].loc[dt, room_type]
        if amount > 0:
            cashflow.loc[idx] = [dt, '객실운영비', '수도광열비', room_type, 0, amount]
            balance.loc[dt, '출금금액'] += amount
            idx += 1

    amount = operating_cost['객실운영비']['수도광열비'].loc[dt, 'Overhead']
    if amount > 0:
        cashflow.loc[idx] = [dt, '객실운영비', '수도광열비', 'Overhead', 0, amount]
        balance.loc[dt, '출금금액'] += amount
        idx += 1
    
    ## 3-3. 예약수수료
    for room_type in room_type_list:
        amount = operating_cost['객실운영비']['예약수수료'].loc[dt, room_type]
        if amount > 0:
            cashflow.loc[idx] = [dt, '객실운영비', '예약수수료', room_type, 0, amount]
            balance.loc[dt, '출금금액'] += amount
            idx += 1
    
    #### 4. 운영비용 - 관리운영비
    ## 4-1. 광고홍보비
    amount = operating_cost['관리운영비']['관리운영비'].loc[dt, '광고홍보비']
    if amount > 0:
        cashflow.loc[idx] = [dt, '관리운영비', '관리운영비', '광고홍보비', 0, amount]
        balance.loc[dt, '출금금액'] += amount
        idx += 1
    
    ## 4-2. 기타운영비
    amount = operating_cost['관리운영비']['관리운영비'].loc[dt, '기타운영비']
    if amount > 0:
        cashflow.loc[idx] = [dt, '관리운영비', '관리운영비', '기타운영비', 0, amount]
        balance.loc[dt, '출금금액'] += amount
        idx += 1

    #### 5. 운영비용 - 인건비
    ## 5-1. 객실운영팀
    amount = operating_cost['인건비']['객실운영팀'].loc[dt, '정규직']
    if amount > 0:
        cashflow.loc[idx] = [dt, '인건비', '객실운영팀', '정규직', 0, amount]
        balance.loc[dt, '출금금액'] += amount
        idx += 1
    amount = operating_cost['인건비']['객실운영팀'].loc[dt, '임시직']
    if amount > 0:
        cashflow.loc[idx] = [dt, '인건비', '객실운영팀', '임시직', 0, amount]
        balance.loc[dt, '출금금액'] += amount
        idx += 1

    ## 5-2. 경영지원팀
    amount = operating_cost['인건비']['경영지원팀'].loc[dt, '정규직']
    if amount > 0:
        cashflow.loc[idx] = [dt, '인건비', '경영지원팀', '정규직', 0, amount]
        balance.loc[dt, '출금금액'] += amount
        idx += 1
    amount = operating_cost['인건비']['경영지원팀'].loc[dt, '임원']
    if amount > 0:
        cashflow.loc[idx] = [dt, '인건비', '경영지원팀', '임원', 0, amount]
        balance.loc[dt, '출금금액'] += amount
        idx += 1

    ## 5-3. 마케팅팀
    amount = operating_cost['인건비']['마케팅팀'].loc[dt, '정규직']
    if amount > 0:
        cashflow.loc[idx] = [dt, '인건비', '마케팅팀', '정규직', 0, amount]
        balance.loc[dt, '출금금액'] += amount
        idx += 1

    ## 5-4. 시설관리팀
    amount = operating_cost['인건비']['시설관리팀'].loc[dt, '정규직']
    if amount > 0:
        cashflow.loc[idx] = [dt, '인건비', '시설관리팀', '정규직', 0, amount]
        balance.loc[dt, '출금금액'] += amount
        idx += 1
    amount = operating_cost['인건비']['시설관리팀'].loc[dt, '임시직']
    if amount > 0:
        cashflow.loc[idx] = [dt, '인건비', '시설관리팀', '임시직', 0, amount]
        balance.loc[dt, '출금금액'] += amount
        idx += 1

    #### 6. 시설관리비
    ## 6-1. 통상수선비
    for room_type in room_type_list:
        amount = facility_cost['통상수선비'].loc[dt, room_type]
        if amount > 0:
            cashflow.loc[idx] = [dt, '시설관리비', '통상수선비', room_type, 0, amount]
            balance.loc[dt, '출금금액'] += amount
            idx += 1

    ## 6-2. 대수선공사비
    for room_type in room_type_list:
        amount = facility_cost['대수선공사비'].loc[dt, room_type]
        if amount > 0:
            cashflow.loc[idx] = [dt, '시설관리비', '대수선공사비', room_type, 0, amount]
            balance.loc[dt, '출금금액'] += amount
            idx += 1

    #### 7. 차입원리금 상환
    ## 7-1. 차입원금 상환
    amount = funding['차입금'].loc[dt, '차입금상환']
    if amount > 0:
        cashflow.loc[idx] = [dt, '차입원리금상환', '차입금', '차입금상환', 0, amount]
        balance.loc[dt, '출금금액'] += amount
        idx += 1
    
    ## 7-2. 차입이자 상환
    amount = funding['차입금'].loc[dt, '차입이자']
    if amount > 0:
        cashflow.loc[idx] = [dt, '차입원리금상환', '차입금', '차입이자', 0, amount]
        balance.loc[dt, '출금금액'] += amount
        idx += 1

    #### 8. 자기자본 배당
    ## 8-1. 배당 전 현금 잔액 계산
    cash_balance = balance.loc[dt, '기초현금'] + balance.loc[dt, '입금금액'] - balance.loc[dt, '출금금액']
    
    ## 8-2. 배당금 지급
    if assumption['funding_assumptions']['equity']['최초배당일'] <= dt and dt.month == 12:
        cash_balance = max(cash_balance, 0)
        amount = int(round(cash_balance * assumption['funding_assumptions']['equity']['배당률'], -3))
        funding['자기자본'].loc[dt, '배당금지급'] = amount
        cashflow.loc[idx] = [dt, '자기자본배당', '자기자본배당', '배당금지급', 0, amount]
        balance.loc[dt, '출금금액'] += amount
        idx += 1


    #### 9. 기말현금 계산
    cash_balance = (
        balance.loc[dt, '기초현금'] + balance.loc[dt, '입금금액'] - balance.loc[dt, '출금금액']
    )
    balance.loc[dt, '기말현금'] = cash_balance