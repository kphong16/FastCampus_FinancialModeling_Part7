import pandas as pd

from m01_assumption import assumption
from m02_index import index


#### 1. 빈 funding 딕셔너리 설정
funding = {}


#### 2. 자기자본 설정
data = []
for dt in index['model']:
    dct = {}
    if dt == assumption['period_assumptions']['자금조달일정']['자기자본유입일']:
        dct['자기자본유입'] = assumption['funding_assumptions']['equity']['amount']
    else:
        dct['자기자본유입'] = 0
    
    dct['배당금지급'] = 0
    
    data.append(dct)
funding['자기자본'] = pd.DataFrame(data, index=index['model'])


#### 3. 차입금 설정
차입금잔액 = 0
data = []
for dt in index['model']:
    dct = {}

    # 차입금 유입금액 설정
    if dt == assumption['period_assumptions']['자금조달일정']['차입금유입일']:
        차입금유입 = assumption['funding_assumptions']['loan']['amount']
    else:
        차입금유입 = 0

    # 3개월 주기 원금상환 설정
    if (
        (dt in index['원금상환']) 
        and (
            index['원금상환'].index(dt) % 
            assumption['funding_assumptions']['loan']['원금상환주기'] == 2
        )
    ):
        차입금상환 = assumption['funding_assumptions']['loan']['상환원금']
    else:
        차입금상환 = 0

    # 매월 이자 지급 설정
    if dt in index['이자지급']:
        이자율 = assumption['funding_assumptions']['loan']['이자율']
        월간일수 = index['days'].loc[dt, '월간일수']
        연간일수 = index['days'].loc[dt, '연간일수']
        # 이자금액 계산
        차입이자 = int(round(차입금잔액 * 이자율 * 월간일수 / 연간일수, -1))
    else:
        차입이자 = 0

    차입금잔액 = 차입금잔액 + 차입금유입 - 차입금상환

    dct['차입금유입'] = 차입금유입
    dct['차입금상환'] = 차입금상환
    dct['차입이자'] = 차입이자
    dct['차입금잔액'] = 차입금잔액

    data.append(dct)
funding['차입금'] = pd.DataFrame(data, index=index['model'])


#### 4. 자산매입 설정
data = []
for dt in index['model']:
    dct = {}
    if dt == assumption['period_assumptions']['자산매입일정']['자산매입일']:
        dct['자산매입'] = assumption['business_overview']['자산매입']['자산매입금액']
    else:
        dct['자산매입'] = 0
    
    if dt == assumption['period_assumptions']['자산매입일정']['매입부수비용지급일']:
        dct['매입부수비용'] = assumption['business_overview']['자산매입']['매입부수비용']
    else:
        dct['매입부수비용'] = 0
    
    data.append(dct)
funding['자산매입'] = pd.DataFrame(data, index=index['model'])