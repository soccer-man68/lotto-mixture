import streamlit as st
import random

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="나만의 시크릿 로또 조합기",
    page_icon="🔒",
    layout="centered"
)

# ==========================================
# [로그인 시스템]
# ==========================================
def check_login():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.header("🔒 접근 제한 구역")
        password_input = st.text_input("비밀번호를 입력하세요", type="password")
        
        if st.button("로그인"):
            # 👇 비밀번호 설정 (현재: 4938)
            if password_input == "4938":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("비밀번호가 틀렸습니다!")
        return False
    return True

if not check_login():
    st.stop()

# ==========================================
# [메인 앱 시작]
# ==========================================

st.title("🎱 로또 커스텀 조합기 (Easy)")
st.markdown("버튼 누르기 힘드셨죠? 이제 목록에서 쉽게 고르세요!")
st.divider()

# 모든 로또 번호 (1~45)
all_numbers = list(range(1, 46))

# --- 1. 번호 선택 구역 (여기가 확 바뀌었습니다!) ---

# (1) 최적 번호(Gold) 선택
st.subheader("🥇 최적 번호 (반드시 포함하고 싶은 수)")
# multiselect: 검색도 되고 목록에서 클릭도 되는 편리한 도구
opt_nums = st.multiselect(
    "여기를 클릭해서 번호를 고르세요 (여러 개 선택 가능)",
    all_numbers,
    placeholder="번호를 선택하거나 검색하세요..."
)

# (2) 최악 번호(Blue) 선택
# *중요*: 최적 번호에서 고른 건 뺍니다. (중복 방지)
remaining_numbers = [n for n in all_numbers if n not in opt_nums]

st.subheader("🥶 최악 번호 (피하고 싶은 수)")
worst_nums = st.multiselect(
    "여기를 클릭해서 번호를 고르세요",
    remaining_numbers,
    placeholder="최적 번호를 제외한 나머지 중에서 선택됨"
)

st.divider()

# --- 2. 추출 개수 설정 ---
col1, col2 = st.columns(2)

with col1:
    st.info(f"선택한 최적 번호: {len(opt_nums)}개")
    pick_opt = st.selectbox("🥇 몇 개를 뽑을까요?", [0,1,2,3,4,5,6], index=4)

with col2:
    st.info(f"선택한 최악 번호: {len(worst_nums)}개")
    pick_worst = st.selectbox("🥶 몇 개를 뽑을까요?", [0,1,2,3,4,5,6], index=2)

# --- 3. 조합 생성 버튼 ---
st.write("") # 여백
generate_btn = st.button("🎲 조합 10게임 생성하기", type="primary", use_container_width=True)

if generate_btn:
    # 예외 처리: 내가 가진 번호보다 뽑으려는 개수가 많으면 에러
    if len(opt_nums) < pick_opt:
        st.error(f"🚨 최적 번호가 부족합니다! (현재 {len(opt_nums)}개 선택됨 / {pick_opt}개 필요)")
    elif len(worst_nums) < pick_worst:
        st.error(f"🚨 최악 번호가 부족합니다! (현재 {len(worst_nums)}개 선택됨 / {pick_worst}개 필요)")
    else:
        st.success(f"✨ 생성 완료! (🥇{pick_opt}개 + 🥶{pick_worst}개)")
        
        # 합계 경고
        if pick_opt + pick_worst != 6:
            st.warning(f"⚠️ 참고: 총 {pick_opt + pick_worst}개의 숫자가 뽑힙니다. (로또 정식 게임은 6개)")

        # 결과 출력
        result_text = ""
        for k in range(1, 11):
            # 랜덤 추출
            selected_opt = random.sample(opt_nums, pick_opt)
            selected_worst = random.sample(worst_nums, pick_worst)
            
            # 합치고 정렬
            final_set = sorted(selected_opt + selected_worst)
            result_text += f"{k}회차:  {final_set}\n"
            
        st.code(result_text, language="python")

# 로그아웃
st.write("---")
if st.button("로그아웃"):
    st.session_state.logged_in = False
    st.rerun()
