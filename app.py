import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta # 이 라이브러리가 필요합니다

st.title("👶 아동 만 나이 계산기")

birth_date = st.date_input(
    "아동의 생년월일",
    value=date(2020, 1, 1),
    min_value=date(1980, 1, 1),
    max_value=date.today()
)

test_date = st.date_input("검사일(오늘)", value=date.today())

if st.button("계산하기"):
    if birth_date > test_date:
        st.error("생년월일이 검사일보다 나중일 수 없습니다.")
    else:
        # relativedelta를 사용하면 연, 월, 일을 아주 정확하게 계산해줍니다.
        diff = relativedelta(test_date, birth_date)
        
        years = diff.years
        months = diff.months
        days = diff.days
        
        # 요청하신 형식으로 결과 출력
        result_text = f"만 {years}세 {months}개월 {days}일 ({years};{months})"
        
        st.markdown("---")
        st.subheader("계산 결과")
        st.success(result_text)
        
        # 팁: 치료실에서 복사해서 바로 쓰실 수 있게 추가
        st.code(result_text, language=None)
