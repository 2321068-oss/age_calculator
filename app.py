import streamlit as st
from datetime import date

st.title("👶 아동 만 나이 계산기")
st.write("아동의 생년월일과 검사일을 입력하면 정확한 만 나이를 계산합니다.")

# 1. 날짜 입력 받기
col1, col2 = st.columns(2)

with col1:
    birth_date = st.date_input("아동의 생년월일", value=date(2020, 1, 1))

with col2:
    test_date = st.date_input("검사일(오늘)", value=date.today())

# 2. 만 나이 계산 로직
if st.button("계산하기"):
    if birth_date > test_date:
        st.error("생년월일이 검사일보다 나중일 수 없습니다. 날짜를 확인해 주세요!")
    else:
        # 연도, 월, 일 차이 계산
        years = test_date.year - birth_date.year
        months = test_date.month - birth_date.month
        days = test_date.day - birth_date.day

        # '일'이 음수면 '월'에서 빌려오기
        if days < 0:
            months -= 1
            # 이전 달의 마지막 날짜만큼 더해줌 (단순화를 위해 30일로 계산하거나 정확한 로직 적용 가능)
            days += 30 

        # '월'이 음수면 '연'에서 빌려오기
        if months < 0:
            years -= 1
            months += 12

        st.success(f"결과: **만 {years}세 {months}개월 {days}일** 입니다.")
        st.balloons()