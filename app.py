import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd
import os

st.set_page_config(page_title="아동 만 나이 기록기", layout="wide")
st.title("👶 아동 만 나이 기록기 (자동 저장형)")

# 저장할 파일 이름
DB_FILE = "slp_database.csv"

# 1. 데이터 불러오기 함수
def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE).to_dict('records')
    return []

# 2. 데이터 저장하기 함수
def save_data(data_list):
    df = pd.DataFrame(data_list)
    df.to_csv(DB_FILE, index=False, encoding='utf-8-sig')

# 3. 세션 상태 초기화 (처음 실행 시 파일에서 로드)
if 'results_list' not in st.session_state:
    st.session_state['results_list'] = load_data()

# --- 사이드바 입력창 ---
with st.sidebar:
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
        else:
            diff = relativedelta(test_date, birth_date)
            total_months = (diff.years * 12) + diff.months
            
            new_entry = {
                "이름": child_name,
                "만 나이": f"{diff.years}세 {diff.months}개월 {diff.days}일",
                "형식": f"{diff.years};{diff.months}",
                "총 월령": f"{total_months}개월",
                "생년월일": birth_date.strftime("%Y-%m-%d"),
                "검사일": test_date.strftime("%Y-%m-%d")
            }
            # 리스트에 추가하고 파일로 즉시 저장
            st.session_state['results_list'].append(new_entry)
            save_data(st.session_state['results_list'])
            st.rerun()

# --- 메인 화면: 결과 목록 ---
st.subheader("📊 누적 검사 결과 목록")

if not st.session_state['results_list']:
    st.info("저장된 데이터가 없습니다.")
else:
    # 목록 표시 (삭제 기능 포함)
    for i, entry in enumerate(reversed(st.session_state['results_list'])):
        real_idx = len(st.session_state['results_list']) - 1 - i
        
        col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 1, 1])
        with col1: st.write(entry['이름'])
        with col2: st.write(entry['만 나이'])
        with col3: st.write(entry['형식'])
        with col4: st.write(entry['총 월령'])
        with col5:
            if st.button("삭제", key=f"del_{real_idx}", use_container_width=True):
                st.session_state['results_list'].pop(real_idx)
                save_data(st.session_state['results_list']) # 삭제 후 파일 업데이트
                st.rerun()

    # 하단 도구
    st.sidebar.markdown("---")
    if st.sidebar.button("데이터 전체 초기화"):
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
        st.session_state['results_list'] = []
        st.rerun()
