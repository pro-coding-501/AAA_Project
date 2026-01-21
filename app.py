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

# 커스텀 CSS - Dark Tech 스타일 (완전 재설계)
st.markdown(f"""
<style>
    /* 웹폰트 로드 */
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css');
    
    /* Streamlit 기본 푸터만 숨기기 (사이드바 메뉴는 유지) */
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* 사이드바 토글 버튼 스타일 개선 */
    [data-testid="stSidebar"] [data-testid="collapsedControl"] {{
        background: rgba(102, 126, 234, 0.2);
        border: 1px solid rgba(102, 126, 234, 0.4);
        border-radius: 8px;
        transition: all 0.3s ease;
    }}
    
    [data-testid="stSidebar"] [data-testid="collapsedControl"]:hover {{
        background: rgba(102, 126, 234, 0.3);
        box-shadow: 0 0 15px rgba(102, 126, 234, 0.5);
    }}
    
    /* 전체 배경 - 회로 기판 패턴 + 깊이 있는 다크 그라데이션 */
    .stApp {{
        background: 
            /* 회로 기판 패턴 (SVG) */
            url("data:image/svg+xml,%3Csvg width='100' height='100' xmlns='http://www.w3.org/2000/svg'%3E%3Cdefs%3E%3Cpattern id='circuit' x='0' y='0' width='100' height='100' patternUnits='userSpaceOnUse'%3E%3Cpath d='M0 50h100M50 0v100' stroke='rgba(102,126,234,0.05)' stroke-width='0.5'/%3E%3Ccircle cx='25' cy='25' r='1' fill='rgba(102,126,234,0.1)'/%3E%3Ccircle cx='75' cy='75' r='1' fill='rgba(118,75,162,0.1)'/%3E%3C/pattern%3E%3C/defs%3E%3Crect width='100' height='100' fill='url(%23circuit)'/%3E%3C/svg%3E"),
            /* 그라데이션 레이어 */
            radial-gradient(circle at 20% 30%, rgba(102, 126, 234, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(118, 75, 162, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(240, 147, 251, 0.08) 0%, transparent 70%),
            linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 25%, #16213e 50%, #0f1419 75%, #0a0a0f 100%);
        background-attachment: fixed;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Noto Sans KR', sans-serif;
        min-height: 100vh;
    }}
    
    /* 메인 컨테이너 스타일 */
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }}
    
    /* 로고 및 타이틀 컨테이너 */
    .brand-header {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1.5rem;
        margin-bottom: 3rem;
        margin-top: 1rem;
        padding: 2rem 0;
        position: relative;
    }}
    
    .brand-header::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 400px;
        height: 200px;
        background: radial-gradient(ellipse, rgba(102, 126, 234, 0.2) 0%, transparent 70%);
        filter: blur(60px);
        z-index: -1;
        animation: pulse 3s ease-in-out infinite;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ opacity: 0.6; }}
        50% {{ opacity: 1; }}
    }}
    
    .logo-container {{
        width: 80px;
        height: 80px;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 
            0 8px 32px rgba(102, 126, 234, 0.4),
            0 0 40px rgba(102, 126, 234, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        border: 2px solid rgba(102, 126, 234, 0.5);
        position: relative;
        animation: glow 2s ease-in-out infinite alternate;
    }}
    
    @keyframes glow {{
        from {{
            box-shadow: 
                0 8px 32px rgba(102, 126, 234, 0.4),
                0 0 40px rgba(102, 126, 234, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.2);
        }}
        to {{
            box-shadow: 
                0 8px 32px rgba(102, 126, 234, 0.6),
                0 0 60px rgba(102, 126, 234, 0.5),
                inset 0 1px 0 rgba(255, 255, 255, 0.3);
        }}
    }}
    
    .logo-container img {{
        width: 100%;
        height: 100%;
        object-fit: contain;
        filter: drop-shadow(0 0 10px rgba(102, 126, 234, 0.5));
    }}
    
    .brand-title {{
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.03em;
        text-shadow: 0 0 30px rgba(102, 126, 234, 0.5);
        position: relative;
    }}
    
    .brand-title::after {{
        content: '';
        position: absolute;
        top: 50%;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.5), transparent);
        transform: translateY(50px);
    }}
    
    /* 사이드바 스타일 - 깊이감 있는 배경 + 테크 느낌 */
    [data-testid="stSidebar"] {{
        background: 
            linear-gradient(180deg, rgba(10, 14, 39, 0.98) 0%, rgba(15, 20, 45, 0.98) 100%),
            url("data:image/svg+xml,%3Csvg width='60' height='60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 30h60M30 0v60' stroke='rgba(102,126,234,0.08)' stroke-width='1'/%3E%3C/svg%3E");
        border-right: 2px solid rgba(102, 126, 234, 0.4);
        box-shadow: 4px 0 30px rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(10px);
    }}
    
    /* 사이드바 헤더 스타일 */
    [data-testid="stSidebar"] h2 {{
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(102, 126, 234, 0.3);
        letter-spacing: -0.01em;
    }}
    
    [data-testid="stSidebar"] h3 {{
        font-size: 1.4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #764ba2 0%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(118, 75, 162, 0.3);
    }}
    
    /* 버튼 스타일 - 강화된 Glow 효과 */
    .stButton > button {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 16px;
        padding: 0.7rem 1.8rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 
            0 4px 15px rgba(102, 126, 234, 0.4),
            0 0 20px rgba(102, 126, 234, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
    }}
    
    .stButton > button::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-3px) scale(1.02);
        box-shadow: 
            0 8px 25px rgba(102, 126, 234, 0.6),
            0 0 40px rgba(102, 126, 234, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 50%, #f093fb 100%);
    }}
    
    .stButton > button:hover::before {{
        left: 100%;
    }}
    
    .stButton > button:active {{
        transform: translateY(-1px) scale(0.98);
    }}
    
    /* 텍스트 입력창 스타일 - Underline 스타일 */
    .stTextInput > div > div > input {{
        background-color: rgba(255, 255, 255, 0.03);
        border: none;
        border-bottom: 2px solid rgba(102, 126, 234, 0.4);
        border-radius: 0;
        color: #ffffff;
        padding: 0.8rem 0.5rem;
        transition: all 0.3s ease;
        font-size: 0.95rem;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-bottom-color: #667eea;
        background-color: rgba(255, 255, 255, 0.05);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        outline: none;
    }}
    
    .stTextInput > div > div > input::placeholder {{
        color: rgba(255, 255, 255, 0.3);
    }}
    
    /* 텍스트 영역 스타일 - 빛나는 테두리 */
    .stTextArea > div > div > textarea {{
        background-color: rgba(255, 255, 255, 0.03);
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 12px;
        color: #ffffff;
        padding: 1rem;
        transition: all 0.3s ease;
        font-size: 0.95rem;
    }}
    
    .stTextArea > div > div > textarea:focus {{
        border-color: #667eea;
        box-shadow: 
            0 0 0 3px rgba(102, 126, 234, 0.2),
            0 0 20px rgba(102, 126, 234, 0.3);
        background-color: rgba(255, 255, 255, 0.05);
        outline: none;
    }}
    
    /* 채팅 메시지 컨테이너 - 간격 넓히기 */
    [data-testid="stChatMessage"] {{
        padding: 0;
        margin-bottom: 2.5rem;
    }}
    
    /* AI 메시지 - 왼쪽 정렬, 유리 질감 (Glassmorphism) */
    [data-testid="stChatMessage"][data-message-author="assistant"] {{
        display: flex;
        flex-direction: row;
        align-items: flex-start;
    }}
    
    [data-testid="stChatMessage"][data-message-author="assistant"] > div:first-child {{
        margin-right: 1rem;
        flex-shrink: 0;
    }}
    
    [data-testid="stChatMessage"][data-message-author="assistant"] > div:last-child {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px) saturate(180%);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-left: 4px solid rgba(102, 126, 234, 0.9);
        border-radius: 20px;
        padding: 1.5rem 1.8rem;
        margin-left: 0;
        box-shadow: 
            0 4px 20px rgba(0, 0, 0, 0.3),
            0 0 30px rgba(102, 126, 234, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
        max-width: 75%;
        flex: 1;
        position: relative;
    }}
    
    [data-testid="stChatMessage"][data-message-author="assistant"] > div:last-child::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: 20px;
        padding: 1px;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.3), rgba(118, 75, 162, 0.3));
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        pointer-events: none;
    }}
    
    /* 사용자 메시지 - 오른쪽 정렬, 그라데이션 말풍선 */
    [data-testid="stChatMessage"][data-message-author="user"] {{
        display: flex;
        flex-direction: row-reverse;
        align-items: flex-start;
        justify-content: flex-end;
    }}
    
    [data-testid="stChatMessage"][data-message-author="user"] > div:first-child {{
        margin-left: 1rem;
        flex-shrink: 0;
    }}
    
    [data-testid="stChatMessage"][data-message-author="user"] > div:last-child {{
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.35) 0%, rgba(118, 75, 162, 0.35) 100%);
        border: 1px solid rgba(102, 126, 234, 0.5);
        border-right: 4px solid #667eea;
        border-radius: 20px;
        padding: 1.5rem 1.8rem;
        margin-right: 0;
        box-shadow: 
            0 4px 20px rgba(102, 126, 234, 0.4),
            0 0 30px rgba(102, 126, 234, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.25);
        max-width: 75%;
        flex: 1;
        backdrop-filter: blur(10px);
    }}
    
    /* 채팅 메시지 텍스트 색상 */
    [data-testid="stChatMessage"] p {{
        color: rgba(255, 255, 255, 0.95);
        line-height: 1.8;
        margin: 0;
        font-size: 1rem;
    }}
    
    /* 아바타 스타일 - 더 크고 빛나게 */
    [data-testid="stChatMessage"] img {{
        border-radius: 50%;
        width: 3rem;
        height: 3rem;
        box-shadow: 
            0 4px 15px rgba(102, 126, 234, 0.4),
            0 0 20px rgba(102, 126, 234, 0.2);
        border: 2px solid rgba(102, 126, 234, 0.5);
    }}
    
    /* 채팅 입력창 스타일 - 빛나는 테두리 */
    .stChatInput > div > div > textarea {{
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 16px !important;
        color: #ffffff !important;
        padding: 1rem 1.2rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px) !important;
    }}
    
    .stChatInput > div > div > textarea:focus {{
        border-color: #667eea !important;
        box-shadow: 
            0 0 0 3px rgba(102, 126, 234, 0.2),
            0 0 25px rgba(102, 126, 234, 0.4) !important;
        background-color: rgba(255, 255, 255, 0.08) !important;
        outline: none !important;
    }}
    
    .stChatInput > div > div > textarea::placeholder {{
        color: rgba(255, 255, 255, 0.4) !important;
    }}
    
    /* 성공/에러/경고 메시지 스타일 */
    .stSuccess {{
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(16, 185, 129, 0.1) 100%);
        border-left: 4px solid #10b981;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2);
        backdrop-filter: blur(10px);
    }}
    
    .stError {{
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(239, 68, 68, 0.1) 100%);
        border-left: 4px solid #ef4444;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.2);
        backdrop-filter: blur(10px);
    }}
    
    .stWarning {{
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(245, 158, 11, 0.1) 100%);
        border-left: 4px solid #f59e0b;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.2);
        backdrop-filter: blur(10px);
    }}
    
    /* 구분선 스타일 - 빛나는 효과 */
    hr {{
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.5), transparent);
        margin: 2rem 0;
    }}
    
    /* 라벨 스타일 */
    label {{
        color: rgba(255, 255, 255, 0.85) !important;
        font-weight: 600;
        font-size: 0.95rem;
    }}
    
    /* 플레이스홀더 스타일 */
    input::placeholder, textarea::placeholder {{
        color: rgba(255, 255, 255, 0.35) !important;
    }}
    
    /* 스피너 스타일 - 포인트 컬러 */
    .stSpinner > div {{
        border-color: #667eea;
        border-top-color: transparent;
    }}
    
    /* 스크롤바 스타일 */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: rgba(255, 255, 255, 0.05);
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }}
</style>
""", unsafe_allow_html=True)

# 브랜드 헤더 - 로고와 타이틀
if logo_base64:
    st.markdown(f"""
    <div class="brand-header">
        <div class="logo-container">
            <img src="data:image/png;base64,{logo_base64}" alt="AlphA AI Logo">
        </div>
        <div class="brand-title">AAA: AlphA AI</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="brand-header">
        <div class="brand-title">🤖 AAA: AlphA AI</div>
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
        st.markdown('<div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(16, 185, 129, 0.1) 100%); border-left: 4px solid #10b981; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2); backdrop-filter: blur(10px);">✅ <strong>OpenAI 자동 연결</strong></div>', unsafe_allow_html=True)
    else: 
        api_key = st.text_input("🔐 OpenAI Key", type="password", placeholder="sk-...")

    if secret_notion_key: 
        notion_key = secret_notion_key
        st.markdown('<div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(16, 185, 129, 0.1) 100%); border-left: 4px solid #10b981; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2); backdrop-filter: blur(10px);">✅ <strong>Notion 자동 연결</strong></div>', unsafe_allow_html=True)
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