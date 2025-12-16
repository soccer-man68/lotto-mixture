import streamlit as st
import random

# --- 1. 페이지 설정 (가장 먼저 와야 함) ---
st.set_page_config(
    page_title="나만의 시크릿 로또 조합기",
    page_icon="🔒",
    layout="centered"
)

# ==========================================
# [추가된 기능] 로그인 시스템
# ==========================================
def check_login():
    # 세션에 로그인 상태 변수가 없으면 초기화
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    # 로그인이 안 된 상태라면? 로그인 화면 보여주기
    if not st.session_state.logged_in:
        st.header("🔒 접근 제한 구역")
        st.write("관계자 외 출입금지입니다. 비밀번호를 입력하세요.")
        
        # 비밀번호 입력칸
        password_input = st.text_input("비밀번호", type="password")
        
        if st.button("로그인"):
            # 👇 여기서 비밀번호를 변경하세요! (현재: 4938)
            if password_input == "4938":
                st.session_state.logged_in = True
                st.rerun() # 화면 새로고침해서 앱 보여주기
            else:
                st.error("비밀번호가 틀렸습니다! 땡! 🚨")
        
        return False # 로그인 실패 상태
    return True # 로그인 성공 상태

# 로그인 체크 실행 (로그인 안 되어 있으면 여기서 코드 실행 멈춤)
if not check_login():
    st.stop()

# ==========================================
# [원래 기능] 로또 앱 메인 코드
# (로그인이 성공해야만 아래 코드가 실행됩니다)
# ==========================================

# --- 2. 세션 상태 초기화 ---
if 'opt_nums' not in st.session_state:
    st.session_state.opt_nums = set()
if 'worst_nums' not in st.session_state:
    st.session_state.worst_nums = set()
if 'input_mode' not in st.session_state:
    st.session_state.input_mode = 'opt'

# --- 3. 함수 정의 ---
def toggle_number(n):
    mode = st.session_state.input_mode
    in_opt = n in st.session_state.opt_nums
    in_worst = n in st.session_state.worst_nums
    
    if mode == 'opt': 
        if in_opt:
            st.session_state.opt_nums.remove(n)
        else:
            if in_worst: st.session_state.worst_nums.remove(n)
            st.session_state.opt_nums.add(n)
            
    else: 
        if in_worst:
            st.session_state.worst_nums.remove(n)
        else:
            if in_opt: st.session_state.opt_nums.remove(n)
            st.session_state.worst_nums.add(n)

def reset_nums():
    st.session_state.opt_nums.clear()
    st.session_state.worst_nums.clear()

# --- 4. 메인 화면 디자인 ---
st.title("🎱 로또 커스텀 조합기 (VIP)")
st.markdown("인증된 사용자만 접근 가능한 시크릿 페이지입니다.")

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader("🥇 최적(Gold)")
    pick_opt = st.selectbox("추출 개수", [0,1,2,3,4,5,6], index=4, key="cnt_opt")
    st.caption(f"선택: {len(st.session_state.opt_nums)}개")

with col2:
    st.subheader("🥶 최악(Blue)")
    pick_worst = st.selectbox("추출 개수", [0,1,2,3,4,5,6], index=2, key="cnt_worst")
    st.caption(f"선택: {len(st.session_state.worst_nums)}개")

st.divider()

mode_select = st.radio(
    "👉 번호 입력 모드 선택",
    ('🥇 최적 번호 입력 중', '🥶 최악 번호 입력 중'),
    horizontal=True
)

if '최적' in mode_select:
    st.session_state.input_mode = 'opt'
else:
    st.session_state.input_mode = 'worst'

if st.button("🔄 전체 초기화"):
    reset_nums()
    st.rerun()

st.write("### 번호 선택판")
grid_cols = st.columns(7) 

for i in range(1, 46):
    col_idx = (i - 1) % 7
    button_col = grid_cols[col_idx]
    
    label = str(i)
    is_primary = False 
    
    if i in st.session_state.opt_nums:
        label = f"🥇{i}"
        is_primary = True
    elif i in st.session_state.worst_nums:
        label = f"🥶{i}"
        
    button_col.button(
        label, 
        key=f"btn_{i}", 
        on_click=toggle_number, 
        args=(i,), 
        use_container_width=True,
        type="primary" if is_primary else "secondary"
    )

st.write("---")
generate_btn = st.button("🎲 시크릿 조합 10게임 생성", type="primary", use_container_width=True)

if generate_btn:
    opt_pool = list(st.session_state.opt_nums)
    worst_pool = list(st.session_state.worst_nums)
    
    if len(opt_pool) < pick_opt:
        st.error(f"최적 번호 부족! ({len(opt_pool)}/{pick_opt})")
    elif len(worst_pool) < pick_worst:
        st.error(f"최악 번호 부족! ({len(worst_pool)}/{pick_worst})")
    else:
        st.success("✨ 조합 생성 완료!")
        result_text = ""
        for k in range(1, 11):
            current_opt = random.sample(opt_pool, pick_opt)
            current_worst = random.sample(worst_pool, pick_worst)
            final_set = sorted(current_opt + current_worst)
            result_text += f"{k}회차:  {final_set}\n"
        st.code(result_text, language="python")

# 로그아웃 버튼 (맨 아래 추가)
st.write("---")
if st.button("로그아웃"):
    st.session_state.logged_in = False
    st.rerun()