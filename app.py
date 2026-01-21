import streamlit as st
import requests
import re
import json

# 1. 페이지 설정
st.set_page_config(page_title="AAA: AlphA AI (v1.2)", page_icon="🤖")
st.title("🤖 AAA: AlphA AI (v1.2)")

# --- 비밀 금고(Secrets)에서 키 가져오기 ---
try: secret_api_key = st.secrets["OPENAI_API_KEY"]
except: secret_api_key = ""

try: secret_notion_key = st.secrets["NOTION_KEY"]
except: secret_notion_key = ""

# --- 도구 함수들 ---
def extract_page_id(url):
    pattern = r"([a-f0-9]{32})"
    match = re.search(pattern, url)
    return match.group(1) if match else None

def call_openai_stream(api_key, messages):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"model": "gpt-4o-mini", "messages": messages, "stream": True}
    try:
        response = requests.post(url, headers=headers, json=payload, stream=True, timeout=30)
        if response.status_code != 200: raise Exception(f"HTTP {response.status_code}: {response.text}")
        for line in response.iter_lines():
            if line:
                line_text = line.decode('utf-8')
                if line_text.startswith("data: "):
                    data_str = line_text[6:]
                    if data_str == "[DONE]": break
                    try:
                        data = json.loads(data_str)
                        content = data["choices"][0]["delta"].get("content", "")
                        if content: yield content
                    except: continue
    except Exception as e:
        yield f"⚠️ 에러: {str(e)}"

# [읽기 함수]
def get_notion_data(notion_key, page_id):
    headers = {"Authorization": f"Bearer {notion_key}", "Content-Type": "application/json", "Notion-Version": "2022-06-28"}
    # 1. DB 시도
    try:
        res = requests.post(f"https://api.notion.com/v1/databases/{page_id}/query", headers=headers)
        if res.status_code == 200:
            content = "=== [노션 데이터베이스] ===\n"
            for row in res.json().get("results", []):
                row_text = []
                for name, prop in row.get("properties", {}).items():
                    val = ""
                    if prop["type"] == "title" and prop.get("title"): val = prop["title"][0].get("plain_text", "")
                    elif prop["type"] == "rich_text" and prop.get("rich_text"): val = prop["rich_text"][0].get("plain_text", "")
                    elif prop["type"] == "select": val = prop.get("select", {}).get("name", "")
                    elif prop["type"] == "status": val = prop.get("status", {}).get("name", "")
                    if val: row_text.append(f"{name}: {val}")
                content += " | ".join(row_text) + "\n"
            return content
    except: pass
    # 2. 페이지 시도
    res = requests.get(f"https://api.notion.com/v1/blocks/{page_id}/children", headers=headers)
    if res.status_code == 200:
        content = "=== [노션 페이지] ===\n"
        for block in res.json().get("results", []):
            type_ = block.get("type")
            if type_ in block and "rich_text" in block[type_]:
                text_content = ""
                for t in block[type_]["rich_text"]: text_content += t.get("plain_text", "")
                if text_content: content += f"- {text_content}\n"
        return content if len(content) > 10 else "내용 없음"
    return "읽기 실패"

# [쓰기 함수] - 추가됨!
def write_to_notion(notion_key, page_id, text_content):
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    headers = {"Authorization": f"Bearer {notion_key}", "Content-Type": "application/json", "Notion-Version": "2022-06-28"}
    payload = {
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": text_content}}]
                }
            }
        ]
    }
    try:
        response = requests.patch(url, headers=headers, json=payload)
        if response.status_code == 200: return True, "저장 성공!"
        else: return False, f"실패: {response.status_code}"
    except Exception as e: return False, str(e)

# --- 사이드바 UI ---
with st.sidebar:
    st.header("🔑 설정")
    if secret_api_key: 
        api_key = secret_api_key
        st.success("✅ OpenAI 자동 연결")
    else: api_key = st.text_input("OpenAI Key", type="password")

    if secret_notion_key: 
        notion_key = secret_notion_key
        st.success("✅ Notion 자동 연결")
    else: notion_key = st.text_input("Notion Key", type="password")

    # 페이지 URL은 항상 입력 가능
    page_url = st.text_input("Notion Page URL", placeholder="https://notion.so/...")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 읽어오기"): st.session_state["fetch_notion"] = True
    
    st.divider()
    
    # [쓰기 기능 UI] - 추가됨!
    st.subheader("📝 메모 남기기")
    memo_text = st.text_area("내용을 입력하세요", height=100)
    if st.button("📤 노션에 저장"):
        if notion_key and page_url and memo_text:
            pid = extract_page_id(page_url)
            if pid:
                with st.spinner("저장 중..."):
                    success, msg = write_to_notion(notion_key, pid, memo_text)
                    if success: st.success(msg)
                    else: st.error(msg)
            else: st.error("URL을 확인하세요")
        else:
            st.warning("키, URL, 내용을 확인하세요")

# --- 메인 로직 ---
if "messages" not in st.session_state: st.session_state.messages = []
if "notion_context" not in st.session_state: st.session_state.notion_context = ""

# 읽기 실행
if st.session_state.get("fetch_notion") and notion_key and page_url:
    pid = extract_page_id(page_url)
    if pid:
        with st.spinner("분석 중..."):
            content = get_notion_data(notion_key, pid)
            st.session_state.notion_context = content
        if "실패" not in content: 
            st.toast("✅ 데이터 로드 완료!")
        else: st.error(content)

# 채팅 화면
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("질문하세요"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    if api_key:
        sys_msg = f"너는 AlphA Inc. 비서 AAA야. 참고 데이터:\n{st.session_state.notion_context}"
        msgs = [{"role": "system", "content": sys_msg}] + st.session_state.messages
        with st.chat_message("assistant"):
            stream = call_openai_stream(api_key, msgs)
            resp = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": resp})
    else:
        st.warning("API Key가 없습니다.")