import datetime

def get_week_of_month(year, month, day):
    # 해당 연도의 해당 월의 첫째 날을 계산
    first_day = datetime.date(year, month, 1)
    current_day = datetime.date(year, month, day)
    # 첫째 주는 첫째 날부터 시작하여 현재 날짜까지의 주차를 계산
    return (current_day.day + first_day.weekday()) // 7 + 1

# 연도와 월, 날짜 입력
today = datetime.datetime.today()

print(today.isoformat())

# 해당 날짜의 몇 번째 주차인지 계산
week_of_month = get_week_of_month(today.year, today.month, today.day)
print(f"{week_of_month}번째 주입니다.")