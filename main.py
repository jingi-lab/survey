import streamlit as st
from datetime import date
import json

st.set_page_config(page_title="상상국어 모의고사 베타베스트 – 검토 설문", layout="wide")
st.title("2026학년도 상상국어 모의고사 베타베스트 – 검토 설문")

# Ⅰ. 회차 평가 ---------------------------------------------------------------
with st.form(key="meta"):
    st.subheader("Ⅰ. 회차 평가")
    col1, col2, col3 = st.columns(3)
    with col1:
        round_no = st.text_input("회차(예: 00차)")
    with col2:
        review_date = st.date_input("검토일", value=date.today())
    with col3:
        reviewer = st.text_input("검토자")

    st.markdown("#### 회차 종합 평가")
    meta_difficulty = st.slider("난이도 (5점)", 1, 5, 3, format="%d점")
    meta_quality   = st.slider("퀄리티 (5점)", 1, 5, 3, format="%d점")
    meta_overall   = st.slider("종합평가 (5점)", 1, 5, 3, format="%d점")

    st.markdown("#### 영역별 만족도")
    area_cols = st.columns(5)
    areas = ["독서","문학","화작","언어","매체"]
    area_scores = {label: col.slider(label, 1, 5, 3, key=f"area_{label}", format="%d점")
                   for label, col in zip(areas, area_cols)}


# Ⅱ. 지문 세트 및 문항 평가 ---------------------------------------------------
st.subheader("Ⅱ. 지문세트 및 문항 평가")
passage_sets = [("독서_1", range(1,4)),
                ("독서_2", range(4,8)),
                ("독서_3", range(8,12))]   # 필요 시 계속 추가

responses = {}
for pid, qnums in passage_sets:
    with st.expander(f"{pid} 세트", expanded=False):
        diff     = st.slider("난이도", 1, 5, 3, key=f"diff_{pid}")
        qual     = st.slider("퀄리티", 1, 5, 3, key=f"qual_{pid}")
        overall  = st.slider("종합평가", 1, 5, 3, key=f"overall_{pid}")

        checklist_opts = ["지문 난이도 ↑","지문 난이도 ↓","문항 난이도 ↑","문항 난이도 ↓",
                          "지문 내용 오류/의심","제재 호감도 낮음","정보량 과다/부족",
                          "글 모호","글 정돈 불량","정오답 모호/근거 부족","추론 과함","선지 오류/의심"]
        issues   = st.multiselect("해당 항목 선택", checklist_opts, key=f"issues_{pid}")
        comment  = st.text_area("세트 종합 코멘트", key=f"comment_{pid}")

        st.write("#### 문항별 검토")
        for q in qnums:
            st.radio(f"{q}번", ["good","수정","삭제","오답"], key=f"{pid}_q{q}", horizontal=True)

        responses[pid] = {"difficulty": diff, "quality": qual, "overall": overall,
                          "issues": issues, "comment": comment,
                          "questions": {q: st.session_state[f'{pid}_q{q}'] for q in qnums}}

# 제출 -----------------------------------------------------------------------
st.markdown("## 제출")
if st.button("📤 응답 제출"):
    output = {"meta": {"round": round_no,
                       "review_date": review_date.isoformat(),
                       "reviewer": reviewer,
                       "difficulty": meta_difficulty,
                       "quality": meta_quality,
                       "overall": meta_overall,
                       "area_scores": area_scores},
              "passage_sets": responses}
    st.success("JSON 데이터가 생성되었습니다. 다운로드 후 공유해주세요!")
    st.json(output, expanded=False)
    st.download_button("⬇️ JSON 다운로드",
        data=json.dumps(output, indent=2, ensure_ascii=False),
        file_name="survey_response.json",
        mime="application/json")
