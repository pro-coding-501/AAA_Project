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
    initial_sidebar_state="expanded"
)

# 로고 이미지 인코딩 함수
def get_logo_base64():
    try:
        with open("AlphA AI2 1.png", "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

logo_base64 = get_logo_base64()

# Midnight Silver & Glass 테마 CSS
st.markdown(f"""
<style>
    /* ============================================ */
    /* Midnight Silver & Glass Theme */
    /* ============================================ */
    
    /* 폰트 임포트 */
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    @import url('https://rsms.me/inter/inter.css');
    
    /* Streamlit 기본 요소 숨기기 */
    footer {{visibility: hidden;}}
    
    /* 헤더는 보이게 하되 메뉴만 숨기기 */
    header {{visibility: visible;}}
    header .stAppToolbar {{
        visibility: visible;
    }}
    
    /* 메뉴는 숨기되 사이드바 토글 버튼은 보이게 */
    #MainMenu {{
        visibility: hidden;
    }}
    
    /* 사이드바 토글 버튼 - 모든 가능한 선택자 */
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
    }}
    
    /* 사이드바가 닫혔을 때도 토글 버튼 보이게 */
    section[data-testid="stSidebar"] ~ div button[kind="header"],
    .stApp header button {{
        visibility: visible !important;
        display: block !important;
    }}
    
    /* ============================================ */
    /* 전체 배경 - Midnight Deep Gray */
    /* ============================================ */
    .stApp {{
        background: linear-gradient(180deg, #0a0a0a 0%, #121212 100%);
        font-family: 'Pretendard', 'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
        min-height: 100vh;
        letter-spacing: -0.02em;
        color: #E8E8E8;
    }}
    
    /* 메인 컨테이너 */
    .main .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 8rem;
        max-width: 1400px;
        margin: 0 auto;
    }}
    
    /* ============================================ */
    /* 로고 헤더 - Glass Effect */
    /* ============================================ */
    .logo-header {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 2.5rem;
        margin-top: 1rem;
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }}
    
    .logo-container {{
        width: 100px;
        height: 100px;
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
    }}
    
    .logo-container img {{
        width: 100%;
        height: 100%;
        object-fit: contain;
        filter: drop-shadow(0 4px 16px rgba(255, 255, 255, 0.1));
    }}
    
    /* ============================================ */
    /* 사이드바 - Metallic Silver Glass */
    /* ============================================ */
    [data-testid="stSidebar"] {{
        background: rgba(18, 18, 18, 0.95);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.5);
    }}
    
    [data-testid="stSidebar"] > div:first-child {{
        background: transparent;
    }}
    
    /* 사이드바 제목 */
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {{
        color: #FFFFFF;
        font-weight: 600;
        letter-spacing: -0.03em;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
    }}
    
    [data-testid="stSidebar"] h3 {{
        font-size: 1.1rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        padding-left: 0.5rem;
        border-left: 3px solid rgba(255, 255, 255, 0.3);
    }}
    
    /* ============================================ */
    /* 버튼 - Silver Metallic */
    /* ============================================ */
    .stButton > button {{
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.05) 100%);
        color: #FFFFFF;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        letter-spacing: -0.01em;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }}
    
    .stButton > button:hover {{
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.15) 100%);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
    }}
    
    .stButton > button:active {{
        transform: translateY(0);
    }}
    
    /* ============================================ */
    /* 입력창 - Glass Morphism */
    /* ============================================ */
    .stTextInput > div > div > input {{
        background: rgba(44, 44, 46, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        color: #FFFFFF;
        padding: 0.85rem 1.1rem;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        letter-spacing: -0.01em;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }}
    
    .stTextInput > div > div > input:focus {{
        background: rgba(44, 44, 46, 0.8);
        outline: none;
        border: 1px solid rgba(255, 255, 255, 0.25);
        box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.05), 0 8px 24px rgba(0, 0, 0, 0.3);
    }}
    
    .stTextInput > div > div > input::placeholder {{
        color: #6E6E73;
    }}
    
    /* 텍스트 영역 */
    .stTextArea > div > div > textarea {{
        background: rgba(44, 44, 46, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        color: #FFFFFF;
        padding: 0.85rem 1.1rem;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        letter-spacing: -0.01em;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }}
    
    .stTextArea > div > div > textarea:focus {{
        background: rgba(44, 44, 46, 0.8);
        outline: none;
        border: 1px solid rgba(255, 255, 255, 0.25);
        box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.05), 0 8px 24px rgba(0, 0, 0, 0.3);
    }}
    
    .stTextArea > div > div > textarea::placeholder {{
        color: #6E6E73;
    }}
    
    /* ============================================ */
    /* 채팅 메시지 - Midnight Silver Style */
    /* ============================================ */
    [data-testid="stChatMessage"] {{
        padding: 0;
        margin-bottom: 1.5rem;
        background: transparent;
        width: 100%;
        display: flex;
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
        gap: 1rem;
        max-width: 75%;
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
        border: 2px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        width: 40px;
        height: 40px;
        object-fit: cover;
        flex-shrink: 0;
    }}
    
    /* AI 아바타 특별 효과 */
    [data-testid="stChatMessage"][data-message-author="assistant"] img {{
        background: rgba(255, 255, 255, 0.05);
        padding: 4px;
        filter: drop-shadow(0 2px 8px rgba(255, 255, 255, 0.15));
    }}
    
    /* AI 메시지 말풍선 */
    [data-testid="stChatMessage"][data-message-author="assistant"] > div:last-child {{
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid #333333;
        border-radius: 18px;
        padding: 1.2rem 1.5rem;
        color: #E8E8E8;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }}
    
    /* 사용자 메시지 말풍선 */
    [data-testid="stChatMessage"][data-message-author="user"] > div:last-child {{
        background: linear-gradient(135deg, #2C2C2E 0%, #1C1C1E 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 1.2rem 1.5rem;
        color: #FFFFFF;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
    }}
    
    /* 채팅 메시지 텍스트 */
    [data-testid="stChatMessage"] p {{
        color: inherit;
        line-height: 1.8;
        margin: 0;
        font-size: 1.1rem;
        letter-spacing: -0.01em;
    }}
    
    /* 채팅 메시지 내부 모든 텍스트 요소 */
    [data-testid="stChatMessage"] * {{
        font-size: 1.1rem !important;
    }}
    
    /* ============================================ */
    /* 채팅 입력창 - Glass Fixed Bottom */
    /* ============================================ */
    .stChatInput {{
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 1.5rem 2rem;
        background: rgba(18, 18, 18, 0.85);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 -4px 24px rgba(0, 0, 0, 0.5);
        z-index: 999;
    }}
    
    .stChatInput > div {{
        max-width: 1400px;
        margin: 0 auto;
    }}
    
    .stChatInput > div > div > textarea {{
        background: rgba(44, 44, 46, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 16px !important;
        color: #FFFFFF !important;
        padding: 1.2rem 1.5rem !important;
        font-size: 1.05rem !important;
        transition: all 0.3s ease !important;
        letter-spacing: -0.01em !important;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) !important;
        min-height: 60px !important;
    }}
    
    .stChatInput > div > div > textarea:focus {{
        background: rgba(44, 44, 46, 0.9) !important;
        outline: none !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.08), 0 8px 32px rgba(0, 0, 0, 0.5) !important;
    }}
    
    .stChatInput > div > div > textarea::placeholder {{
        color: #6E6E73 !important;
    }}
    
    /* ============================================ */
    /* 정보 카드 위젯 - Glass Card */
    /* ============================================ */
    .info-card {{
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }}
    
    .info-card:hover {{
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.5);
        transform: translateY(-2px);
    }}
    
    .info-card h4 {{
        color: #FFFFFF;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        letter-spacing: -0.02em;
    }}
    
    .info-card p {{
        color: #B8B8B8;
        font-size: 0.9rem;
        line-height: 1.6;
        margin: 0;
    }}
    
    /* ============================================ */
    /* 라벨 및 기타 요소 */
    /* ============================================ */
    label {{
        color: #E8E8E8 !important;
        font-weight: 500;
        font-size: 0.85rem;
        letter-spacing: -0.01em;
        text-transform: uppercase;
        opacity: 0.8;
    }}
    
    /* 성공 메시지 */
    .stSuccess {{
        background: rgba(52, 199, 89, 0.15);
        border: 1px solid rgba(52, 199, 89, 0.3);
        border-radius: 12px;
        padding: 1rem;
        color: #34C759;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }}
    
    /* 에러 메시지 */
    .stError {{
        background: rgba(255, 59, 48, 0.15);
        border: 1px solid rgba(255, 59, 48, 0.3);
        border-radius: 12px;
        padding: 1rem;
        color: #FF3B30;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }}
    
    /* 구분선 */
    hr {{
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, rgba(255, 255, 255, 0.1) 50%, transparent 100%);
        margin: 2rem 0;
    }}
    
    /* ============================================ */
    /* 스크롤바 - Minimal Silver */
    /* ============================================ */
    ::-webkit-scrollbar {{
        width: 10px;
        height: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: #0a0a0a;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.08) 100%);
        border-radius: 5px;
        border: 2px solid #0a0a0a;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.15) 100%);
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
    # 잠금 화면 CSS 추가 - Midnight Silver & Glass
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
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(30px);
            -webkit-backdrop-filter: blur(30px);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 24px;
            padding: 3rem 2.5rem;
            width: 100%;
            max-width: 480px;
            box-shadow: 0 16px 64px rgba(0, 0, 0, 0.6);
            text-align: center;
            margin: 0 auto;
        }
        .lock-title {
            color: #FFFFFF;
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 0.8rem;
            letter-spacing: -0.03em;
            text-shadow: 0 2px 12px rgba(0, 0, 0, 0.5);
        }
        .lock-subtitle {
            color: #B8B8B8;
            font-size: 0.95rem;
            margin-bottom: 2.5rem;
            letter-spacing: -0.01em;
        }
        .lock-input-wrapper {
            margin-bottom: 1.5rem;
        }
        .error-message {
            background: rgba(255, 59, 48, 0.15);
            border: 1px solid rgba(255, 59, 48, 0.3);
            border-radius: 12px;
            color: #FF3B30;
            padding: 0.9rem;
            margin-top: 1.2rem;
            font-size: 0.9rem;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
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