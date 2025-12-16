import streamlit as st
import random

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="모바일 로또 조합기",
    page_icon="📱",
    layout="centered"
)

# =========================================================
# [핵심] 모바일에서도 가로 7칸을 강제로 유지하는 스타일 설정
# =========================================================
st.markdown("""
<style>
    /* 폰에서 버튼 안의 글자 크기와 여백을 확 줄임 */
    div.stButton > button {
        width: 100%;
        padding: 5px 0px !important; /* 위아래 여백 축소 */
        font-size: 14px !important;  /* 글자 크기 조절 */
        min-height: 0px !important;  /* 버튼 최소 높이 제거 */
        margin-bottom: 2px !important;
    }

    /* 화면이 좁을 때(모바일) 강제로 컬럼을 가로로 유지 */
    @media (max-width: 640px) {
        div[data-testid="column"] {
            width: 14.2% !important;     /* 7등분 (100% / 7) */
            flex: 0 0 14.2% !important;
            min-width: 0px !important;
            padding: 1px !important;     /* 좌우 간격 거의 없앰 */
        }
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
        st.warning("🔒 관계자 외 출입금지")
        password_input = st.text_input("비밀번호", type="password")
        if st.button("로그인", use_container_width=True):
            if password_input == "1234": # 👈 비밀번호 변경
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("비밀번호 오류!")
        return False
    return True

if not check_login():
    st.stop()

# ==========================================
# [메인 로직]
# ==========================================

# 세션 초기화
if 'opt_nums' not in st.session_state:
    st.session_state.opt_nums = set()
if 'worst_nums' not in st.session_state:
    st.session_state.worst_nums = set()
if 'mode' not in st.session_state:
    st.session_state.mode = 'gold' 

# 번호 토글 함수
def toggle_num(n):
    mode = st.session_state.mode
    in_gold = n in st.session_state.opt_nums
    in_blue = n in st.session_state.worst_nums
    
    if mode == 'gold': 
        if in_gold:
            st.session_state.opt_nums.remove(n) 
        else:
            if in_blue: st.session_state.worst_nums.remove(n)
            st.session_state.opt_nums.add(n)
            
    elif mode == 'blue': 
        if in_blue:
            st.session_state.worst_nums.remove(n) 
        else:
            if in_gold: st.session_state.opt_nums.remove(n) 
            st.session_state.worst_nums.add(n) 

def reset_all():
    st.session_state.opt_nums.clear()
    st.session_state.worst_nums.clear()

# ==========================================
# [화면 구성]
# ==========================================

# 1. 사이드바 (설정 메뉴를 옆으로 뺌)
with st.sidebar:
    st.header("⚙️ 설정 메뉴")
    st.info("여기서 추출 개수를 정하세요")
    
    st.markdown("---")
    st.write("🥇 **최적(Gold) 개수**")
    pick_opt = st.selectbox("최적 개수", [0,1,2,3,4,5,6], index=4, label_visibility="collapsed")
    st.caption(f"선택됨: {len(st.session_state.opt_nums)}개")
    
    st.markdown("---")
    st.write("🥶 **최악(Blue) 개수**")
    pick_worst = st.selectbox("최악 개수", [0,1,2,3,4,5,6], index=2, label_visibility="collapsed")
    st.caption(f"선택됨: {len(st.session_state.worst_nums)}개")
    
    st.markdown("---")
    if st.button("로그아웃"):
        st.session_state.logged_in = False
        st.rerun()

# 2. 메인 화면 (번호판 집중)
st.title("🎱 로또 조합기")

# 모드 선택 버튼 (가로형)
mode = st.radio(
    "입력 모드",
    ["🥇 최적 모드", "🥶 최악 모드"],
    horizontal=True,
    label_visibility="collapsed"
)

# 모드 상태 업데이트 및 초기화 버튼 배치
col_ctrl1, col_ctrl2 = st.columns([3, 1])
with col_ctrl1:
    if "최적" in mode:
        st.session_state.mode = 'gold'
        st.caption("현재: 🥇 최적 번호 입력 중 (노란색)")
    else:
        st.session_state.mode = 'blue'
        st.caption("현재: 🥶 최악 번호 입력 중 (파란색)")
with col_ctrl2:
    if st.button("초기화"):
        reset_all()
        st.rerun()

# --- 번호판 그리드 (모바일 강제 적용) ---
grid_cols = st.columns(7) # 7개 컬럼 생성

for i in range(1, 46):
    col_idx = (i - 1) % 7
    
    label = str(i)
    is_primary = False
    
    # 이모티콘 대신 색상으로 구분 (모바일 공간 절약)
    # 🥇, 🥶 이모티콘은 폰에서 자리를 많이 차지하므로 심플하게 갑니다
    if i in st.session_state.opt_nums:
        label = "✅" 
        is_primary = True
    elif i in st.session_state.worst_nums:
        label = "❌"
        is_primary = False 
    
    # 버튼 생성
    grid_cols[col_idx].button(
        label if (i in st.session_state.opt_nums or i in st.session_state.worst_nums) else str(i),
        key=f"btn_{i}",
        on_click=toggle_num,
        args=(i,),
        type="primary" if is_primary or (i in st.session_state.worst_nums) else "secondary"
    )

st.divider()

# 생성 버튼
if st.button("🎲 조합 10게임 생성", type="primary", use_container_width=True):
    gold_set = list(st.session_state.opt_nums)
    blue_set = list(st.session_state.worst_nums)
    
    if len(gold_set) < pick_opt:
        st.error(f"최적 번호 부족! ({len(gold_set)}/{pick_opt})")
    elif len(blue_set) < pick_worst:
        st.error(f"최악 번호 부족! ({len(blue_set)}/{pick_worst})")
    else:
        st.success("조합 생성 완료! (설정은 사이드바 확인)")
        
        result_txt = ""
        for k in range(1, 11):
            s_gold = random.sample(gold_set, pick_opt)
            s_blue = random.sample(blue_set, pick_worst)
            final_nums = sorted(s_gold + s_blue)
            result_txt += f"{k}회차: {final_nums}\n"
            
        st.code(result_txt)
