import streamlit as st
from datetime import date

st.title("👶 만 나이 계산기")

# min_value를 1980년 1월 1일로 설정합니다.
# value는 기본으로 표시될 날짜입니다.
birth_date = st.date_input(
    "아동의 생년월일",
    value=date(2020, 1, 1), # 기본값 (원하는 대로 수정 가능)
    min_value=date(1980, 1, 1), # 1980년부터 입력 가능하도록 수정
    max_value=date.today()      # 오늘 이후 날짜는 선택 불가능하게 설정
)

test_date = st.date_input("검사일(오늘)", value=date.today())

# 버튼을 눌렀을 때 계산하도록 구성하면 더 깔끔합니다.
if st.button("계산하기"):
    if birth_date > test_date:
        st.error("생년월일이 검사일보다 나중일 수 없습니다.")
    else:
        # 여기에 기존에 작성하셨던 만 나이 계산 로직을 넣으시면 됩니다.
        st.write(f"선택하신 생년월일: {birth_date}")
        st.success("계산된 만 나이입니다!")
