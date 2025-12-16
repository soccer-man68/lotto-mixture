import streamlit as st
import random

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="로또 모바일",
    page_icon="🎱",
    layout="centered"
)

# =========================================================
# [핵심] CSS Grid를 이용한 강제 7등분 (절대 밀리지 않음)
# =========================================================
st.markdown("""
<style>
    /* 1. 컨테이너를 Grid로 변경 (가장 강력한 해결책) */
    /* Streamlit의 줄바꿈 기능을 무시하고 무조건 7개 구역으로 나눕니다. */
    div[data-testid="stHorizontalBlock"] {
        display: grid !important;
        grid-template-columns: repeat(7, 1fr) !important; /* 1fr = 균등분할 */
        gap: 2px !important; /* 칸 사이 간격 2px */
        padding: 0px !important;
    }

    /* 2. 각 칸(Column)의 너비 제한 해제 */
    div[data-testid="column"] {
        width: 100% !important;
        min-width: 0px !important; /* 최소 너비 0 (가장 중요) */
        flex: unset !important;
        padding: 0px !important;
    }

    /* 3. 버튼 디자인 (모바일 최적화) */
    div.stButton > button {
        width: 100% !important;
        min-width: 0px !important;
        padding: 0px !important;  /* 안쪽 여백 제거 */
        margin: 0px !important;
        height: 40px !important;  /* 버튼 높이 */
        font-size: 12px !important;
        line-height: 1 !important;
        border-radius: 4px !important;
    }
    
    /* 4. 버튼 텍스트 강제 한 줄 표시 */
    div.stButton > button p {
        font-size: 11px !important;
        white-space: nowrap !important;
    }

    /* 5. 화면 전체 여백 최소화 (폰 화면 넓게 쓰기) */
    .block-container {
        padding-top: 1rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        max-width: 100% !important;
    }
    
    /* [예외 처리] 설정 메뉴 등 다른 컬럼들이 깨지지 않도록 보호 */
    /* 번호판 외의 다른 요소들은 Grid 적용을 피하기 위해 sidebar 사용 권장 */
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
# [사이드바 (설정)]
# ==========================================
# 메인 화면에 st.columns를 쓰면 위의 CSS Grid가 적용되어 버리므로
# 설정 버튼들은 무조건 사이드바에 넣어야 합니다.
with st.sidebar:
    st.header("설정 메뉴")
    st.write("🥇 **최적(Gold)**")
    pick_opt = st.selectbox("최적 개수", [0,1,2,3,4,5,6], index=4, label_visibility="collapsed")
    
    st.write("🥶 **최악(Blue)**")
    pick_worst = st.selectbox("최악 개수", [0,1,2,3,4,5,6], index=2, label_visibility="collapsed")
    
    st.write("---")
    if st.button("🔄 번호 초기화"):
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
    st.caption(f"**최적(노랑)** 입력 중 | {len(st.session_state.opt_nums)}개 선택")
else:
    st.session_state.mode = 'blue'
    st.caption(f"**최악(파랑)** 입력 중 | {len(st.session_state.worst_nums)}개 선택")

# --- 번호판 그리기 ---
# 여기서 st.columns(7)을 호출하면, CSS Grid가 작동하여
# 무조건 화면을 7등분합니다. 절대 줄바꿈되지 않습니다.
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
        
        cols[i].button(
            label if (num in st.session_state.opt_nums or num in st.session_state.worst_nums) else str(num),
            key=f"btn_{num}",
            on_click=toggle_num,
            args=(num,),
            type="primary" if is_primary or (num in st.session_state.worst_nums) else "secondary"
        )

st.divider()

if st.button("🎲 10게임 생성하기"):
    gold_set = list(st.session_state.opt_nums)
    blue_set = list(st.session_state.worst_nums)
    
    if len(gold_set) < pick_opt:
        st.error(f"최적 부족! ({len(gold_set)}/{pick_opt})")
    elif len(blue_set) < pick_worst:
        st.error(f"최악 부족! ({len(blue_set)}/{pick_worst})")
    else:
        st.success("생성 완료!")
        result_txt = ""
        for k in range(1, 11):
            s_gold = random.sample(gold_set, pick_opt)
            s_blue = random.sample(blue_set, pick_worst)
            final_nums = sorted(s_gold + s_blue)
            result_txt += f"{k}회: {final_nums}\n"
        st.code(result_txt)
