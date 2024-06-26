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
from m07_cashflow import cashflow, balance


def pivot_cashflow(cashflow=cashflow):
    cf_table = cashflow.copy()
    
    # 입금금액과 출금금액 간 차액 계산
    cf_table['amount'] = cf_table['입금금액'] - cf_table['출금금액']
    cf_table = cf_table[['date', 'categoryA', 'categoryB', 'categoryC', 'amount']]

    # 피벗테이블 작성
    cf_table = cf_table.pivot_table(
        values = 'amount',
        index = 'date',
        columns = ['categoryA', 'categoryB', 'categoryC'],
        aggfunc = 'sum'
    ).fillna(0).astype(int)

    # 현금잔액 및 소계 데이터 추가
    cf_table[('운영수입', '소계', '')] = operating_income['Total']['객실수입']
    cf_table[('객실운영비', '소계', '')] = -operating_cost['객실운영비']['Total']
    cf_table[('관리운영비', '소계', '')] = -operating_cost['관리운영비']['Total']
    cf_table[('인건비', '소계', '')] = -operating_cost['인건비']['Total']
    cf_table[('시설관리비', '소계', '')] = -facility_cost['Total']
    cf_table['기초현금'] = balance['기초현금']
    cf_table['기말현금'] = balance['기말현금']

    # 컬럼 순서 정리
    cf_table = cf_table[[
        (   '기초현금',       '',         ''),
        (   '자금조달',   '자기자본',   '자기자본유입'),
        (   '자금조달',    '차입금',    '차입금유입'),
        (   '자산매입',   '자산매입',  '매입대금지출'),
        (   '자산매입',   '매입부수비용',  '부수비용지출'),
        (   '운영수입',   '객실수입',     'TypeA'),
        (   '운영수입',   '객실수입',     'TypeB'),
        (   '운영수입',   '객실수입',     'TypeC'),
        (   '운영수입',      '소계',          ''),
        (  '객실운영비',  '예약수수료',    'TypeA'),
        (  '객실운영비',  '예약수수료',    'TypeB'),
        (  '객실운영비',  '예약수수료',    'TypeC'),
        (  '객실운영비',  '청소세탁비',    'TypeA'),
        (  '객실운영비',  '청소세탁비',    'TypeB'),
        (  '객실운영비',  '청소세탁비',    'TypeC'),
        (  '객실운영비',  '수도광열비',    'TypeA'),
        (  '객실운영비',  '수도광열비',    'TypeB'),
        (  '객실운영비',  '수도광열비',    'TypeC'),
        (  '객실운영비',  '수도광열비', 'Overhead'),
        (  '객실운영비',      '소계',         ''),
        (  '관리운영비',  '관리운영비',   '광고홍보비'),
        (  '관리운영비',  '관리운영비',   '기타운영비'),
        (  '관리운영비',      '소계',         ''),
        (    '인건비',  '객실운영팀',      '임시직'),
        (    '인건비',  '객실운영팀',      '정규직'),
        (    '인건비',  '경영지원팀',       '임원'),
        (    '인건비',  '경영지원팀',      '정규직'),
        (    '인건비',   '마케팅팀',      '정규직'),
        (    '인건비',  '시설관리팀',      '임시직'),
        (    '인건비',  '시설관리팀',      '정규직'),
        (    '인건비',      '소계',         ''),
        (  '시설관리비',  '통상수선비',    'TypeA'),
        (  '시설관리비',  '통상수선비',    'TypeB'),
        (  '시설관리비',  '통상수선비',    'TypeC'),
        (  '시설관리비', '대수선공사비',    'TypeA'),
        (  '시설관리비', '대수선공사비',    'TypeB'),
        (  '시설관리비', '대수선공사비',    'TypeC'),
        (  '시설관리비',      '소계',         ''),
        ('차입원리금상환',    '차입금',    '차입금상환'),
        ('차입원리금상환',    '차입금',     '차입이자'),       
        ('자기자본배당', '자기자본배당', '배당금지급'), 
        (   '기말현금',       '',         '')
    ]]

    return cf_table


def print_cashflow(cashflow=cashflow, file_name='cashflow_table.xlsx'):
    cf_excel = pivot_cashflow(cashflow)
    cf_excel.index = cf_excel.index.strftime('%Y-%m-%d')
    cf_excel.to_excel(file_name)


dct = {
    'assumption': assumption,
    'index': index,
    'funding': funding,
    'operating_income': operating_income,
    'operating_cost': operating_cost,
    'facility_cost': facility_cost,
    'cashflow': cashflow,
    'balance': balance,
    'pivot_cashflow': pivot_cashflow,
    'print_cashflow': print_cashflow
}