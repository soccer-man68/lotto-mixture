import streamlit as st
import random

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="모바일 로또",
    page_icon="📱",
    layout="centered"
)

# =========================================================
# [핵심] 모바일에서도 가로 7칸을 강제로 유지하는 "핵" 코드
# =========================================================
st.markdown("""
<style>
    /* 1. 모바일에서 강제로 줄바꿈되는 것을 막고, 무조건 1/7 크기로 고정 */
    [data-testid="column"] {
        width: 14.28% !important;
        flex: 0 0 14.28% !important;
        min-width: 0 !important;
        padding: 1px !important; /* 간격 최소화 */
    }

    /* 2. 버튼 디자인: 폰에서 터치하기 좋게 크기 조절 */
    div.stButton > button {
        width: 100%;
        padding: 8px 0px !important; /* 위아래 여백 */
        font-size: 14px !important;  /* 글자 크기 */
        line-height: 1.2 !important;
        margin-bottom: 4px !important;
        border-radius: 5px !important;
        min-height: 0px !important;
    }
    
    /* 3. 사이드바나 다른 곳의 컬럼은 깨지지 않게 보호하는 예외처리 */
    /* (사이드바는 원래 좁으니 냅두고, 메인 화면만 적용됨) */
</style>
""", unsafe_allow_html=True)

# ==========================================
# [로그인]
# ==========================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.warning("🔒 관계자 외 출입금지")
    pw = st.text_input("비밀번호", type="password")
    if st.button("로그인", use_container_width=True):
        if pw == "0207": # 👈 비번 변경
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("땡!")
    st.stop()

# ==========================================
# [메인 로직]
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
# [화면 구성 - 사이드바에 설정 몰아넣기]
# ==========================================
# 메인 화면에서 컬럼(st.columns)을 쓰면 위의 강제 CSS 때문에 
# 모양이 이상해질 수 있어서, 설정 버튼들은 전부 사이드바로 뺐습니다.
with st.sidebar:
    st.header("⚙️ 설정 & 메뉴")
    
    st.write("---")
    st.write("🥇 **최적(Gold) 개수**")
    pick_opt = st.selectbox("최적 개수", [0,1,2,3,4,5,6], index=4, label_visibility="collapsed")
    st.caption(f"현재 선택: {len(st.session_state.opt_nums)}개")
    
    st.write("---")
    st.write("🥶 **최악(Blue) 개수**")
    pick_worst = st.selectbox("최악 개수", [0,1,2,3,4,5,6], index=2, label_visibility="collapsed")
    st.caption(f"현재 선택: {len(st.session_state.worst_nums)}개")
    
    st.write("---")
    if st.button("🔄 전체 초기화", use_container_width=True):
        reset_all()
        st.rerun()
        
    if st.button("로그아웃", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

# ==========================================
# [메인 화면 - 번호판]
# ==========================================
st.title("🎱 모바일 로또")

# 입력 모드 선택 (라디오 버튼은 세로로 쌓이지 않음)
mode = st.radio(
    "모드 선택",
    ["🥇 최적 모드 (클릭시 Gold)", "🥶 최악 모드 (클릭시 Blue)"],
    horizontal=True,
    label_visibility="collapsed"
)

if "최적" in mode:
    st.session_state.mode = 'gold'
    st.caption("👇 **최적 번호**를 선택하세요 (노란색)")
else:
    st.session_state.mode = 'blue'
    st.caption("👇 **최악 번호**를 선택하세요 (파란색)")

st.write("") # 약간의 여백

# --- 번호판 그리기 (가로 7개씩 끊어서 그리기) ---
# 이렇게 해야 1,2,3,4... 순서대로 가로로 나옵니다.
for row in range(7): # 0행 ~ 6행 (총 7줄)
    cols = st.columns(7) # 한 줄에 7칸 생성
    
    for col in range(7): # 0열 ~ 6열
        num = row * 7 + col + 1 # 번호 계산 (1, 2, 3...)
        
        if num > 45: break # 45번 넘으면 중단
        
        # 버튼 스타일(색상) 결정
        label = str(num)
        is_primary = False
        
        # 모바일 공간 절약을 위해 이모티콘 대신 심플하게
        if num in st.session_state.opt_nums:
            label = "✅" 
            is_primary = True
        elif num in st.session_state.worst_nums:
            label = "❌"
            is_primary = False 
        
        # 해당 칸(cols[col])에 버튼 배치
        cols[col].button(
            label if (num in st.session_state.opt_nums or num in st.session_state.worst_nums) else str(num),
            key=f"btn_{num}",
            on_click=toggle_num,
            args=(num,),
            type="primary" if is_primary or (num in st.session_state.worst_nums) else "secondary"
        )

st.divider()

# 조합 생성 버튼
if st.button("🎲 조합 10게임 생성", type="primary", use_container_width=True):
    gold_set = list(st.session_state.opt_nums)
    blue_set = list(st.session_state.worst_nums)
    
    if len(gold_set) < pick_opt:
        st.error(f"최적 번호 부족! ({len(gold_set)}/{pick_opt})")
    elif len(blue_set) < pick_worst:
        st.error(f"최악 번호 부족! ({len(blue_set)}/{pick_worst})")
    else:
        st.success("🎉 생성 완료! (사이드바에서 개수 조절 가능)")
        
        result_txt = ""
        for k in range(1, 11):
            s_gold = random.sample(gold_set, pick_opt)
            s_blue = random.sample(blue_set, pick_worst)
            final_nums = sorted(s_gold + s_blue)
            result_txt += f"{k}회: {final_nums}\n"
            
        st.code(result_txt)
