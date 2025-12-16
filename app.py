import streamlit as st
import random

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="로또 모바일",
    page_icon="🎱",
    layout="centered"
)

# =========================================================
# [핵심] 모바일 '세로 줄서기'를 막는 강력한 스타일
# =========================================================
st.markdown("""
<style>
    /* 1. 틀(Block) 강제 가로 정렬 */
    /* Streamlit은 모바일에서 이 틀을 세로(column)로 바꿔버립니다. */
    /* 이걸 !important로 막아서 강제로 가로(row)로 유지시킵니다. */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important; /* 무조건 가로! */
        flex-wrap: nowrap !important;   /* 줄바꿈 금지! */
    }

    /* 2. 칸(Column) 너비 강제 고정 */
    div[data-testid="column"] {
        width: 14.28% !important;       /* 1/7 크기 */
        flex: 0 0 14.28% !important;
        min-width: 1px !important;      /* 최소 너비 제한 해제 */
        padding: 1px !important;        /* 간격 최소화 */
    }

    /* 3. 버튼 디자인 (작게) */
    div.stButton > button {
        width: 100%;
        padding: 5px 0px !important;
        font-size: 11px !important;     /* 글씨 더 작게 */
        min-height: 0px !important;
        margin: 0px !important;
        line-height: 1 !important;
    }
    
    /* 4. 불필요한 여백 제거 */
    .block-container {
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# [로그인]
# ==========================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.warning("🔒 로그인 필요")
    pw = st.text_input("비밀번호", type="password")
    if st.button("로그인", use_container_width=True):
        if pw == "0207":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("비밀번호 오류")
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
# [사이드바 설정]
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

mode = st.radio(
    "모드",
    ["🥇 최적", "🥶 최악"],
    horizontal=True,
    label_visibility="collapsed"
)

if "최적" in mode:
    st.session_state.mode = 'gold'
    st.caption("현재: **최적(노랑)** 입력 중")
else:
    st.session_state.mode = 'blue'
    st.caption("현재: **최악(파랑)** 입력 중")

st.write("") 

# --- 번호판 그리기 (7개씩 끊어서 생성) ---
# 여기서 st.columns(7)이 실행될 때, 위의 CSS가 "가로로 서라!"라고 명령합니다.
for row_start in range(1, 46, 7):
    cols = st.columns(7) 
    
    for i in range(7):
        num = row_start + i
        if num > 45: break
        
        # 버튼 텍스트/스타일
        label = str(num)
        is_primary = False
        
        if num in st.session_state.opt_nums:
            label = "✅" 
            is_primary = True
        elif num in st.session_state.worst_nums:
            label = "❌"
            is_primary = False 
        
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
