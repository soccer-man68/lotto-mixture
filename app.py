import streamlit as st
import random

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="로또 생성기",
    page_icon="🎱",
    layout="centered"
)

# =========================================================
# [CSS] PC 간격 축소 + 모바일 7칸 강제 고정 (완성본)
# =========================================================
st.markdown("""
<style>
/* 1. 가로 줄바꿈 절대 금지 (모바일 1,2번만 보이는 문제 해결) */
div[data-testid="stHorizontalBlock"] {
    gap: 0.2rem !important;
    flex-wrap: nowrap !important;
}

/* 2. 컬럼 폭 7칸 강제 고정 */
div[data-testid="column"] {
    flex: 0 0 14.28% !important;
    width: 14.28% !important;
    max-width: 14.28% !important;
    min-width: 0 !important;
    padding: 0 !important;
}

/* 3. 버튼 꽉 차게 */
div.stButton > button {
    width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
    min-height: 32px !important;
    line-height: 1 !important;
}

/* 4. 버튼 글자 크기 */
div.stButton > button p {
    font-size: 14px !important;
}
@media (max-width: 640px) {
    div.stButton > button p {
        font-size: 10px !important;
    }
}

/* 5. 전체 화면 폭 제한 */
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
            st.session_state.worst_nums.discard(n)
            st.session_state.opt_nums.add(n)
    else:
        if n in st.session_state.worst_nums:
            st.session_state.worst_nums.remove(n)
        else:
            st.session_state.opt_nums.discard(n)
            st.session_state.worst_nums.add(n)

def reset_all():
    st.session_state.opt_nums.clear()
    st.session_state.worst_nums.clear()

# ==========================================
# [UI]
# ==========================================
st.title("🎱 로또 커스텀")

with st.expander("⚙️ 설정 및 초기화", expanded=False):
    c1, c2 = st.columns(2)
    with c1:
        st.write("🥇 최적")
        pick_opt = st.selectbox("개수", [0,1,2,3,4,5,6], index=4)
    with c2:
        st.write("🥶 최악")
        pick_worst = st.selectbox("개수", [0,1,2,3,4,5,6], index=2)

    if st.button("🔄 번호 초기화", use_container_width=True):
        reset_all()
        st.rerun()

mode = st.radio("모드", ["🥇 최적", "🥶 최악"], horizontal=True, label_visibility="collapsed")
if "최적" in mode:
    st.session_state.mode = 'gold'
    st.caption(f"현재: 최적 선택 중 ({len(st.session_state.opt_nums)}개)")
else:
    st.session_state.mode = 'blue'
    st.caption(f"현재: 최악 선택 중 ({len(st.session_state.worst_nums)}개)")

# ==========================================
# [번호판] 7열 고정
# ==========================================
for row_start in range(1, 46, 7):
    cols = st.columns(7)
    for i in range(7):
        num = row_start + i
        if num > 45:
            break

        label = str(num)
        btn_type = "secondary"

        if num in st.session_state.opt_nums:
            label = "✅"
            btn_type = "primary"
        elif num in st.session_state.worst_nums:
            label = "❌"
            btn_type = "primary"

        cols[i].button(
            label,
            key=f"btn_{num}",
            on_click=toggle_num,
            args=(num,),
            type=btn_type
        )

st.divider()

# ==========================================
# [결과 생성]
# ==========================================
if st.button("🎲 10게임 생성", type="primary", use_container_width=True):
    gold = list(st.session_state.opt_nums)
    blue = list(st.session_state.worst_nums)

    if len(gold) < pick_opt:
        st.error("최적 번호가 부족합니다.")
    elif len(blue) < pick_worst:
        st.error("최악 번호가 부족합니다.")
    else:
        result = ""
        for i in range(1, 11):
            nums = sorted(
                random.sample(gold, pick_opt) +
                random.sample(blue, pick_worst)
            )
            result += f"{i}회: {nums}\n"
        st.code(result)
