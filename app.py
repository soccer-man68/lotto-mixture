import streamlit as st
import random

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="로또 생성기",
    page_icon="🎱",
    layout="centered"
)

# =========================================================
# [CSS] PC 간격 축소 + 모바일 7칸 강제 고정
# =========================================================
st.markdown("""
<style>
    /* 1. PC/모바일 공통: 컬럼 간격(Gap) 제거 */
    /* 이게 없으면 PC에서 버튼 사이가 너무 벌어집니다. */
    div[data-testid="stHorizontalBlock"] {
        gap: 0.2rem !important; /* 간격을 16px -> 3px 정도로 축소 */
    }

    /* 2. 모바일/PC 공통: 컬럼 너비 강제 고정 */
    /* 'min-width: 0'이 핵심입니다. 이게 없으면 폰에서 버튼이 밀려납니다. */
    div[data-testid="column"] {
        width: 14.28% !important;
        flex: 0 0 14.28% !important;
        min-width: 0px !important; /* 👈 1,2번만 나오는 현상 해결의 열쇠 */
        padding: 0px !important;
    }

    /* 3. 버튼 디자인 (꽉 차게 + 글자 조절) */
    div.stButton > button {
        width: 100% !important;
        padding: 0.2rem 0rem !important; /* 버튼 내부 여백 축소 */
        margin: 0px !important;
        line-height: 1 !important;
        height: auto !important;
        min-height: 35px !important; 
    }
    
    /* 4. 버튼 텍스트 크기 반응형 조절 (폰에서는 작게) */
    div.stButton > button p {
        font-size: 14px !important;
    }
    @media (max-width: 640px) {
        div.stButton > button p {
            font-size: 10px !important; /* 폰에서는 글자 작게 */
        }
    }

    /* 5. PC 화면이 너무 넓을 때 중앙 정렬 및 최대 너비 제한 */
    .block-container {
        max-width: 800px !important;
        padding-top: 1rem !important;
        padding-bottom: 5rem !important;
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
# [로직]
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
# [UI 구성]
# ==========================================
st.title("🎱 로또 커스텀")

# 설정은 st.expander(접이식 메뉴) 안에 넣어서 번호판에 영향 안 주게 함
with st.expander("⚙️ 설정 및 초기화 (눌러서 열기)", expanded=False):
    c1, c2 = st.columns(2)
    with c1:
        st.write("🥇 **최적(Gold)**")
        pick_opt = st.selectbox("개수", [0,1,2,3,4,5,6], index=4, key='opt')
    with c2:
        st.write("🥶 **최악(Blue)**")
        pick_worst = st.selectbox("개수", [0,1,2,3,4,5,6], index=2, key='worst')
    
    if st.button("🔄 번호 초기화", use_container_width=True):
        reset_all()
        st.rerun()

# 모드 선택
mode = st.radio("모드", ["🥇 최적", "🥶 최악"], horizontal=True, label_visibility="collapsed")
if "최적" in mode:
    st.session_state.mode = 'gold'
    st.caption(f"현재: **최적(노랑)** 선택 중 | {len(st.session_state.opt_nums)}개 선택됨")
else:
    st.session_state.mode = 'blue'
    st.caption(f"현재: **최악(파랑)** 선택 중 | {len(st.session_state.worst_nums)}개 선택됨")

# --- 번호판 (7열 그리드) ---
# 여기서부터는 CSS가 강력하게 적용되어 7칸으로 쪼개집니다.
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

if st.button("🎲 10게임 생성", type="primary", use_container_width=True):
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
