import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd

st.set_page_config(page_title="만 나이 계산기", layout="wide")
st.title("👶 만 나이 계산기")

# 1. 세션 상태 초기화
if 'results_list' not in st.session_state:
    st.session_state['results_list'] = []

# 2. 정보 입력 섹션
with st.sidebar: # 입력창을 왼쪽 사이드바로 옮겨서 결과 목록을 더 넓게 볼 수 있게 구성했습니다.
    st.header("📋 정보 입력")
    child_name = st.text_input("대상자 이름", placeholder="이름 입력")
    
    birth_date = st.date_input(
        "생년월일",
        value=date(2020, 1, 1),
        min_value=date(1980, 1, 1),
        max_value=date.today()
    )
    test_date = st.date_input("검사일(오늘)", value=date.today())

    if st.button("계산 및 목록 추가", use_container_width=True):
        if not child_name:
            st.warning("이름을 입력해주세요.")
        elif birth_date > test_date:
            st.error("날짜를 확인해주세요.")
        else:
            diff = relativedelta(test_date, birth_date)
            total_months = (diff.years * 12) + diff.months
            
            new_entry = {
                "이름": child_name,
                "만 나이": f"{diff.years}세 {diff.months}개월 {diff.days}일",
                "형식": f"{diff.years};{diff.months}",
                "총 월령": f"{total_months}개월",
                "생년월일": birth_date.strftime("%Y-%m-%d")
            }
            st.session_state['results_list'].append(new_entry)
            st.rerun()

# 3. 결과 목록 표시 섹션
st.subheader("📊 검사 결과 목록")

if not st.session_state['results_list']:
    st.info("입력된 데이터가 없습니다. 왼쪽에서 정보를 입력하고 추가해주세요.")
else:
    # 헤더 부분
    h_col1, h_col2, h_col3, h_col4, h_col5 = st.columns([1, 2, 1, 1, 1])
    h_col1.write("**이름**")
    h_col2.write("**만 나이**")
    h_col3.write("**형식(세;월)**")
    h_col4.write("**총 월령**")
    h_col5.write("**관리**")
    st.divider()

    # 목록 반복문으로 출력 (역순으로 보여줘서 최신 데이터가 위로 오게 함)
    for i, entry in enumerate(reversed(st.session_state['results_list'])):
        # 실제 인덱스 계산 (역순 출력 때문)
        real_idx = len(st.session_state['results_list']) - 1 - i
        
        col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 1, 1])
        
        col1.write(entry['이름'])
        col2.write(entry['만 나이'])
        col3.write(entry['형식'])
        col4.write(entry['총 월령'])
        
        # 개별 삭제 버튼
        if col5.button("삭제", key=f"del_{real_idx}", type="secondary", use_container_width=True):
            st.session_state['results_list'].pop(real_idx)
            st.rerun()

    # 4. 하단 관리 기능
    st.sidebar.markdown("---")
    if st.sidebar.button("목록 전체 초기화"):
        st.session_state['results_list'] = []
        st.rerun()
    
    if st.session_state['results_list']:
        df = pd.DataFrame(st.session_state['results_list'])
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.sidebar.download_button(
            label="전체 목록 CSV 다운로드",
            data=csv,
            file_name=f"SLP_Age_Report_{date.today()}.csv",
            mime="text/csv",
            use_container_width=True
        )
