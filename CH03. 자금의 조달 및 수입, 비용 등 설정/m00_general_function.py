from datetime import datetime, timedelta

def end_of_month(dt):
    # 다음 달의 첫날
    next_month = dt.replace(day=28) + timedelta(days=4)
    # 이번 달의 마지막 날
    return next_month - timedelta(days=next_month.day)

def list_end_of_months(start_date, end_date):
    end_of_months = []

    current_date = end_of_month(start_date)
    while current_date <= end_date:
        end_of_months.append(current_date)
        next_month = current_date.replace(day=28) + timedelta(days=4)
        current_date = end_of_month(next_month)
    
    return end_of_months

def calculate_inflation_rate(year, base_year, rate):
    return ((1 + rate) ** max(year - base_year, 0))

def subtotal(df, param):
    subtotal = 0
    for key in df.keys():
        try:
            subtotal = subtotal + df[key][param]
        except KeyError:
            pass
    return subtotal
