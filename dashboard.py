import streamlit as st
import json

SUMMARY_JSON_FILE = "pytorch_cluster_summaries_1000.json"

# --- 1. 데이터 로드 ---
@st.cache_data # 데이터를 캐시하여 매번 다시 로드하지 않음
def load_data():
    try:
        with open(SUMMARY_JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        st.error(f"오류: '{SUMMARY_JSON_FILE}' 파일을 찾을 수 없습니다.")
        return {}

cluster_data = load_data()

# --- 2. 대시보드 UI ---
st.set_page_config(layout="wide") # 넓은 화면 사용
st.title("PyTorch 이슈 클러스터 분석 대시보드 📊")
st.markdown(f"**총 {len(cluster_data)} 개의 유의미한 클러스터** 발견 (원본 1000개 이슈)")

# --- 3. 정렬 옵션 ---
sort_option = st.radio(
    "클러스터 정렬 기준:",
    ("이슈 개수 (많은 순)", "클러스터 ID (번호 순)"),
    horizontal=True,
)

if sort_option == "이슈 개수 (많은 순)":
    # 이슈 개수(count)를 기준으로 내림차순 정렬
    sorted_clusters = sorted(cluster_data.items(), key=lambda item: item[1]['count'], reverse=True)
else:
    # 클러스터 ID(key)를 숫자로 변환하여 오름차순 정렬
    sorted_clusters = sorted(cluster_data.items(), key=lambda item: int(item[0]))

# --- 4. 클러스터 목록 표시 ---
st.subheader("클러스터 목록")

if not sorted_clusters:
    st.warning("표시할 클러스터 데이터가 없습니다.")
else:
    # 2열 레이아웃
    col1, col2 = st.columns(2)
    
    for i, (cluster_id, data) in enumerate(sorted_clusters):
        # 2열로 번갈아 가며 표시
        target_col = col1 if i % 2 == 0 else col2 
        
        with target_col.expander(f"**Cluster {cluster_id}** ({data['count']}개 이슈)"):
            
            # (A) LLM 요약
            st.markdown("##### 🤖 LLM 요약")
            st.info(data['summary'])
            
            # (B) 이슈 목록 (드릴다운)
            st.markdown("##### Issues in this cluster:")
            for issue in data['issues']:
                issue_id = issue['id']
                issue_title = issue['title']
                issue_url = issue['url']
                # GitHub 링크와 함께 표시
                st.markdown(f"- **#{issue_id}**: [{issue_title}]({issue_url})")