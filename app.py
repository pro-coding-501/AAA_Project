import streamlit as st
import requests
import re
import json
import base64

# 1. 페이지 설정
st.set_page_config(
    page_title="AlphA AI • AAA", 
    page_icon=None, 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 로고 이미지 인코딩 함수
def get_logo_base64():
    try:
        with open("AlphA AI2 1.png", "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

logo_base64 = get_logo_base64()

# Premium Dark Theme CSS
st.markdown(f"""
<style>
    /* ============================================ */
    /* Premium AI Chat Interface Theme */
    /* ============================================ */
    
    /* 폰트 임포트 */
    @import url('https://rsms.me/inter/inter.css');
    
    /* Streamlit 기본 요소 숨기기 */
    footer {{visibility: hidden;}}
    #MainMenu {{visibility: hidden;}}
    
    /* 사이드바 토글 버튼 스타일 */
    button[kind="header"],
    button[title="View sidebar"],
    button[title="Close sidebar"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapseButton"] button,
    .stAppToolbar button,
    header button {{
        visibility: visible !important;
        display: block !important;
        opacity: 1 !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
    }}
    
    button[kind="header"]:hover,
    [data-testid="stSidebarCollapseButton"] button:hover {{
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
    }}
    
    /* ============================================ */
    /* 전체 배경 - Deep Near-Black */
    /* ============================================ */
    .stApp {{
        background: linear-gradient(180deg, #050505 0%, #0a0a0a 50%, #0f0f0f 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
        min-height: 100vh;
        letter-spacing: -0.01em;
        color: #E5E5E5;
    }}
    
    /* ============================================ */
    /* 상단 고정 헤더 */
    /* ============================================ */
    .app-header {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 64px;
        background: rgba(10, 10, 10, 0.8);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        padding: 0 2rem;
    }}
    
    .app-header-content {{
        max-width: 1200px;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
    }}
    
    .app-header-logo {{
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    
    .app-header-logo img {{
        width: 100%;
        height: 100%;
        object-fit: contain;
        filter: brightness(1.1);
    }}
    
    .app-header-title {{
        color: #FFFFFF;
        font-size: 1rem;
        font-weight: 500;
        letter-spacing: -0.02em;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    
    .app-header-title .separator {{
        color: rgba(255, 255, 255, 0.3);
        font-weight: 300;
    }}
    
    /* 메인 컨테이너 - 중앙 정렬, 최대 너비 65-70% */
    .main .block-container {{
        padding-top: 5rem;
        padding-bottom: 10rem;
        max-width: 65%;
        margin: 0 auto;
    }}
    
    @media (max-width: 1200px) {{
        .main .block-container {{
            max-width: 75%;
        }}
    }}
    
    @media (max-width: 768px) {{
        .main .block-container {{
            max-width: 95%;
            padding-top: 4rem;
        }}
    }}
    
    /* ============================================ */
    /* 사이드바 - Minimal Collapsible Panel */
    /* ============================================ */
    [data-testid="stSidebar"] {{
        background: rgba(15, 15, 15, 0.95);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 2px 0 32px rgba(0, 0, 0, 0.6);
    }}
    
    [data-testid="stSidebar"] > div:first-child {{
        background: transparent;
        padding-top: 1rem;
    }}
    
    /* 사이드바 제목 */
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {{
        color: #FFFFFF;
        font-weight: 600;
        letter-spacing: -0.02em;
        font-size: 0.95rem;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
        opacity: 0.9;
    }}
    
    [data-testid="stSidebar"] h3 {{
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        opacity: 0.7;
    }}
    
    /* ============================================ */
    /* 버튼 - Minimal & Subtle */
    /* ============================================ */
    .stButton > button {{
        background: rgba(255, 255, 255, 0.06);
        color: #FFFFFF;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 0.65rem 1.25rem;
        font-weight: 500;
        font-size: 0.875rem;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        letter-spacing: -0.01em;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }}
    
    .stButton > button:hover {{
        background: rgba(255, 255, 255, 0.1);
        border-color: rgba(255, 255, 255, 0.15);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }}
    
    .stButton > button:active {{
        transform: translateY(0);
    }}
    
    /* ============================================ */
    /* 입력창 - Subtle & Clean */
    /* ============================================ */
    .stTextInput > div > div > input {{
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        color: #FFFFFF;
        padding: 0.75rem 1rem;
        font-size: 0.875rem;
        transition: all 0.2s ease;
        letter-spacing: -0.01em;
    }}
    
    .stTextInput > div > div > input:focus {{
        background: rgba(255, 255, 255, 0.08);
        outline: none;
        border-color: rgba(255, 255, 255, 0.2);
        box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.05);
    }}
    
    .stTextInput > div > div > input::placeholder {{
        color: rgba(255, 255, 255, 0.4);
    }}
    
    /* 텍스트 영역 */
    .stTextArea > div > div > textarea {{
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        color: #FFFFFF;
        padding: 0.75rem 1rem;
        font-size: 0.875rem;
        transition: all 0.2s ease;
        letter-spacing: -0.01em;
    }}
    
    .stTextArea > div > div > textarea:focus {{
        background: rgba(255, 255, 255, 0.08);
        outline: none;
        border-color: rgba(255, 255, 255, 0.2);
        box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.05);
    }}
    
    .stTextArea > div > div > textarea::placeholder {{
        color: rgba(255, 255, 255, 0.4);
    }}
    
    /* ============================================ */
    /* 채팅 메시지 - Premium Card Style */
    /* ============================================ */
    [data-testid="stChatMessage"] {{
        padding: 0;
        margin-bottom: 1.25rem;
        background: transparent;
        width: 100%;
        display: flex;
        animation: messageSlideIn 0.3s ease-out;
    }}
    
    @keyframes messageSlideIn {{
        from {{
            opacity: 0;
            transform: translateY(10px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    /* AI 메시지 - 왼쪽 정렬 */
    [data-testid="stChatMessage"][data-message-author="assistant"] {{
        justify-content: flex-start;
    }}
    
    /* 사용자 메시지 - 오른쪽 정렬 */
    [data-testid="stChatMessage"][data-message-author="user"] {{
        justify-content: flex-end;
    }}
    
    /* 채팅 메시지 내부 컨테이너 */
    [data-testid="stChatMessage"] > div {{
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        max-width: 85%;
    }}
    
    /* AI 메시지 내부 컨테이너 - 왼쪽 정렬 */
    [data-testid="stChatMessage"][data-message-author="assistant"] > div {{
        justify-content: flex-start;
    }}
    
    /* 사용자 메시지 내부 컨테이너 - 오른쪽 정렬, 아바타와 메시지 순서 반전 */
    [data-testid="stChatMessage"][data-message-author="user"] > div {{
        justify-content: flex-end;
        flex-direction: row-reverse;
    }}
    
    /* 아바타 이미지 스타일 */
    [data-testid="stChatMessage"] img {{
        border-radius: 50%;
        border: 1px solid rgba(255, 255, 255, 0.1);
        width: 36px;
        height: 36px;
        object-fit: cover;
        flex-shrink: 0;
    }}
    
    /* AI 아바타 특별 효과 */
    [data-testid="stChatMessage"][data-message-author="assistant"] img {{
        background: rgba(255, 255, 255, 0.03);
        padding: 2px;
    }}
    
    /* AI 메시지 말풍선 */
    [data-testid="stChatMessage"][data-message-author="assistant"] > div:last-child {{
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1rem 1.25rem;
        color: #E5E5E5;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.2);
    }}
    
    /* 사용자 메시지 말풍선 */
    [data-testid="stChatMessage"][data-message-author="user"] > div:last-child {{
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 1rem 1.25rem;
        color: #FFFFFF;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.25);
    }}
    
    /* 채팅 메시지 텍스트 */
    [data-testid="stChatMessage"] p {{
        color: inherit;
        line-height: 1.7;
        margin: 0;
        font-size: 0.95rem;
        letter-spacing: -0.01em;
    }}
    
    /* 채팅 메시지 내부 모든 텍스트 요소 */
    [data-testid="stChatMessage"] * {{
        font-size: 0.95rem !important;
    }}
    
    [data-testid="stChatMessage"] h1,
    [data-testid="stChatMessage"] h2,
    [data-testid="stChatMessage"] h3,
    [data-testid="stChatMessage"] h4 {{
        font-size: inherit !important;
    }}
    
    /* ============================================ */
    /* 채팅 입력창 - Floating Capsule Style */
    /* ============================================ */
    .stChatInput {{
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 1.25rem 2rem;
        background: rgba(10, 10, 10, 0.9);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 -4px 32px rgba(0, 0, 0, 0.6);
        z-index: 999;
    }}
    
    .stChatInput > div {{
        max-width: 65%;
        margin: 0 auto;
    }}
    
    @media (max-width: 1200px) {{
        .stChatInput > div {{
            max-width: 75%;
        }}
    }}
    
    @media (max-width: 768px) {{
        .stChatInput > div {{
            max-width: 95%;
        }}
        .stChatInput {{
            padding: 1rem 1rem;
        }}
    }}
    
    .stChatInput > div > div > textarea {{
        background: rgba(255, 255, 255, 0.06) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 24px !important;
        color: #FFFFFF !important;
        padding: 1rem 1.5rem !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
        letter-spacing: -0.01em !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        box-shadow: 0 2px 16px rgba(0, 0, 0, 0.3) !important;
        min-height: 56px !important;
        resize: none !important;
    }}
    
    .stChatInput > div > div > textarea:focus {{
        background: rgba(255, 255, 255, 0.08) !important;
        outline: none !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
        box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.05), 0 4px 24px rgba(0, 0, 0, 0.4) !important;
    }}
    
    .stChatInput > div > div > textarea::placeholder {{
        color: rgba(255, 255, 255, 0.4) !important;
    }}
    
    /* ============================================ */
    /* 라벨 및 기타 요소 */
    /* ============================================ */
    label {{
        color: rgba(255, 255, 255, 0.7) !important;
        font-weight: 500;
        font-size: 0.8rem;
        letter-spacing: -0.01em;
        opacity: 0.8;
    }}
    
    /* 성공 메시지 */
    .stSuccess {{
        background: rgba(52, 199, 89, 0.12);
        border: 1px solid rgba(52, 199, 89, 0.25);
        border-radius: 10px;
        padding: 0.875rem;
        color: #34C759;
    }}
    
    /* 에러 메시지 */
    .stError {{
        background: rgba(255, 59, 48, 0.12);
        border: 1px solid rgba(255, 59, 48, 0.25);
        border-radius: 10px;
        padding: 0.875rem;
        color: #FF3B30;
    }}
    
    /* 구분선 */
    hr {{
        border: none;
        height: 1px;
        background: rgba(255, 255, 255, 0.08);
        margin: 1.5rem 0;
    }}
    
    /* ============================================ */
    /* 스크롤바 - Minimal */
    /* ============================================ */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: transparent;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: rgba(255, 255, 255, 0.15);
    }}
    
    /* ============================================ */
    /* 타이핑 인디케이터 */
    /* ============================================ */
    .typing-indicator {{
        display: inline-flex;
        gap: 4px;
        padding: 0.5rem 0;
    }}
    
    .typing-indicator span {{
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.4);
        animation: typingDot 1.4s infinite;
    }}
    
    .typing-indicator span:nth-child(2) {{
        animation-delay: 0.2s;
    }}
    
    .typing-indicator span:nth-child(3) {{
        animation-delay: 0.4s;
    }}
    
    @keyframes typingDot {{
        0%, 60%, 100% {{
            transform: translateY(0);
            opacity: 0.4;
        }}
        30% {{
            transform: translateY(-8px);
            opacity: 1;
        }}
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
    # 잠금 화면 CSS 추가 - Premium Style
    st.markdown("""
    <style>
        .stApp {
            overflow: hidden !important;
        }
        .main .block-container {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            max-width: 100% !important;
        }
        .lock-screen-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            width: 100vw;
            position: fixed;
            top: 0;
            left: 0;
            padding: 2rem;
            box-sizing: border-box;
        }
        .lock-card {
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(30px);
            -webkit-backdrop-filter: blur(30px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 3rem 2.5rem;
            width: 100%;
            max-width: 420px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.7);
            text-align: center;
            margin: 0 auto;
        }
        .lock-title {
            color: #FFFFFF;
            font-size: 1.75rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
            letter-spacing: -0.02em;
        }
        .lock-subtitle {
            color: rgba(255, 255, 255, 0.6);
            font-size: 0.9rem;
            margin-bottom: 2rem;
            letter-spacing: -0.01em;
        }
        .lock-input-wrapper {
            margin-bottom: 1.5rem;
        }
        .error-message {
            background: rgba(255, 59, 48, 0.12);
            border: 1px solid rgba(255, 59, 48, 0.25);
            border-radius: 10px;
            color: #FF3B30;
            padding: 0.875rem;
            margin-top: 1rem;
            font-size: 0.875rem;
            animation: shake 0.4s;
        }
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-8px); }
            75% { transform: translateX(8px); }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # 잠금 화면 UI
    st.markdown('<div class="lock-screen-wrapper">', unsafe_allow_html=True)
    st.markdown('''
    <div class="lock-card">
        <div class="lock-title">AlphA AI</div>
        <div class="lock-subtitle">접근하려면 비밀번호를 입력하세요</div>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 입력창과 버튼은 중앙 정렬
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password_input = st.text_input(
            "비밀번호", 
            type="password", 
            placeholder="••••••••", 
            label_visibility="collapsed", 
            key="lock_password"
        )
        if st.button("잠금 해제", use_container_width=True, key="lock_submit"):
            if app_password and password_input == app_password:
                st.session_state.authenticated = True
                st.session_state.password_error = False
                st.rerun()
            else:
                st.session_state.password_error = True
        
        if st.session_state.get("password_error", False):
            st.markdown('<div class="error-message">비밀번호가 일치하지 않습니다</div>', unsafe_allow_html=True)
    
    # 잠금 화면에서는 여기서 종료
    st.stop()

# --- 인증 성공 후 메인 화면 ---

# 상단 고정 헤더
if logo_base64:
    st.markdown(f"""
    <div class="app-header">
        <div class="app-header-content">
            <div class="app-header-logo">
                <img src="data:image/png;base64,{logo_base64}" alt="AlphA AI Logo">
            </div>
            <div class="app-header-title">
                <span>AlphA AI</span>
                <span class="separator">·</span>
                <span style="opacity: 0.7;">AAA</span>
            </div>
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
    
    # [쓰기 기능 UI] - 추가됨!
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
            st.toast("데이터 로드 완료!")
        else: 
            st.toast(f"오류: {content}")

# 채팅 화면
for msg in st.session_state.messages:
    if msg["role"] == "user":
        avatar = None
    else:
        # AI는 로고 이미지 사용
        avatar = f"data:image/png;base64,{logo_base64}" if logo_base64 else None
    
    with st.chat_message(msg["role"], avatar=avatar): 
        st.markdown(msg["content"])

if prompt := st.chat_input("메시지를 입력하세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 사용자 메시지 표시
    with st.chat_message("user", avatar=None): 
        st.markdown(prompt)

    if api_key:
        sys_msg = f"너는 AlphA Inc. 비서 AAA야. 참고 데이터:\n{st.session_state.notion_context}"
        msgs = [{"role": "system", "content": sys_msg}] + st.session_state.messages
        
        # AI 응답 (로고 아바타)
        ai_avatar = f"data:image/png;base64,{logo_base64}" if logo_base64 else None
        with st.chat_message("assistant", avatar=ai_avatar):
            stream = call_openai_stream(api_key, msgs)
            resp = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": resp})
    else:
        st.toast("API Key가 없습니다.")