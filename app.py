import streamlit as st
import requests
import re
import json
import base64

# 1. 페이지 설정
st.set_page_config(page_title="AAA: AlphA AI (v1.2)", page_icon="🤖", layout="wide")

# 로고 이미지 인코딩 함수
def get_logo_base64():
    try:
        with open("AlphA AI2 1.png", "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

logo_base64 = get_logo_base64()

# Apple-style Minimalist Dark 테마 CSS
st.markdown(f"""
<style>
    /* Streamlit 기본 푸터 숨기기 */
    footer {{visibility: hidden;}}
    
    /* 전체 배경 - Pure Black */
    .stApp {{
        background: #000000;
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif;
        min-height: 100vh;
        letter-spacing: -0.01em;
    }}
    
    /* 메인 컨테이너 */
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }}
    
    /* 로고 컨테이너 - 상단 중앙 */
    .logo-header {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 3rem;
        margin-top: 2rem;
        padding: 1rem 0;
    }}
    
    .logo-container {{
        width: 120px;
        height: 120px;
        display: flex;
        justify-content: center;
        align-items: center;
    }}
    
    .logo-container img {{
        width: 100%;
        height: 100%;
        object-fit: contain;
    }}
    
    /* 사이드바 스타일 - Apple Gray */
    [data-testid="stSidebar"] {{
        background: #1c1c1e;
    }}
    
    /* 사이드바 텍스트 색상 */
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {{
        color: #F5F5F7;
        font-weight: 600;
        letter-spacing: -0.01em;
    }}
    
    [data-testid="stSidebar"] h2 {{
        font-size: 1.5rem;
        margin-bottom: 1.5rem;
    }}
    
    [data-testid="stSidebar"] h3 {{
        font-size: 1.2rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }}
    
    /* 버튼 스타일 - 둥근 사각형, 화이트 배경 */
    .stButton > button {{
        background: #FFFFFF;
        color: #000000;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.2s ease;
        letter-spacing: -0.01em;
    }}
    
    .stButton > button:hover {{
        background: #F5F5F7;
        transform: scale(1.02);
    }}
    
    .stButton > button:active {{
        transform: scale(0.98);
    }}
    
    /* 텍스트 입력창 - 테두리 없음, 짙은 회색 배경 */
    .stTextInput > div > div > input {{
        background-color: #2c2c2e;
        border: none;
        border-radius: 10px;
        color: #F5F5F7;
        padding: 0.75rem 1rem;
        font-size: 0.95rem;
        transition: all 0.2s ease;
        letter-spacing: -0.01em;
    }}
    
    .stTextInput > div > div > input:focus {{
        background-color: #3a3a3c;
        outline: none;
        box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1);
    }}
    
    .stTextInput > div > div > input::placeholder {{
        color: #86868B;
    }}
    
    /* 텍스트 영역 - 테두리 없음, 짙은 회색 배경 */
    .stTextArea > div > div > textarea {{
        background-color: #2c2c2e;
        border: none;
        border-radius: 10px;
        color: #F5F5F7;
        padding: 0.75rem 1rem;
        font-size: 0.95rem;
        transition: all 0.2s ease;
        letter-spacing: -0.01em;
    }}
    
    .stTextArea > div > div > textarea:focus {{
        background-color: #3a3a3c;
        outline: none;
        box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1);
    }}
    
    .stTextArea > div > div > textarea::placeholder {{
        color: #86868B;
    }}
    
    /* 채팅 메시지 컨테이너 */
    [data-testid="stChatMessage"] {{
        padding: 0;
        margin-bottom: 2rem;
    }}
    
    /* AI 메시지 - 투명 배경 */
    [data-testid="stChatMessage"][data-message-author="assistant"] > div:last-child {{
        background: transparent;
        border: none;
        padding: 1rem 0;
        color: #F5F5F7;
    }}
    
    /* 사용자 메시지 - 짙은 회색 배경 */
    [data-testid="stChatMessage"][data-message-author="user"] > div:last-child {{
        background: #3a3a3c;
        border: none;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        color: #F5F5F7;
    }}
    
    /* 채팅 메시지 텍스트 색상 */
    [data-testid="stChatMessage"] p {{
        color: #F5F5F7;
        line-height: 1.6;
        margin: 0;
        font-size: 0.95rem;
        letter-spacing: -0.01em;
    }}
    
    /* 채팅 입력창 - 테두리 없음, 짙은 회색 배경 */
    .stChatInput > div > div > textarea {{
        background-color: #2c2c2e !important;
        border: none !important;
        border-radius: 10px !important;
        color: #F5F5F7 !important;
        padding: 1rem 1.2rem !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
        letter-spacing: -0.01em !important;
    }}
    
    .stChatInput > div > div > textarea:focus {{
        background-color: #3a3a3c !important;
        outline: none !important;
        box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1) !important;
    }}
    
    .stChatInput > div > div > textarea::placeholder {{
        color: #86868B !important;
    }}
    
    /* 라벨 스타일 */
    label {{
        color: #F5F5F7 !important;
        font-weight: 500;
        font-size: 0.9rem;
        letter-spacing: -0.01em;
    }}
    
    /* 성공/에러 메시지 - 미니멀 스타일 */
    .stSuccess {{
        background: #2c2c2e;
        border: none;
        border-radius: 10px;
        padding: 1rem;
        color: #F5F5F7;
    }}
    
    .stError {{
        background: #2c2c2e;
        border: none;
        border-radius: 10px;
        padding: 1rem;
        color: #F5F5F7;
    }}
    
    /* 구분선 */
    hr {{
        border: none;
        height: 1px;
        background: #2c2c2e;
        margin: 2rem 0;
    }}
    
    /* 스크롤바 스타일 */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: #000000;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: #2c2c2e;
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: #3a3a3c;
    }}
</style>
""", unsafe_allow_html=True)

# --- 비밀번호 인증 체크 ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# 비밀번호 가져오기
try:
    app_password = st.secrets["APP_PASSWORD"]
except:
    app_password = None

# 인증되지 않은 경우 잠금 화면 표시
if not st.session_state.authenticated:
    # 잠금 화면 CSS 추가
    st.markdown("""
    <style>
        .lock-screen-container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 80vh;
            padding: 2rem;
        }
        .lock-message {
            color: #F5F5F7;
            font-size: 1.2rem;
            font-weight: 500;
            margin-bottom: 2rem;
            text-align: center;
            letter-spacing: -0.01em;
        }
        .lock-input-container {
            width: 100%;
            max-width: 400px;
            margin-bottom: 1rem;
        }
        .lock-button-container {
            width: 100%;
            max-width: 400px;
        }
        .error-message {
            color: #FF6B6B;
            font-size: 0.9rem;
            margin-top: 1rem;
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # 잠금 화면 UI
    st.markdown('<div class="lock-screen-container">', unsafe_allow_html=True)
    st.markdown('<div class="lock-message">🔒 접근 권한이 없습니다. 비밀번호를 입력하세요.</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password_input = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요", label_visibility="collapsed", key="lock_password")
        if st.button("확인", use_container_width=True, key="lock_submit"):
            if app_password and password_input == app_password:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.session_state.password_error = True
        
        if st.session_state.get("password_error", False):
            st.markdown('<div class="error-message">❌ 비밀번호가 일치하지 않습니다.</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 잠금 화면에서는 여기서 종료
    st.stop()

# --- 인증 성공 후 메인 화면 ---

# 로고 헤더 - 상단 중앙 배치
if logo_base64:
    st.markdown(f"""
    <div class="logo-header">
        <div class="logo-container">
            <img src="data:image/png;base64,{logo_base64}" alt="AlphA AI Logo">
        </div>
    </div>
    """, unsafe_allow_html=True)

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
        st.success("✅ OpenAI 자동 연결")
    else: 
        api_key = st.text_input("🔐 OpenAI Key", type="password", placeholder="sk-...")

    if secret_notion_key: 
        notion_key = secret_notion_key
        st.success("✅ Notion 자동 연결")
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
                        st.toast("✅ 저장 성공!", icon="🎉")
                    else: 
                        st.toast(f"❌ {msg}", icon="⚠️")
            else: 
                st.toast("❌ URL을 확인하세요", icon="⚠️")
        else:
            st.toast("⚠️ 키, URL, 내용을 확인하세요", icon="⚠️")

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
            st.toast(f"❌ {content}", icon="⚠️")

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
        st.toast("⚠️ API Key가 없습니다.", icon="⚠️")