import streamlit as st
from openai import OpenAI
import requests
import re
import httpx  # 필수: pip install httpx

# --- 1. 기본 페이지 설정 ---
st.set_page_config(page_title="AAA: AlphA AI", page_icon="🤖")
st.title("🤖 AAA: AlphA AI")

# --- 2. 도구 함수들 (노션 ID 추출, 데이터 읽기) ---
def extract_page_id(url):
    # 노션 링크에서 32자리 ID만 쏙 뽑아내는 정규표현식
    pattern = r"([a-f0-9]{32})"
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_notion_data(notion_key, page_id):
    headers = {
        "Authorization": f"Bearer {notion_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    # [시도 1] 데이터베이스(표)로 읽어보기
    db_url = f"https://api.notion.com/v1/databases/{page_id}/query"
    try:
        response = requests.post(db_url, headers=headers)
        if response.status_code == 200:
            results = response.json().get("results", [])
            content = "=== [노션 데이터베이스(표) 내용] ===\n"
            for row in results:
                props = row.get("properties", {})
                row_text = []
                for name, prop in props.items():
                    # 다양한 속성 타입(텍스트, 숫자, 선택, 상태 등) 처리
                    type_ = prop.get("type")
                    val = ""
                    if type_ == "title" and prop.get("title"):
                        val = prop["title"][0].get("plain_text", "")
                    elif type_ == "rich_text" and prop.get("rich_text"):
                        val = prop["rich_text"][0].get("plain_text", "")
                    elif type_ == "number":
                        val = str(prop.get("number", ""))
                    elif type_ == "select" and prop.get("select"):
                        val = prop["select"].get("name", "")
                    elif type_ == "status" and prop.get("status"):
                        val = prop["status"].get("name", "")
                    elif type_ == "date" and prop.get("date"):
                        val = prop["date"].get("start", "")
                    
                    if val:
                        row_text.append(f"{name}: {val}")
                content += " | ".join(row_text) + "\n"
            return content
    except:
        pass # 데이터베이스가 아니면 조용히 넘어감

    # [시도 2] 일반 페이지(글)로 읽어보기
    page_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    response = requests.get(page_url, headers=headers)
    
    if response.status_code == 200:
        blocks = response.json().get("results", [])
        content = "=== [노션 페이지(글) 내용] ===\n"
        for block in blocks:
            type_ = block.get("type")
            if type_ in block and "text" in block[type_]:
                texts = block[type_]["text"]
                for text in texts:
                    content += text.get("plain_text", "")
                content += "\n"
            elif type_ in block and "rich_text" in block[type_]:
                texts = block[type_]["rich_text"]
                for text in texts:
                    content += text.get("plain_text", "")
                content += "\n"
        
        if len(content) < 30: # 내용이 너무 없으면
            return "내용을 찾을 수 없습니다. (빈 페이지거나 권한이 없는 데이터베이스입니다.)"
        return content
    else:
        return f"읽기 실패 (Error Code: {response.status_code})"

# --- 3. 사이드바 (설정 메뉴) ---
with st.sidebar:
    st.header("🔑 설정")
    api_key = st.text_input("OpenAI API Key", type="password")
    
    st.divider()
    st.subheader("📘 Notion 연동")
    notion_key = st.text_input("Notion Secret Key", type="password")
    page_url = st.text_input("연동할 Notion 페이지 링크")
    
    if st.button("노션 데이터 불러오기"):
        st.session_state["fetch_notion"] = True

# --- 4. 데이터 로드 및 상태 관리 ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "notion_context" not in st.session_state:
    st.session_state.notion_context = ""

# 버튼 눌렀을 때 노션 데이터 가져오기
if st.session_state.get("fetch_notion") and notion_key and page_url:
    page_id = extract_page_id(page_url)
    if page_id:
        with st.spinner("노션 데이터(표/글) 분석 중..."):
            content = get_notion_data(notion_key, page_id)
            st.session_state.notion_context = content
            
        if "실패" not in content and "찾을 수 없습니다" not in content:
            st.sidebar.success(f"✅ 읽기 성공! (약 {len(content)}자)")
            with st.expander("읽어온 데이터 확인"):
                st.text(content[:1000]) # 너무 길면 잘라서 보여줌
        else:
            st.sidebar.error(f"❌ {content}")
    else:
        st.sidebar.error("⚠️ 올바른 노션 링크가 아닙니다.")

# --- 5. 채팅 화면 구현 ---
# 이전 대화 기록 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input("질문을 입력하세요"):
    # 1. 내 메시지 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. AI 답변 생성
    if api_key:
        # [핵심] SSL 인증서 무시(verify=False) & 타임아웃 60초 설정
        http_client = httpx.Client(timeout=60.0, verify=False)
        client = OpenAI(api_key=api_key, http_client=http_client)
        
        # 시스템 프롬프트에 노션 데이터 주입
        system_prompt = f"""너는 AlphA Inc.의 유능한 AI 비서 AAA야. 
        아래 제공된 [사용자 노션 데이터]를 최우선으로 참고해서 질문에 답해줘.
        데이터에 없는 내용은 지어내지 말고 모른다고 해.
        
        [사용자 노션 데이터]
        {st.session_state.notion_context}
        """

        with st.chat_message("assistant"):
            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": system_prompt}]
                         + st.session_state.messages
            )
            answer = res.choices[0].message.content
            st.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )
