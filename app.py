import streamlit as st
import requests
import re
import json

# 1. 페이지 설정
st.set_page_config(page_title="AAA: AlphA AI (v1.2)", page_icon="🤖", layout="wide")

# 커스텀 CSS - Dark Tech 스타일
st.markdown("""
<style>
    /* 웹폰트 로드 */
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css');
    
    /* Streamlit 기본 헤더/푸터 숨기기 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 전체 배경 및 폰트 설정 */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1419 100%);
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Noto Sans KR', sans-serif;
    }
    
    /* 메인 컨테이너 스타일 */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* 제목 스타일 - 브랜드 로고처럼 */
    h1 {
        text-align: center;
        font-size: 3rem !important;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 2rem !important;
        letter-spacing: -0.02em;
    }
    
    /* 사이드바 스타일 */
    .css-1d391kg {
        background-color: rgba(10, 14, 39, 0.95);
        border-right: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    [data-testid="stSidebar"] {
        background-color: rgba(10, 14, 39, 0.95);
        border-right: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    /* 사이드바 헤더 스타일 */
    [data-testid="stSidebar"] h2 {
        font-size: 1.5rem;
        font-weight: 600;
        color: #667eea;
        margin-bottom: 1rem;
    }
    
    [data-testid="stSidebar"] h3 {
        font-size: 1.2rem;
        font-weight: 600;
        color: #764ba2;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
    }
    
    /* 버튼 스타일 - 그라데이션, 둥근 모서리 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* 텍스트 입력창 스타일 */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 10px;
        color: #ffffff;
        padding: 0.6rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
        background-color: rgba(255, 255, 255, 0.08);
    }
    
    /* 텍스트 영역 스타일 */
    .stTextArea > div > div > textarea {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 10px;
        color: #ffffff;
        padding: 0.8rem;
        transition: all 0.3s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
        background-color: rgba(255, 255, 255, 0.08);
    }
    
    /* 채팅 메시지 컨테이너 */
    [data-testid="stChatMessage"] {
        padding: 0;
        margin-bottom: 1.5rem;
    }
    
    /* 채팅 메시지 내용 영역 */
    [data-testid="stChatMessage"] > div {
        padding: 1.2rem 1.5rem;
        border-radius: 16px;
        margin-left: 0.5rem;
    }
    
    /* AI 메시지 배경 */
    [data-testid="stChatMessage"][data-message-author="assistant"] > div {
        background-color: rgba(255, 255, 255, 0.04);
        border-left: 4px solid rgba(102, 126, 234, 0.6);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* 사용자 메시지 배경 */
    [data-testid="stChatMessage"][data-message-author="user"] > div {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.25) 0%, rgba(118, 75, 162, 0.25) 100%);
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
    }
    
    /* 채팅 메시지 텍스트 색상 */
    [data-testid="stChatMessage"] p {
        color: rgba(255, 255, 255, 0.9);
        line-height: 1.7;
        margin: 0;
    }
    
    /* 아바타 스타일 */
    [data-testid="stChatMessage"] img {
        border-radius: 50%;
        width: 2.5rem;
        height: 2.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* 채팅 입력창 스타일 */
    .stChatInput > div > div > textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
    }
    
    .stChatInput > div > div > textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
    }
    
    /* 성공/에러 메시지 스타일 */
    .stSuccess {
        background-color: rgba(16, 185, 129, 0.15);
        border-left: 4px solid #10b981;
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stError {
        background-color: rgba(239, 68, 68, 0.15);
        border-left: 4px solid #ef4444;
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stWarning {
        background-color: rgba(245, 158, 11, 0.15);
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* 구분선 스타일 */
    hr {
        border-color: rgba(102, 126, 234, 0.2);
        margin: 1.5rem 0;
    }
    
    /* 라벨 스타일 */
    label {
        color: rgba(255, 255, 255, 0.8) !important;
        font-weight: 500;
    }
    
    /* 플레이스홀더 스타일 */
    input::placeholder, textarea::placeholder {
        color: rgba(255, 255, 255, 0.4) !important;
    }
    
    /* 스피너 스타일 */
    .stSpinner > div {
        border-color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# 브랜드 제목 - 중앙 정렬
st.markdown("<h1>🤖 AAA: AlphA AI (v1.2)</h1>", unsafe_allow_html=True)

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
    st.markdown("### 🔑 설정")
    if secret_api_key: 
        api_key = secret_api_key
        st.markdown('<div style="background-color: rgba(16, 185, 129, 0.15); border-left: 4px solid #10b981; border-radius: 8px; padding: 0.8rem; margin-bottom: 1rem;">✅ <strong>OpenAI 자동 연결</strong></div>', unsafe_allow_html=True)
    else: 
        api_key = st.text_input("🔐 OpenAI Key", type="password", placeholder="sk-...")

    if secret_notion_key: 
        notion_key = secret_notion_key
        st.markdown('<div style="background-color: rgba(16, 185, 129, 0.15); border-left: 4px solid #10b981; border-radius: 8px; padding: 0.8rem; margin-bottom: 1rem;">✅ <strong>Notion 자동 연결</strong></div>', unsafe_allow_html=True)
    else: 
        notion_key = st.text_input("🔐 Notion Key", type="password", placeholder="secret_...")

    # 페이지 URL은 항상 입력 가능
    page_url = st.text_input("🔗 Notion Page URL", placeholder="https://notion.so/...")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 읽어오기", use_container_width=True): 
            st.session_state["fetch_notion"] = True
    
    st.markdown("---")
    
    # [쓰기 기능 UI] - 추가됨!
    st.markdown("### 📝 메모 남기기")
    memo_text = st.text_area("💬 내용을 입력하세요", height=100, placeholder="여기에 메모를 작성하세요...")
    if st.button("📤 노션에 저장", use_container_width=True):
        if notion_key and page_url and memo_text:
            pid = extract_page_id(page_url)
            if pid:
                with st.spinner("💾 저장 중..."):
                    success, msg = write_to_notion(notion_key, pid, memo_text)
                    if success: 
                        st.markdown(f'<div style="background-color: rgba(16, 185, 129, 0.15); border-left: 4px solid #10b981; border-radius: 8px; padding: 0.8rem;">✅ {msg}</div>', unsafe_allow_html=True)
                    else: 
                        st.markdown(f'<div style="background-color: rgba(239, 68, 68, 0.15); border-left: 4px solid #ef4444; border-radius: 8px; padding: 0.8rem;">❌ {msg}</div>', unsafe_allow_html=True)
            else: 
                st.markdown('<div style="background-color: rgba(239, 68, 68, 0.15); border-left: 4px solid #ef4444; border-radius: 8px; padding: 0.8rem;">❌ URL을 확인하세요</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="background-color: rgba(245, 158, 11, 0.15); border-left: 4px solid #f59e0b; border-radius: 8px; padding: 0.8rem;">⚠️ 키, URL, 내용을 확인하세요</div>', unsafe_allow_html=True)

# --- 메인 로직 ---
if "messages" not in st.session_state: st.session_state.messages = []
if "notion_context" not in st.session_state: st.session_state.notion_context = ""

# 읽기 실행
if st.session_state.get("fetch_notion") and notion_key and page_url:
    pid = extract_page_id(page_url)
    if pid:
        with st.spinner("🔍 분석 중..."):
            content = get_notion_data(notion_key, pid)
            st.session_state.notion_context = content
        if "실패" not in content: 
            st.toast("✅ 데이터 로드 완료!", icon="🎉")
        else: 
            st.markdown(f'<div style="background-color: rgba(239, 68, 68, 0.15); border-left: 4px solid #ef4444; border-radius: 8px; padding: 1rem; margin-bottom: 1rem;">❌ {content}</div>', unsafe_allow_html=True)

# 채팅 화면
for msg in st.session_state.messages:
    avatar = "🧑‍💼" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar): 
        st.markdown(msg["content"])

if prompt := st.chat_input("💬 질문하세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💼"): 
        st.markdown(prompt)

    if api_key:
        sys_msg = f"너는 AlphA Inc. 비서 AAA야. 참고 데이터:\n{st.session_state.notion_context}"
        msgs = [{"role": "system", "content": sys_msg}] + st.session_state.messages
        with st.chat_message("assistant", avatar="🤖"):
            stream = call_openai_stream(api_key, msgs)
            resp = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": resp})
    else:
        st.markdown('<div style="background-color: rgba(245, 158, 11, 0.15); border-left: 4px solid #f59e0b; border-radius: 8px; padding: 1rem; margin-bottom: 1rem;">⚠️ API Key가 없습니다.</div>', unsafe_allow_html=True)