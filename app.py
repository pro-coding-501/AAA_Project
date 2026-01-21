import streamlit as st
import requests
import re
import json

# 1. 페이지 설정
st.set_page_config(page_title="AAA: AlphA AI", page_icon="🤖")
st.title("🤖 AAA: AlphA AI")

# --- OpenAI API 직접 호출 함수 (requests 사용) ---
def call_openai_stream(api_key, messages):
    """
    requests 라이브러리만 사용하여 OpenAI Chat Completion API를 직접 호출합니다.
    스트리밍 응답을 처리하여 텍스트를 실시간으로 반환합니다.
    """
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-4o-mini",
        "messages": messages,
        "stream": True
    }
    
    try:
        # 스트리밍 요청
        response = requests.post(url, headers=headers, json=payload, stream=True, timeout=30)
        
        # HTTP 에러 체크
        if response.status_code != 200:
            error_detail = response.text
            try:
                error_json = response.json()
                error_message = error_json.get("error", {}).get("message", error_detail)
            except:
                error_message = f"HTTP {response.status_code}: {error_detail}"
            raise Exception(f"OpenAI API 호출 실패: {error_message}")
        
        # SSE 스트리밍 응답 파싱
        full_text = ""
        for line in response.iter_lines():
            if line:
                line_text = line.decode('utf-8')
                
                # SSE 형식: "data: {...}" 또는 "data: [DONE]"
                if line_text.startswith("data: "):
                    data_str = line_text[6:]  # "data: " 제거
                    
                    if data_str == "[DONE]":
                        break
                    
                    try:
                        data = json.loads(data_str)
                        choices = data.get("choices", [])
                        if choices:
                            delta = choices[0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                full_text += content
                                yield content
                    except json.JSONDecodeError as e:
                        # JSON 파싱 에러는 무시하고 계속 진행
                        continue
        
        return full_text
        
    except requests.exceptions.Timeout:
        raise Exception("OpenAI API 연결 시간 초과: 서버 응답이 30초를 초과했습니다.")
    except requests.exceptions.ConnectionError as e:
        raise Exception(f"OpenAI API 연결 실패: 네트워크 연결을 확인해주세요. ({str(e)})")
    except requests.exceptions.RequestException as e:
        raise Exception(f"OpenAI API 요청 실패: {str(e)}")
    except Exception as e:
        raise Exception(f"예상치 못한 에러: {str(e)}")

# --- 도구 함수 (노션 데이터 읽기) ---
def extract_page_id(url):
    pattern = r"([a-f0-9]{32})"
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_notion_data(notion_key, page_id):
    headers = {
        "Authorization": f"Bearer {notion_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    # [시도 1] 데이터베이스(표) 쿼리
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
                    # 텍스트, 타이틀, 숫자 등 주요 속성만 추출
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
                    
                    if val:
                        row_text.append(f"{name}: {val}")
                content += " | ".join(row_text) + "\n"
            return content
    except:
        pass # DB가 아니면 패스

    # [시도 2] 페이지 블록(글) 조회
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
        
        if len(content) < 10:
            return "내용을 찾을 수 없습니다. (빈 페이지거나 권한이 없는 데이터베이스입니다.)"
        return content
    else:
        return f"읽기 실패 (Error Code: {response.status_code})"

# 2. 사이드바 설정
with st.sidebar:
    st.header("🔑 설정")
    api_key = st.text_input("OpenAI API Key", type="password")
    
    st.divider()
    st.subheader("📘 Notion 연동")
    notion_key = st.text_input("Notion Secret Key", type="password")
    page_url = st.text_input("연동할 Notion 페이지 링크")
    
    if st.button("노션 데이터 불러오기"):
        st.session_state["fetch_notion"] = True

# 3. 데이터 로드 및 저장
if "messages" not in st.session_state:
    st.session_state.messages = []
if "notion_context" not in st.session_state:
    st.session_state.notion_context = ""

if st.session_state.get("fetch_notion") and notion_key and page_url:
    page_id = extract_page_id(page_url)
    if page_id:
        with st.spinner("데이터 분석 중..."):
            content = get_notion_data(notion_key, page_id)
            st.session_state.notion_context = content
            
        if "실패" not in content and "찾을 수 없습니다" not in content:
            st.sidebar.success("✅ 읽기 성공!")
            with st.expander("데이터 확인"):
                st.text(content[:1000])
        else:
            st.sidebar.error(f"❌ {content}")
    else:
        st.sidebar.error("⚠️ 올바른 링크가 아닙니다.")

# 4. 채팅 인터페이스
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("질문을 입력하세요"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if api_key:
        try:
            system_prompt = f"""너는 AlphA Inc.의 AI 비서 AAA야. 
            아래 [노션 데이터]를 참고해서 질문에 답해줘.
            
            [노션 데이터]
            {st.session_state.notion_context}
            """

            messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages
            
            with st.chat_message("assistant"):
                # requests를 사용한 직접 호출 (스트리밍)
                stream_generator = call_openai_stream(api_key, messages)
                response = st.write_stream(stream_generator)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        except Exception as e:
            st.error(f"에러 발생: {e}")
    else:
        st.warning("API Key를 입력해주세요!")