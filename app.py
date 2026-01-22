import streamlit as st
import requests
import re
import json
import base64

# 페이지 설정
st.set_page_config(
    page_title="AlphA AI • AAA", 
    page_icon=None, 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 파일 로드
def load_css():
    try:
        with open("style.css", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""

# CSS 적용
css_content = load_css()
if css_content:
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

# 로고 이미지 인코딩 함수
def get_logo_base64():
    try:
        with open("AlphA AI2 1.png", "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

logo_base64 = get_logo_base64()

# Streamlit 기본 요소 숨기기
st.markdown("""
<style>
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    header[data-testid="stHeader"] {display: none;}
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
    # 잠금 화면 HTML 구조
    st.markdown('<div class="lock-screen-container">', unsafe_allow_html=True)
    
    logo_html = ''
    if logo_base64:
        logo_html = f'<div class="lock-logo"><img src="data:image/png;base64,{logo_base64}" alt="AlphA AI"></div>'
    
    st.markdown(f'''
    <div class="lock-card">
        {logo_html}
        <div class="lock-title">AlphA AI</div>
        <div class="lock-subtitle">접근하려면 비밀번호를 입력하세요</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Form을 사용하여 Enter 키 지원
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form(key="login_form", clear_on_submit=False):
            password_input = st.text_input(
                "비밀번호", 
                type="password", 
                placeholder="••••••••", 
                label_visibility="collapsed", 
                key="lock_password"
            )
            submit_button = st.form_submit_button("잠금 해제", use_container_width=True)
            
            if submit_button:
                if app_password and password_input == app_password:
                    st.session_state.authenticated = True
                    st.session_state.password_error = False
                    st.rerun()
                else:
                    st.session_state.password_error = True
        
        if st.session_state.get("password_error", False):
            st.markdown('<div class="error-message">⚠️ 비밀번호가 일치하지 않습니다</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- 인증 성공 후 메인 화면 ---

# 상단 고정 헤더
if logo_base64:
    st.markdown(f"""
    <div class="app-header">
        <div class="app-header-content">
            <div class="app-header-left">
                <div class="app-header-logo">
                    <img src="data:image/png;base64,{logo_base64}" alt="AlphA AI Logo">
                </div>
                <div class="app-header-title">
                    <span>AlphA AI</span>
                    <span class="separator">·</span>
                    <span class="subtitle">AAA</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 비밀 금고(Secrets)에서 키 가져오기 ---
try: 
    secret_api_key = st.secrets["OPENAI_API_KEY"]
except: 
    secret_api_key = ""

try: 
    secret_notion_key = st.secrets["NOTION_KEY"]
except: 
    secret_notion_key = ""

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
        if response.status_code != 200: 
            raise Exception(f"HTTP {response.status_code}: {response.text}")
        for line in response.iter_lines():
            if line:
                line_text = line.decode('utf-8')
                if line_text.startswith("data: "):
                    data_str = line_text[6:]
                    if data_str == "[DONE]": 
                        break
                    try:
                        data = json.loads(data_str)
                        content = data["choices"][0]["delta"].get("content", "")
                        if content: 
                            yield content
                    except: 
                        continue
    except Exception as e:
        yield f"에러: {str(e)}"

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
                    if prop["type"] == "title" and prop.get("title"): 
                        val = prop["title"][0].get("plain_text", "")
                    elif prop["type"] == "rich_text" and prop.get("rich_text"): 
                        val = prop["rich_text"][0].get("plain_text", "")
                    elif prop["type"] == "select": 
                        val = prop.get("select", {}).get("name", "")
                    elif prop["type"] == "status": 
                        val = prop.get("status", {}).get("name", "")
                    if val: 
                        row_text.append(f"{name}: {val}")
                content += " | ".join(row_text) + "\n"
            return content
    except: 
        pass
    # 2. 페이지 시도
    res = requests.get(f"https://api.notion.com/v1/blocks/{page_id}/children", headers=headers)
    if res.status_code == 200:
        content = "=== [노션 페이지] ===\n"
        for block in res.json().get("results", []):
            type_ = block.get("type")
            if type_ in block and "rich_text" in block[type_]:
                text_content = ""
                for t in block[type_]["rich_text"]: 
                    text_content += t.get("plain_text", "")
                if text_content: 
                    content += f"- {text_content}\n"
        return content if len(content) > 10 else "내용 없음"
    return "읽기 실패"

# [쓰기 함수]
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
        if response.status_code == 200: 
            return True, "저장 성공!"
        else: 
            return False, f"실패: {response.status_code}"
    except Exception as e: 
        return False, str(e)

# HTML 이스케이프 함수
def escape_html(text):
    if not text:
        return ""
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&#x27;"))

# 마크다운을 HTML로 변환 (간단한 버전)
def markdown_to_html(text):
    if not text:
        return ""
    # 줄바꿈 처리
    html = escape_html(text)
    html = html.replace("\n", "<br>")
    # 간단한 마크다운 처리
    import re
    # **bold**
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    # *italic*
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    # `code`
    html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
    return html

# 메시지를 HTML로 렌더링하는 함수
def render_message_html(role, content, index, logo_base64=None):
    is_user = role == "user"
    avatar_html = ""
    
    if not is_user and logo_base64:
        avatar_html = f'<div class="message-avatar"><img src="data:image/png;base64,{logo_base64}" alt="AI"></div>'
    
    content_html = markdown_to_html(content)
    
    message_class = "message user-message" if is_user else "message ai-message"
    bubble_class = "message-bubble user-bubble" if is_user else "message-bubble ai-bubble"
    
    if is_user:
        return f'''
        <div class="{message_class}" style="animation-delay: {index * 0.05}s;">
            <div class="{bubble_class}">
                <div class="message-content">{content_html}</div>
            </div>
        </div>
        '''
    else:
        return f'''
        <div class="{message_class}" style="animation-delay: {index * 0.05}s;">
            {avatar_html}
            <div class="{bubble_class}">
                <div class="message-content">{content_html}</div>
            </div>
        </div>
        '''

# --- 사이드바 UI ---
with st.sidebar:
    st.markdown("### 설정")
    if secret_api_key: 
        api_key = secret_api_key
        st.success("OpenAI 자동 연결")
    else: 
        api_key = st.text_input("OpenAI Key", type="password", placeholder="sk-...")

    if secret_notion_key: 
        notion_key = secret_notion_key
        st.success("Notion 자동 연결")
    else: 
        notion_key = st.text_input("Notion Key", type="password", placeholder="secret_...")

    # 페이지 URL은 항상 입력 가능
    page_url = st.text_input("Notion Page URL", placeholder="https://notion.so/...")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("읽어오기", use_container_width=True): 
            st.session_state["fetch_notion"] = True
    
    st.markdown("---")
    
    # [쓰기 기능 UI]
    st.markdown("### 메모 남기기")
    memo_text = st.text_area("내용을 입력하세요", height=100, placeholder="여기에 메모를 작성하세요...")
    if st.button("노션에 저장", use_container_width=True):
        if notion_key and page_url and memo_text:
            pid = extract_page_id(page_url)
            if pid:
                with st.spinner("저장 중..."):
                    success, msg = write_to_notion(notion_key, pid, memo_text)
                    if success: 
                        st.toast("저장 성공!")
                    else: 
                        st.toast(f"오류: {msg}")
            else: 
                st.toast("URL을 확인하세요")
        else:
            st.toast("키, URL, 내용을 확인하세요")

# --- 메인 로직 ---
if "messages" not in st.session_state: 
    st.session_state.messages = []
if "notion_context" not in st.session_state: 
    st.session_state.notion_context = ""

# 읽기 실행
if st.session_state.get("fetch_notion") and notion_key and page_url:
    pid = extract_page_id(page_url)
    if pid:
        with st.spinner("분석 중..."):
            content = get_notion_data(notion_key, pid)
            st.session_state.notion_context = content
        if "실패" not in content: 
            st.toast("데이터 로드 완료!")
        else: 
            st.toast(f"오류: {content}")

# 채팅 컨테이너 시작
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
st.markdown('<div class="messages-wrapper">', unsafe_allow_html=True)

# 기존 메시지들 렌더링 (st.chat_message 사용 안 함)
for idx, msg in enumerate(st.session_state.messages):
    message_html = render_message_html(msg["role"], msg["content"], idx, logo_base64)
    st.markdown(message_html, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 입력창 (st.chat_input 사용, CSS로 스타일링)
if prompt := st.chat_input("메시지를 입력하세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 사용자 메시지 즉시 표시
    user_message_html = render_message_html("user", prompt, len(st.session_state.messages) - 1)
    st.markdown(user_message_html, unsafe_allow_html=True)

    if api_key:
        sys_msg = f"너는 AlphA Inc. 비서 AAA야. 참고 데이터:\n{st.session_state.notion_context}"
        msgs = [{"role": "system", "content": sys_msg}] + st.session_state.messages
        
        # AI 응답 스트리밍
        stream = call_openai_stream(api_key, msgs)
        
        # 스트리밍 응답을 위한 플레이스홀더
        response_placeholder = st.empty()
        full_response = ""
        
        # 스트리밍 중 메시지 업데이트
        for chunk in stream:
            full_response += chunk
            ai_message_html = render_message_html("assistant", full_response, len(st.session_state.messages))
            response_placeholder.markdown(ai_message_html, unsafe_allow_html=True)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    else:
        st.toast("API Key가 없습니다.")
