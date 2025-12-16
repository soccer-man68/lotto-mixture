import streamlit as st
import random

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="모바일 로또",
    page_icon="🎱",
    layout="centered"
)

# =========================================================
# [핵심] 모바일 세로 정렬을 막는 "강력한(Nuclear)" 스타일
# =========================================================
st.markdown("""
<style>
    /* 1. 컬럼(칸) 강제 고정 */
    /* 화면이 좁아지면 무조건 세로로 쌓으려는 Streamlit의 성질을 억지로 눕힙니다 */
    [data-testid="column"] {
        width: 14.28% !important;       /* 100% 나누기 7 */
        flex: 0 0 14.28% !important;    /* 크기 늘어나거나 줄어들지 않게 고정 */
        min-width: 0px !important;      /* 최소 너비 제한 해제 (이게 핵심!) */
        max-width: 14.28% !important;
        padding: 1px !important;        /* 칸 사이 여백 최소화 */
        overflow: visible !important;   /* 내용물이 잘리지 않게 */
    }

    /* 2. 버튼 디자인 다이어트 */
    /* 버튼 내부의 뚱뚱한 여백을 전부 제거해야 폰에서 7개가 들어갑니다 */
    div.stButton > button {
        width: 100%;
        padding: 4px 0px !important;    /* 위아래 여백 */
        margin: 0px !important;
        font-size: 12px !important;     /* 글씨 크기 축소 */
        height: auto !important;
        min-height: 0px !important;
        line-height: 1.2 !important;
        border-radius: 4px !important;
    }

    /* 3. 버튼 안의 텍스트가 줄바꿈되지 않게 */
    div.stButton > button p {
        font-size: 12px !important;
    }
    
    /* 4. 모바일 화면에서 양옆 여백 제거 (화면 넓게 쓰기) */
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# [로그인 로직]
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
# [화면 구성 - 사이드바]
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
# [메인 화면 - 번호판]
# ==========================================
st.write("### 🎱 모바일 로또")

# 입력 모드 선택
mode = st.radio(
    "모드",
    ["🥇 최적 (터치시 노랑)", "🥶 최악 (터치시 파랑)"],
    horizontal=True,
    label_visibility="collapsed"
)

if "최적" in mode:
    st.session_state.mode = 'gold'
    st.caption("현재: **최적(Gold)** 입력 중")
else:
    st.session_state.mode = 'blue'
    st.caption("현재: **최악(Blue)** 입력 중")

st.write("") # 간격

# --- 번호판 그리기 ---
# 버튼을 그릴 때, 1~45 숫자를 순서대로 7개씩 끊어서 배치
# (가로 7칸이 강제 적용된 CSS 안에서 작동함)

# 1. 숫자 45개를 7개씩 나눔
rows = []
for i in range(1, 46, 7):
    # i부터 i+7까지 자름 (예: 1~7, 8~14...)
    rows.append(range(i, min(i + 7, 46)))

# 2. 줄(row)마다 컬럼(cols) 생성
for row_nums in rows:
    cols = st.columns(7) # 여기서 만들어진 7개 칸은 위 CSS 때문에 절대 세로로 안 쌓임
    
    for idx, num in enumerate(row_nums):
        # 버튼 라벨 & 색상
        label = str(num)
        is_primary = False
        
        if num in st.session_state.opt_nums:
            label = "✅" # 체크 표시
            is_primary = True
        elif num in st.session_state.worst_nums:
            label = "❌" # 엑스 표시
            is_primary = False 
        
        # 버튼 배치 (cols[0] ~ cols[6])
        cols[idx].button(
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
        st.success("생성 완료! (사이드바에서 개수 조절)")
        result_txt = ""
        for k in range(1, 11):
            s_gold = random.sample(gold_set, pick_opt)
            s_blue = random.sample(blue_set, pick_worst)
            final_nums = sorted(s_gold + s_blue)
            result_txt += f"{k}회: {final_nums}\n"
        st.code(result_txt)
