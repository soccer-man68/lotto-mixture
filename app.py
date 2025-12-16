import streamlit as st
import random

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="로또 번호판 조합기",
    page_icon="🎱",
    layout="centered"
)

# [스타일 보정] 버튼 간격을 좁혀서 번호판처럼 보이게 만들기
st.markdown("""
<style>
    div[data-testid="column"] {
        padding: 0px 5px; /* 좌우 간격 줄임 */
    }
    div.stButton > button {
        width: 100%;
        padding: 10px 0px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# [로그인 시스템]
# ==========================================
def check_login():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.header("🔒 접근 제한")
        password_input = st.text_input("비밀번호", type="password")
        if st.button("로그인"):
            if password_input == "0207": # 👈 비밀번호 변경 가능
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("비밀번호가 틀렸습니다.")
        return False
    return True

if not check_login():
    st.stop()

# ==========================================
# [메인 로직]
# ==========================================

# 1. 세션 상태 초기화 (저장소)
if 'opt_nums' not in st.session_state:
    st.session_state.opt_nums = set()
if 'worst_nums' not in st.session_state:
    st.session_state.worst_nums = set()
if 'mode' not in st.session_state:
    st.session_state.mode = 'gold' # 기본값: 최적(Gold) 입력 모드

# 2. 번호 클릭 시 실행될 함수
def toggle_num(n):
    mode = st.session_state.mode
    
    # 이미 선택되어 있는지 확인
    in_gold = n in st.session_state.opt_nums
    in_blue = n in st.session_state.worst_nums
    
    if mode == 'gold': # [최적 모드] 일 때
        if in_gold:
            st.session_state.opt_nums.remove(n) # 이미 있으면 뺌
        else:
            if in_blue: st.session_state.worst_nums.remove(n) # 파란색에 있으면 거기서 빼고
            st.session_state.opt_nums.add(n) # 노란색 추가
            
    elif mode == 'blue': # [최악 모드] 일 때
        if in_blue:
            st.session_state.worst_nums.remove(n) # 이미 있으면 뺌
        else:
            if in_gold: st.session_state.opt_nums.remove(n) # 노란색에 있으면 거기서 빼고
            st.session_state.worst_nums.add(n) # 파란색 추가

# 3. 초기화 함수
def reset_all():
    st.session_state.opt_nums.clear()
    st.session_state.worst_nums.clear()

# ==========================================
# [화면 디자인]
# ==========================================
st.title("🎱 로또 커스텀 조합기 (Grid)")

# --- 상단 설정 영역 ---
st.write("### 1. 조합 설정 및 추출 개수")
col_s1, col_s2 = st.columns(2)

with col_s1:
    st.markdown("#### 🥇 최적 예상수 (Gold)")
    pick_opt = st.selectbox("추출 개수:", [0,1,2,3,4,5,6], index=4, key='s_opt')
    st.caption(f"현재 선택: {len(st.session_state.opt_nums)}개")

with col_s2:
    st.markdown("#### 🥶 최악 예상수 (Blue)")
    pick_worst = st.selectbox("추출 개수:", [0,1,2,3,4,5,6], index=2, key='s_worst')
    st.caption(f"현재 선택: {len(st.session_state.worst_nums)}개")

st.divider()

# --- 입력 모드 선택 (라디오 버튼) ---
col_m1, col_m2 = st.columns([3, 1])
with col_m1:
    st.write("### 2. 번호판 클릭 모드 선택")
    # 가로형 라디오 버튼으로 모드 스위치 구현
    mode_selection = st.radio(
        "어떤 번호를 입력하시겠습니까?",
        ["🥇 최적 예상수 입력 중", "🥶 최악 예상수 입력 중"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    # 선택된 값에 따라 내부 상태 변경
    if "최적" in mode_selection:
        st.session_state.mode = 'gold'
    else:
        st.session_state.mode = 'blue'

with col_m2:
    st.write("") # 줄맞춤용 공백
    if st.button("전체 초기화"):
        reset_all()
        st.rerun()

# --- 번호판 그리드 생성 (핵심 부분!) ---
st.write("### 3. 번호 선택")

# 7개 열 생성 (일~토 달력처럼 7칸씩)
columns = st.columns(7)

for i in range(1, 46):
    col_idx = (i - 1) % 7 # 0~6 인덱스 반복
    
    # 버튼 라벨과 스타일 결정
    label = str(i)
    is_primary = False
    
    if i in st.session_state.opt_nums:
        label = f"🥇{i}" # 최적 번호는 금메달 표시
        is_primary = True # 색상 강조
    elif i in st.session_state.worst_nums:
        label = f"🥶{i}" # 최악 번호는 얼음 표시
        is_primary = False 
    
    # 버튼 그리기 (callback 함수 사용)
    columns[col_idx].button(
        label,
        key=f"btn_{i}",
        on_click=toggle_num, # 버튼 누르면 toggle_num 함수 실행
        args=(i,),           # 함수에 숫자 i를 전달
        type="primary" if is_primary or (i in st.session_state.worst_nums) else "secondary", 
        use_container_width=True
    )

st.divider()

# --- 생성 버튼 ---
generate_btn = st.button("🔮 커스텀 조합 생성 및 추천 받기", type="primary", use_container_width=True)

if generate_btn:
    gold_set = list(st.session_state.opt_nums)
    blue_set = list(st.session_state.worst_nums)
    
    # 개수 검사
    if len(gold_set) < pick_opt:
        st.error(f"오류: 최적 예상수가 부족합니다. ({len(gold_set)}개 선택됨 / {pick_opt}개 필요)")
    elif len(blue_set) < pick_worst:
        st.error(f"오류: 최악 예상수가 부족합니다. ({len(blue_set)}개 선택됨 / {pick_worst}개 필요)")
    else:
        st.success("조합 생성 완료! 아래 추천 번호를 확인하세요.")
        
        # 결과 텍스트 생성
        result_txt = ""
        for k in range(1, 11):
            s_gold = random.sample(gold_set, pick_opt)
            s_blue = random.sample(blue_set, pick_worst)
            final_nums = sorted(s_gold + s_blue)
            result_txt += f"추천 {k:02d}:  {final_nums}\n"
            
        st.code(result_txt, language="python")

# 하단 로그아웃
st.markdown("---")
if st.button("로그아웃"):
    st.session_state.logged_in = False
    st.rerun()
