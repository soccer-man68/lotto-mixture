import streamlit as st
import random

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="로또 Red & Blue",
    page_icon="🎱",
    layout="centered"
)

# =========================================================
# [스타일] 격자 유지 + 폰트 진하게 + 색상 강조
# =========================================================
st.markdown("""
<style>
    /* 1. 번호판 격자(Grid) 유지 (절대 깨지지 않음) */
    div[data-testid="stHorizontalBlock"] {
        display: grid !important;
        grid-template-columns: repeat(7, 1fr) !important;
        gap: 2px !important;
        padding: 0px !important;
    }

    /* 2. 각 칸의 크기 제한 해제 */
    div[data-testid="column"] {
        width: 100% !important;
        min-width: 0px !important;
        flex: unset !important;
        padding: 0px !important;
    }

    /* 3. 버튼 디자인 (폰트 진하게!) */
    div.stButton > button {
        width: 100% !important;
        min-width: 0px !important;
        padding: 0px !important;
        margin: 0px !important;
        height: 40px !important;
        
        /* 👇 요청하신 폰트 진하게 설정 */
        font-weight: 900 !important; 
        font-family: sans-serif !important;
        font-size: 13px !important;
        
        line-height: 1 !important;
        border-radius: 5px !important;
        border: 1px solid #e0e0e0 !important;
    }
    
    /* 4. 버튼 텍스트 설정 */
    div.stButton > button p {
        font-size: 13px !important;
        font-weight: 900 !important; /* 글자도 진하게 */
        white-space: nowrap !important;
    }

    /* 5. 선택된 버튼(Primary)의 색상 강제 지정 (빨강) */
    /* Streamlit 테마와 상관없이 최적 선택 시 빨간맛을 내기 위함 */
    div.stButton > button[kind="primary"] {
        background-color: #FF4B4B !important; /* 밝은 빨강 */
        color: white !important;
        border: none !important;
    }

    /* 6. 화면 여백 최적화 */
    .block-container {
        padding-top: 1rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        max-width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# [로그인]
# ==========================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.warning("🔒 로그인")
    pw = st.text_input("비밀번호", type="password")
    if st.button("로그인"):
        if pw == "0207":
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# ==========================================
# [데이터 로직]
# ==========================================
if 'opt_nums' not in st.session_state:
    st.session_state.opt_nums = set()
if 'worst_nums' not in st.session_state:
    st.session_state.worst_nums = set()
if 'mode' not in st.session_state:
    st.session_state.mode = 'red' # 기본값: 레드

def toggle_num(n):
    mode = st.session_state.mode
    
    # 레드(최적) 모드일 때
    if mode == 'red': 
        if n in st.session_state.opt_nums:
            st.session_state.opt_nums.remove(n) # 이미 있으면 제거
        else:
            if n in st.session_state.worst_nums: st.session_state.worst_nums.remove(n) # 파랑에 있으면 제거
            st.session_state.opt_nums.add(n) # 레드 추가
            
    # 블루(최악) 모드일 때
    else: 
        if n in st.session_state.worst_nums:
            st.session_state.worst_nums.remove(n) # 이미 있으면 제거
        else:
            if n in st.session_state.opt_nums: st.session_state.opt_nums.remove(n) # 레드에 있으면 제거
            st.session_state.worst_nums.add(n) # 블루 추가

def reset_all():
    st.session_state.opt_nums.clear()
    st.session_state.worst_nums.clear()

# ==========================================
# [사이드바 설정]
# ==========================================
with st.sidebar:
    st.header("설정 메뉴")
    
    st.write("🔴 **최적(Red)**")
    pick_opt = st.selectbox("최적 개수", [0,1,2,3,4,5,6], index=4, label_visibility="collapsed")
    
    st.write("🔵 **최악(Blue)**")
    pick_worst = st.selectbox("최악 개수", [0,1,2,3,4,5,6], index=2, label_visibility="collapsed")
    
    st.write("---")
    if st.button("🔄 번호 초기화"):
        reset_all()
        st.rerun()

# ==========================================
# [메인 화면]
# ==========================================
st.write("### 🎱 로또 (Red & Blue)")

# 모드 선택
mode = st.radio("모드 선택", ["🔴 최적 (Red)", "🔵 최악 (Blue)"], horizontal=True, label_visibility="collapsed")

if "최적" in mode:
    st.session_state.mode = 'red'
    st.caption(f"**🔴 최적(Red)** 선택 중 | {len(st.session_state.opt_nums)}개")
else:
    st.session_state.mode = 'blue'
    st.caption(f"**🔵 최악(Blue)** 선택 중 | {len(st.session_state.worst_nums)}개")

# --- 번호판 그리기 (Grid 적용됨) ---
for row_start in range(1, 46, 7):
    cols = st.columns(7)
    
    for i in range(7):
        num = row_start + i
        if num > 45: break
        
        # 버튼 라벨 및 스타일 결정
        label = str(num)
        is_primary = False # 기본은 흰색(secondary)
        
        # 1. 최적(Red)일 때
        if num in st.session_state.opt_nums:
            label = "🔴" # 빨간 원
            is_primary = True # CSS에서 빨간색 배경으로 만듦
            
        # 2. 최악(Blue)일 때
        elif num in st.session_state.worst_nums:
            label = "🔵" # 파란 원
            is_primary = False # 파란색은 이모티콘으로 표현 (배경은 흰색 유지)
        
        # 버튼 생성
        cols[i].button(
            label,
            key=f"btn_{num}",
            on_click=toggle_num,
            args=(num,),
            # 최적(Red)일 때만 primary 타입을 줘서 배경색을 칠함
            type="primary" if is_primary else "secondary"
        )

st.divider()

if st.button("🎲 10게임 생성하기", type="primary", use_container_width=True):
    red_set = list(st.session_state.opt_nums)
    blue_set = list(st.session_state.worst_nums)
    
    if len(red_set) < pick_opt:
        st.error(f"🔴 최적(Red) 번호 부족! ({len(red_set)}/{pick_opt})")
    elif len(blue_set) < pick_worst:
        st.error(f"🔵 최악(Blue) 번호 부족! ({len(blue_set)}/{pick_worst})")
    else:
        st.success("✨ 생성 완료!")
        result_txt = ""
        for k in range(1, 11):
            s_red = random.sample(red_set, pick_opt)
            s_blue = random.sample(blue_set, pick_worst)
            final_nums = sorted(s_red + s_blue)
            result_txt += f"{k}회: {final_nums}\n"
        st.code(result_txt)
