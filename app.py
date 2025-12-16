import streamlit as st
import random

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="로또 모바일",
    page_icon="🎱",
    layout="centered"
)

# =========================================================
# [핵심] 간격(Gap)을 0으로 만드는 초강력 CSS
# =========================================================
st.markdown("""
<style>
    /* 1. 컬럼 사이의 거대한 간격(기본 16px)을 2px로 강제 축소 */
    div[data-testid="stHorizontalBlock"] {
        gap: 2px !important; /* 여기가 범인 검거 현장! */
        flex-direction: row !important; /* 무조건 가로 정렬 */
        flex-wrap: nowrap !important;
    }

    /* 2. 컬럼 자체의 불필요한 여백 제거 */
    div[data-testid="column"] {
        min-width: 0px !important;
        width: 14.28% !important; /* 정확히 1/7 */
        flex: 1 !important;
        padding: 0px !important;
        margin: 0px !important;
    }

    /* 3. 버튼 꽉 차게 만들기 */
    div.stButton > button {
        width: 100%;
        padding: 0px !important;   /* 버튼 안쪽 여백 제거 */
        margin: 0px !important;    /* 버튼 바깥 여백 제거 */
        height: 35px !important;   /* 버튼 높이 고정 */
        min-height: 0px !important;
        font-size: 12px !important;
        line-height: 1 !important;
        border-radius: 4px !important;
    }
    
    /* 4. 화면 양옆 여백 줄이기 (화면 넓게 쓰기) */
    .block-container {
        padding-top: 2rem !important;
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
    if st.button("로그인", use_container_width=True):
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
    st.session_state.mode = 'gold' 

def toggle_num(n):
    mode = st.session_state.mode
    if mode == 'gold': 
        if n in st.session_state.opt_nums:
            st.session_state.opt_nums.remove(n) 
        else:
            if n in st.session_state.worst_nums: st.session_state.worst_nums.remove(n)
            st.session_state.opt_nums.add(n)
    else: 
        if n in st.session_state.worst_nums:
            st.session_state.worst_nums.remove(n) 
        else:
            if n in st.session_state.opt_nums: st.session_state.opt_nums.remove(n) 
            st.session_state.worst_nums.add(n) 

def reset_all():
    st.session_state.opt_nums.clear()
    st.session_state.worst_nums.clear()

# ==========================================
# [사이드바]
# ==========================================
with st.sidebar:
    st.header("설정")
    st.write("🥇 **최적(Gold)**")
    pick_opt = st.selectbox("최적 개수", [0,1,2,3,4,5,6], index=4, label_visibility="collapsed")
    st.caption(f"선택: {len(st.session_state.opt_nums)}개")
    st.write("🥶 **최악(Blue)**")
    pick_worst = st.selectbox("최악 개수", [0,1,2,3,4,5,6], index=2, label_visibility="collapsed")
    st.caption(f"선택: {len(st.session_state.worst_nums)}개")
    st.divider()
    if st.button("🔄 초기화", use_container_width=True):
        reset_all()
        st.rerun()

# ==========================================
# [메인 화면]
# ==========================================
st.write("### 🎱 모바일 로또")

# 모드 선택
mode = st.radio("모드", ["🥇 최적", "🥶 최악"], horizontal=True, label_visibility="collapsed")

if "최적" in mode:
    st.session_state.mode = 'gold'
    st.caption("현재: **최적(노랑)** 선택 중")
else:
    st.session_state.mode = 'blue'
    st.caption("현재: **최악(파랑)** 선택 중")

# --- 번호판 그리기 ---
# gap: 2px !important가 적용된 상태에서 그려집니다.
for row_start in range(1, 46, 7):
    cols = st.columns(7)
    
    for i in range(7):
        num = row_start + i
        if num > 45: break
        
        label = str(num)
        is_primary = False
        
        if num in st.session_state.opt_nums:
            label = "✅" 
            is_primary = True
        elif num in st.session_state.worst_nums:
            label = "❌"
            is_primary = False 
        
        # cols[i]에 버튼 배치
        cols[i].button(
            label if (num in st.session_state.opt_nums or num in st.session_state.worst_nums) else str(num),
            key=f"btn_{num}",
            on_click=toggle_num,
            args=(num,),
            type="primary" if is_primary or (num in st.session_state.worst_nums) else "secondary"
        )

st.divider()

if st.button("🎲 10게임 생성", type="primary", use_container_width=True):
    gold_set = list(st.session_state.opt_nums)
    blue_set = list(st.session_state.worst_nums)
    
    if len(gold_set) < pick_opt:
        st.error(f"최적 번호 부족! ({len(gold_set)}/{pick_opt})")
    elif len(blue_set) < pick_worst:
        st.error(f"최악 번호 부족! ({len(blue_set)}/{pick_worst})")
    else:
        st.success("생성 완료! (메뉴>설정 확인)")
        result_txt = ""
        for k in range(1, 11):
            s_gold = random.sample(gold_set, pick_opt)
            s_blue = random.sample(blue_set, pick_worst)
            final_nums = sorted(s_gold + s_blue)
            result_txt += f"{k}회: {final_nums}\n"
        st.code(result_txt)
