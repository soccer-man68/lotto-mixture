import streamlit as st
import random

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="로또 모바일",
    page_icon="🎱",
    layout="centered"
)

# =========================================================
# [핵심 CSS] "모든 컬럼을 무조건 1/7로 고정하라"
# =========================================================
st.markdown("""
<style>
    /* 1. 이 페이지에 있는 모든 '칸(Column)'은 무조건 14.28% 너비를 가진다. */
    /* 다른 설정(최소 너비 등)은 전부 무시(!important)한다. */
    div[data-testid="column"] {
        width: 14.28% !important;
        flex: 0 0 14.28% !important;
        min-width: 0px !important;
        max-width: 14.28% !important;
        padding: 1px !important; /* 칸 사이 간격 1px */
        overflow: hidden !important; /* 튀어나오면 자름 */
    }

    /* 2. 칸들을 감싸는 부모 틀의 간격을 없앤다. */
    div[data-testid="stHorizontalBlock"] {
        gap: 0px !important;
        flex-wrap: nowrap !important; /* 줄바꿈 절대 금지 */
    }

    /* 3. 버튼 크기와 글자 크기를 확 줄인다. */
    div.stButton > button {
        width: 100% !important;
        padding: 0px !important;
        margin: 0px !important;
        height: 35px !important;   /* 버튼 높이 */
        font-size: 10px !important; /* 글자 크기 10px */
        line-height: 1 !important;
        border: 1px solid #ddd !important; /* 경계선 얇게 */
    }
    
    /* 4. 버튼 안의 텍스트가 두 줄이 되지 않게 한다. */
    div.stButton > button p {
        font-size: 10px !important;
        white-space: nowrap !important;
    }

    /* 5. 전체 화면 여백을 최소화해서 공간을 확보한다. */
    .block-container {
        padding-left: 0.2rem !important;
        padding-right: 0.2rem !important;
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
    if st.button("로그인"): # 여기는 use_container_width 안 씀 (CSS 충돌 방지)
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
# [사이드바 메뉴] (화면 공간 확보를 위해 전부 이쪽으로 뺌)
# ==========================================
with st.sidebar:
    st.header("설정 메뉴")
    st.write("---")
    st.write("🥇 **최적(Gold)**")
    pick_opt = st.selectbox("최적 개수", [0,1,2,3,4,5,6], index=4, label_visibility="collapsed")
    st.caption(f"선택: {len(st.session_state.opt_nums)}개")
    
    st.write("---")
    st.write("🥶 **최악(Blue)**")
    pick_worst = st.selectbox("최악 개수", [0,1,2,3,4,5,6], index=2, label_visibility="collapsed")
    st.caption(f"선택: {len(st.session_state.worst_nums)}개")
    
    st.write("---")
    # 초기화 버튼
    if st.button("🔄 번호 초기화"):
        reset_all()
        st.rerun()

# ==========================================
# [메인 화면]
# ==========================================
st.write("### 🎱 모바일 로또")

# 모드 선택 (여기는 columns 안 쓰고 그냥 라디오 버튼으로 둠)
# columns를 쓰면 위의 강력한 CSS 때문에 모양이 깨질 수 있어서 피함
mode = st.radio(
    "모드 선택",
    ["🥇 최적 (터치시 노랑)", "🥶 최악 (터치시 파랑)"],
    label_visibility="collapsed"
)

if "최적" in mode:
    st.session_state.mode = 'gold'
    st.info("현재: **최적(Gold)** 입력 중")
else:
    st.session_state.mode = 'blue'
    st.info("현재: **최악(Blue)** 입력 중")

# --- 번호판 그리기 (유일하게 columns를 쓰는 곳) ---
# 위의 CSS가 오직 이것만을 위해 존재합니다.
for row_start in range(1, 46, 7):
    cols = st.columns(7) # 무조건 14.28%씩 쪼개짐
    
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
        
        # 버튼 생성
        cols[i].button(
            label if (num in st.session_state.opt_nums or num in st.session_state.worst_nums) else str(num),
            key=f"btn_{num}",
            on_click=toggle_num,
            args=(num,),
            type="primary" if is_primary or (num in st.session_state.worst_nums) else "secondary"
        )

st.divider()

# 생성 버튼 (CSS 충돌 방지를 위해 use_container_width 안 씀)
if st.button("🎲 10게임 생성하기"):
    gold_set = list(st.session_state.opt_nums)
    blue_set = list(st.session_state.worst_nums)
    
    if len(gold_set) < pick_opt:
        st.error(f"최적 번호 부족! ({len(gold_set)}/{pick_opt})")
    elif len(blue_set) < pick_worst:
        st.error(f"최악 번호 부족! ({len(blue_set)}/{pick_worst})")
    else:
        st.success("생성 완료! (메뉴를 열어 개수 확인)")
        result_txt = ""
        for k in range(1, 11):
            s_gold = random.sample(gold_set, pick_opt)
            s_blue = random.sample(blue_set, pick_worst)
            final_nums = sorted(s_gold + s_blue)
            result_txt += f"{k}회: {final_nums}\n"
        st.code(result_txt)
