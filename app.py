import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd # 결과 목록을 표로 보여주기 위해 필요합니다

st.title("👶 아동 만 나이 계산기")

# 1. 결과 목록을 저장할 저장소(리스트) 생성 (세션 상태 활용)
if 'results_list' not in st.session_state:
    st.session_state['results_list'] = []

# 2. 입력 섹션
with st.container():
    st.subheader("정보 입력")
    # 대상자 이름 입력 칸 추가
    child_name = st.text_input("대상자 이름", placeholder="이름을 입력하세요")
    
    col1, col2 = st.columns(2)
    with col1:
        birth_date = st.date_input(
            "생년월일",
            value=date(2020, 1, 1),
            min_value=date(1980, 1, 1),
            max_value=date.today()
        )
    with col2:
        test_date = st.date_input("검사일(오늘)", value=date.today())

# 3. 계산 및 누적 버튼
if st.button("계산 및 목록에 추가"):
    if not child_name:
        st.warning("대상자의 이름을 입력해주세요.")
    elif birth_date > test_date:
        st.error("생년월일이 검사일보다 나중일 수 없습니다.")
    else:
        # 계산 로직
        diff = relativedelta(test_date, birth_date)
        years, months, days = diff.years, diff.months, diff.days
        total_months = (years * 12) + months
        
        # 결과 데이터 생성
        new_data = {
            "이름": child_name,
            "생년월일": birth_date.strftime("%Y-%m-%d"),
            "검사일": test_date.strftime("%Y-%m-%d"),
            "만 나이": f"{years}세 {months}개월 {days}일",
            "형식(세;월)": f"{years};{months}",
            "총 월령": f"{total_months}개월"
        }
        
        # 목록에 추가
        st.session_state['results_list'].append(new_data)
        st.success(f"'{child_name}' 아동의 데이터가 추가되었습니다!")

# 4. 결과 목록 표시 섹션
if st.session_state['results_list']:
    st.markdown("---")
    st.subheader("📊 검사 결과 목록")
    
    # 리스트를 데이터프레임(표)으로 변환
    df = pd.DataFrame(st.session_state['results_list'])
    
    # 표 출력
    st.table(df) # 또는 st.dataframe(df)
    
    # 5. 엑셀/CSV 다운로드 기능 (선택 사항)
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="결과 목록 다운로드 (CSV)",
        data=csv,
        file_name=f"검사결과목록_{date.today()}.csv",
        mime="text/csv",
    )
    
    # 목록 초기화 버튼
    if st.button("목록 전체 삭제"):
        st.session_state['results_list'] = []
        st.rerun()
