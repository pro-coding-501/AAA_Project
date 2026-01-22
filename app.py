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

# 로고 이미지 인코딩 함수
def get_logo_base64():
    try:
        with open("AlphA AI2 1.png", "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

logo_base64 = get_logo_base64()

# ============================================
# 완전히 재설계된 Premium UI CSS
# ============================================
st.markdown(f"""
<style>
    /* ============================================ */
    /* CSS Variables - Apple Premium Dark Theme */
    /* ============================================ */
    :root {{
        --bg-primary: #000000;
        --bg-secondary: #1C1C1E;
        --bg-tertiary: #2C2C2E;
        --text-primary: #FFFFFF;
        --text-secondary: #8E8E93;
        --accent-color: #0A84FF;
        --border-color: rgba(255, 255, 255, 0.1);
        --glass-bg: rgba(28, 28, 30, 0.7);
    }}
    
    /* ============================================ */
    /* 폰트 & 기본 설정 */
    /* ============================================ */
    @import url('https://rsms.me/inter/inter.css');
    
    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }}
    
    /* Streamlit 기본 요소 숨기기 */
    footer {{visibility: hidden;}}
    #MainMenu {{visibility: hidden;}}
    header[data-testid="stHeader"] {{display: none;}}
    
    /* ============================================ */
    /* 전체 앱 배경 - Deep Premium Black */
    /* ============================================ */
    .stApp {{
        background: linear-gradient(180deg, var(--bg-primary) 0%, #0a0a0a 50%, var(--bg-secondary) 100%);
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', 'Inter', Roboto, Helvetica, Arial, sans-serif;
        min-height: 100vh;
        letter-spacing: -0.011em;
        color: var(--text-primary);
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }}
    
    /* ============================================ */
    /* 슬림 상단 앱 바 - Glassmorphism */
    /* ============================================ */
    .app-header {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 56px;
        background: var(--glass-bg);
        backdrop-filter: blur(40px) saturate(180%);
        -webkit-backdrop-filter: blur(40px) saturate(180%);
        border-bottom: 1px solid var(--border-color);
        display: flex;
        align-items: center;
        justify-content: space-between;
        z-index: 1000;
        padding: 0 2rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 1px 20px rgba(0, 0, 0, 0.5);
    }}
    
    .app-header-content {{
        max-width: 1400px;
        width: 100%;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    
    .app-header-left {{
        display: flex;
        align-items: center;
        gap: 0.875rem;
    }}
    
    .app-header-logo {{
        width: 28px;
        height: 28px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        animation: breathe 4s ease-in-out infinite;
    }}
    
    @keyframes breathe {{
        0%, 100% {{
            transform: scale(1);
            opacity: 1;
        }}
        50% {{
            transform: scale(1.05);
            opacity: 0.9;
        }}
    }}
    
    .app-header-logo img {{
        width: 100%;
        height: 100%;
        object-fit: contain;
        filter: brightness(1.2) contrast(1.08) drop-shadow(0 0 8px rgba(10, 132, 255, 0.15));
    }}
    
    .app-header-title {{
        color: #FFFFFF;
        font-size: 0.9375rem;
        font-weight: 500;
        letter-spacing: -0.02em;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        white-space: nowrap;
    }}
    
    .app-header-title .separator {{
        color: rgba(255, 255, 255, 0.25);
        font-weight: 300;
    }}
    
    .app-header-title .subtitle {{
        color: rgba(255, 255, 255, 0.65);
        font-weight: 400;
    }}
    
    .app-header-right {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    
    .header-icon-btn {{
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        color: rgba(255, 255, 255, 0.7);
        cursor: pointer;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        font-size: 0.875rem;
    }}
    
    .header-icon-btn:hover {{
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.12);
        color: rgba(255, 255, 255, 0.9);
        transform: translateY(-1px);
    }}
    
    /* 사이드바 토글 버튼 스타일 */
    button[kind="header"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapseButton"] button {{
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 8px !important;
        width: 36px !important;
        height: 36px !important;
        padding: 0 !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}
    
    [data-testid="stSidebarCollapseButton"] button:hover {{
        background: rgba(255, 255, 255, 0.08) !important;
        border-color: rgba(255, 255, 255, 0.12) !important;
        transform: translateY(-1px) !important;
    }}
    
    /* ============================================ */
    /* 메인 채팅 영역 - 중앙 정렬, 최대 너비 65% */
    /* ============================================ */
    .main .block-container {{
        padding-top: 5.5rem !important;
        padding-bottom: 12rem !important;
        max-width: 65% !important;
        margin: 0 auto !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }}
    
    @media (max-width: 1400px) {{
        .main .block-container {{
            max-width: 70%;
        }}
    }}
    
    @media (max-width: 1200px) {{
        .main .block-container {{
            max-width: 80%;
        }}
    }}
    
    @media (max-width: 768px) {{
        .main .block-container {{
            max-width: 95%;
            padding-top: 4.5rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }}
        .app-header {{
            padding: 0 1rem;
        }}
    }}
    
    /* ============================================ */
    /* 사이드바 - Premium Glass Drawer */
    /* ============================================ */
    [data-testid="stSidebar"] {{
        background: var(--glass-bg) !important;
        backdrop-filter: blur(60px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(60px) saturate(180%) !important;
        border-right: 1px solid var(--border-color) !important;
        box-shadow: 4px 0 64px rgba(0, 0, 0, 0.9), 
                    inset -1px 0 1px rgba(255, 255, 255, 0.05) !important;
        width: 320px !important;
    }}
    
    [data-testid="stSidebar"] > div:first-child {{
        background: transparent !important;
        padding-top: 1.5rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }}
    
    /* 사이드바 제목 */
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {{
        color: #FFFFFF !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em !important;
        font-size: 0.9375rem !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.875rem !important;
        opacity: 0.95 !important;
    }}
    
    [data-testid="stSidebar"] h3 {{
        font-size: 0.8125rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        opacity: 0.65 !important;
        font-weight: 500 !important;
    }}
    
    [data-testid="stSidebar"] h2:first-child,
    [data-testid="stSidebar"] h3:first-child {{
        margin-top: 0 !important;
    }}
    
    /* ============================================ */
    /* 버튼 - Premium Apple Style */
    /* ============================================ */
    .stButton > button {{
        background: rgba(255, 255, 255, 0.06) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.25rem !important;
        font-weight: 500 !important;
        font-size: 0.9375rem !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        letter-spacing: -0.015em !important;
        backdrop-filter: blur(20px) saturate(150%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(150%) !important;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.3), 
                    0 0 1px rgba(255, 255, 255, 0.08) inset !important;
    }}
    
    .stButton > button:hover {{
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(255, 255, 255, 0.16) !important;
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4), 
                    0 0 1px rgba(255, 255, 255, 0.12) inset !important;
    }}
    
    .stButton > button:active {{
        transform: translateY(0) scale(0.99) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
    }}
    
    /* ============================================ */
    /* 입력창 - Premium Glassmorphism */
    /* ============================================ */
    .stTextInput > div > div > input {{
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        padding: 0.875rem 1.125rem !important;
        font-size: 0.9375rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        letter-spacing: -0.015em !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2), 
                    0 0 1px rgba(255, 255, 255, 0.06) inset !important;
    }}
    
    .stTextInput > div > div > input:focus {{
        background: rgba(255, 255, 255, 0.08) !important;
        outline: none !important;
        border-color: var(--accent-color) !important;
        box-shadow: 0 0 0 4px rgba(10, 132, 255, 0.12), 
                    0 4px 16px rgba(0, 0, 0, 0.3), 
                    0 0 1px rgba(255, 255, 255, 0.1) inset !important;
        transform: translateY(-1px) !important;
    }}
    
    .stTextInput > div > div > input::placeholder {{
        color: var(--text-secondary) !important;
    }}
    
    /* 텍스트 영역 */
    .stTextArea > div > div > textarea {{
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        padding: 0.875rem 1.125rem !important;
        font-size: 0.9375rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        letter-spacing: -0.015em !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2), 
                    0 0 1px rgba(255, 255, 255, 0.06) inset !important;
    }}
    
    .stTextArea > div > div > textarea:focus {{
        background: rgba(255, 255, 255, 0.08) !important;
        outline: none !important;
        border-color: var(--accent-color) !important;
        box-shadow: 0 0 0 4px rgba(10, 132, 255, 0.12), 
                    0 4px 16px rgba(0, 0, 0, 0.3), 
                    0 0 1px rgba(255, 255, 255, 0.1) inset !important;
    }}
    
    .stTextArea > div > div > textarea::placeholder {{
        color: var(--text-secondary) !important;
    }}
    
    /* ============================================ */
    /* 채팅 메시지 - Premium Card Style */
    /* ============================================ */
    [data-testid="stChatMessage"] {{
        padding: 0 !important;
        margin-bottom: 1.5rem !important;
        background: transparent !important;
        width: 100% !important;
        display: flex !important;
        animation: messageAppear 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }}
    
    @keyframes messageAppear {{
        from {{
            opacity: 0;
            transform: translateY(12px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    /* AI 메시지 - 왼쪽 정렬 */
    [data-testid="stChatMessage"][data-message-author="assistant"] {{
        justify-content: flex-start !important;
    }}
    
    /* 사용자 메시지 - 오른쪽 정렬 */
    [data-testid="stChatMessage"][data-message-author="user"] {{
        justify-content: flex-end !important;
    }}
    
    /* 채팅 메시지 내부 컨테이너 */
    [data-testid="stChatMessage"] > div {{
        display: flex !important;
        align-items: flex-start !important;
        gap: 0.75rem !important;
        max-width: 88% !important;
    }}
    
    /* AI 메시지 내부 컨테이너 - 왼쪽 정렬 */
    [data-testid="stChatMessage"][data-message-author="assistant"] > div {{
        justify-content: flex-start !important;
    }}
    
    /* 사용자 메시지 내부 컨테이너 - 오른쪽 정렬, 아바타와 메시지 순서 반전 */
    [data-testid="stChatMessage"][data-message-author="user"] > div {{
        justify-content: flex-end !important;
        flex-direction: row-reverse !important;
    }}
    
    /* 아바타 이미지 스타일 */
    [data-testid="stChatMessage"] img {{
        border-radius: 50% !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        width: 32px !important;
        height: 32px !important;
        object-fit: cover !important;
        flex-shrink: 0 !important;
    }}
    
    /* AI 아바타 특별 효과 - Breathing Glow */
    [data-testid="stChatMessage"][data-message-author="assistant"] img {{
        background: rgba(255, 255, 255, 0.02) !important;
        padding: 2px !important;
        box-shadow: 0 0 0 0 rgba(10, 132, 255, 0) !important;
        animation: aiAvatarGlow 3s ease-in-out infinite !important;
    }}
    
    @keyframes aiAvatarGlow {{
        0%, 100% {{
            box-shadow: 0 0 8px rgba(10, 132, 255, 0.1), 
                        0 0 16px rgba(10, 132, 255, 0.05) !important;
            filter: brightness(1) contrast(1);
        }}
        50% {{
            box-shadow: 0 0 16px rgba(10, 132, 255, 0.2), 
                        0 0 32px rgba(10, 132, 255, 0.1) !important;
            filter: brightness(1.1) contrast(1.05);
        }}
    }}
    
    /* AI 메시지 말풍선 - Glassmorphism */
    [data-testid="stChatMessage"][data-message-author="assistant"] > div:last-child {{
        background: var(--glass-bg) !important;
        backdrop-filter: blur(20px) saturate(150%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(150%) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        padding: 1.25rem 1.5rem !important;
        color: var(--text-primary) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35), 
                    0 0 1px rgba(255, 255, 255, 0.08) inset !important;
        line-height: 1.75 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}
    
    [data-testid="stChatMessage"][data-message-author="assistant"] > div:last-child:hover {{
        border-color: rgba(255, 255, 255, 0.14) !important;
        box-shadow: 0 6px 28px rgba(0, 0, 0, 0.4), 
                    0 0 1px rgba(255, 255, 255, 0.12) inset !important;
    }}
    
    /* 사용자 메시지 말풍선 - Premium Blue Accent */
    [data-testid="stChatMessage"][data-message-author="user"] > div:last-child {{
        background: linear-gradient(135deg, 
            rgba(10, 132, 255, 0.15) 0%, 
            rgba(10, 132, 255, 0.08) 100%) !important;
        backdrop-filter: blur(20px) saturate(150%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(150%) !important;
        border: 1px solid rgba(10, 132, 255, 0.3) !important;
        border-radius: 20px !important;
        padding: 1.25rem 1.5rem !important;
        color: var(--text-primary) !important;
        box-shadow: 0 4px 20px rgba(10, 132, 255, 0.15), 
                    0 0 1px rgba(10, 132, 255, 0.2) inset !important;
        line-height: 1.75 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}
    
    [data-testid="stChatMessage"][data-message-author="user"] > div:last-child:hover {{
        border-color: rgba(10, 132, 255, 0.4) !important;
        box-shadow: 0 6px 28px rgba(10, 132, 255, 0.2), 
                    0 0 1px rgba(10, 132, 255, 0.3) inset !important;
    }}
    
    /* 채팅 메시지 텍스트 */
    [data-testid="stChatMessage"] p {{
        color: inherit !important;
        line-height: 1.75 !important;
        margin: 0 !important;
        font-size: 0.9375rem !important;
        letter-spacing: -0.01em !important;
    }}
    
    /* 채팅 메시지 내부 모든 텍스트 요소 */
    [data-testid="stChatMessage"] * {{
        font-size: 0.9375rem !important;
    }}
    
    [data-testid="stChatMessage"] h1,
    [data-testid="stChatMessage"] h2,
    [data-testid="stChatMessage"] h3,
    [data-testid="stChatMessage"] h4 {{
        font-size: inherit !important;
    }}
    
    /* ============================================ */
    /* 채팅 입력창 - Premium Floating Bar */
    /* ============================================ */
    .stChatInput {{
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        padding: 1.75rem 2rem !important;
        background: var(--glass-bg) !important;
        backdrop-filter: blur(60px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(60px) saturate(180%) !important;
        border-top: 1px solid var(--border-color) !important;
        box-shadow: 0 -8px 48px rgba(0, 0, 0, 0.8), 
                    inset 0 1px 1px rgba(255, 255, 255, 0.05) !important;
        z-index: 999 !important;
    }}
    
    .stChatInput > div {{
        max-width: 65% !important;
        margin: 0 auto !important;
    }}
    
    @media (max-width: 1400px) {{
        .stChatInput > div {{
            max-width: 70% !important;
        }}
    }}
    
    @media (max-width: 1200px) {{
        .stChatInput > div {{
            max-width: 80% !important;
        }}
    }}
    
    @media (max-width: 768px) {{
        .stChatInput > div {{
            max-width: 95% !important;
        }}
        .stChatInput {{
            padding: 1.25rem 1rem !important;
        }}
    }}
    
    .stChatInput > div > div > textarea {{
        background: rgba(255, 255, 255, 0.06) !important;
        border: 1px solid rgba(255, 255, 255, 0.14) !important;
        border-radius: 28px !important;
        color: var(--text-primary) !important;
        padding: 1.125rem 1.75rem !important;
        font-size: 1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        letter-spacing: -0.015em !important;
        backdrop-filter: blur(30px) saturate(150%) !important;
        -webkit-backdrop-filter: blur(30px) saturate(150%) !important;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.4), 
                    0 0 1px rgba(255, 255, 255, 0.1) inset !important;
        min-height: 56px !important;
        resize: none !important;
    }}
    
    .stChatInput > div > div > textarea:focus {{
        background: rgba(255, 255, 255, 0.09) !important;
        outline: none !important;
        border-color: var(--accent-color) !important;
        box-shadow: 0 0 0 4px rgba(10, 132, 255, 0.15), 
                    0 6px 32px rgba(0, 0, 0, 0.5), 
                    0 0 1px rgba(255, 255, 255, 0.12) inset !important;
        transform: translateY(-2px) !important;
    }}
    
    .stChatInput > div > div > textarea::placeholder {{
        color: var(--text-secondary) !important;
        font-weight: 400 !important;
    }}
    
    /* ============================================ */
    /* 라벨 및 기타 요소 */
    /* ============================================ */
    label {{
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        letter-spacing: -0.015em !important;
        opacity: 0.9 !important;
        transition: color 0.2s ease !important;
    }}
    
    label:hover {{
        color: rgba(255, 255, 255, 0.8) !important;
    }}
    
    /* 성공 메시지 - Apple Green */
    .stSuccess {{
        background: rgba(52, 199, 89, 0.15) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(52, 199, 89, 0.3) !important;
        border-radius: 12px !important;
        padding: 1rem 1.125rem !important;
        color: #32D74B !important;
        font-weight: 500 !important;
        box-shadow: 0 2px 12px rgba(52, 199, 89, 0.15) !important;
    }}
    
    /* 에러 메시지 - Apple Red */
    .stError {{
        background: rgba(255, 59, 48, 0.15) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 59, 48, 0.3) !important;
        border-radius: 12px !important;
        padding: 1rem 1.125rem !important;
        color: #FF453A !important;
        font-weight: 500 !important;
        box-shadow: 0 2px 12px rgba(255, 59, 48, 0.15) !important;
    }}
    
    /* 구분선 - Apple Style */
    hr {{
        border: none !important;
        height: 1px !important;
        background: var(--border-color) !important;
        margin: 2rem 0 !important;
        opacity: 0.8 !important;
    }}
    
    /* ============================================ */
    /* 스크롤바 - Minimal & Premium */
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
        border: 2px solid transparent;
        background-clip: padding-box;
        transition: background 0.2s ease;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: rgba(255, 255, 255, 0.16);
        background-clip: padding-box;
    }}
    
    ::-webkit-scrollbar-thumb:active {{
        background: rgba(255, 255, 255, 0.2);
        background-clip: padding-box;
    }}
    
    /* ============================================ */
    /* 타이핑 인디케이터 - Apple Style */
    /* ============================================ */
    .typing-indicator {{
        display: inline-flex;
        gap: 6px;
        padding: 0.625rem 0;
        align-items: center;
    }}
    
    .typing-indicator span {{
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: var(--accent-color);
        animation: typingDot 1.6s infinite ease-in-out;
        box-shadow: 0 0 8px rgba(10, 132, 255, 0.3);
    }}
    
    .typing-indicator span:nth-child(2) {{
        animation-delay: 0.2s;
    }}
    
    .typing-indicator span:nth-child(3) {{
        animation-delay: 0.4s;
    }}
    
    @keyframes typingDot {{
        0%, 60%, 100% {{
            transform: translateY(0) scale(1);
            opacity: 0.3;
        }}
        30% {{
            transform: translateY(-8px) scale(1.1);
            opacity: 1;
        }}
    }}
    
    /* ============================================ */
    /* 추가 시각 효과 - Smooth Transitions */
    /* ============================================ */
    * {{
        transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}
    
    /* 포커스 가시성 제거 (키보드 접근성은 유지) */
    *:focus-visible {{
        outline: none !important;
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
    # 잠금 화면 CSS 추가 - Premium Apple Style with Enhanced Glassmorphism
    st.markdown(f"""
    <style>
        .stApp {{
            overflow: hidden !important;
        }}
        .main .block-container {{
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            max-width: 100% !important;
        }}
        .lock-screen-wrapper {{
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
            background: radial-gradient(circle at 50% 50%, rgba(10, 132, 255, 0.03) 0%, transparent 50%);
        }}
        .lock-card {{
            background: var(--glass-bg);
            backdrop-filter: blur(60px) saturate(180%);
            -webkit-backdrop-filter: blur(60px) saturate(180%);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 28px;
            padding: 4rem 3.5rem;
            width: 100%;
            max-width: 460px;
            box-shadow: 0 32px 80px rgba(0, 0, 0, 0.9), 
                        0 0 1px rgba(255, 255, 255, 0.1) inset;
            text-align: center;
            margin: 0 auto;
            animation: lockCardAppear 0.6s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
        }}
        .lock-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, 
                transparent, 
                rgba(255, 255, 255, 0.2), 
                transparent);
            border-radius: 28px 28px 0 0;
        }}
        @keyframes lockCardAppear {{
            from {{
                opacity: 0;
                transform: translateY(24px) scale(0.96);
            }}
            to {{
                opacity: 1;
                transform: translateY(0) scale(1);
            }}
        }}
        .lock-logo {{
            width: 72px;
            height: 72px;
            margin: 0 auto 1.5rem;
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.1);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
            animation: logoGlow 3s ease-in-out infinite;
        }}
        .lock-logo img {{
            width: 52px;
            height: 52px;
            object-fit: contain;
            filter: brightness(1.2) contrast(1.1);
        }}
        @keyframes logoGlow {{
            0%, 100% {{
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
            }}
            50% {{
                box-shadow: 0 8px 32px rgba(10, 132, 255, 0.15), 
                            0 0 40px rgba(10, 132, 255, 0.05);
            }}
        }}
        .lock-title {{
            color: var(--text-primary);
            font-size: 2.125rem;
            font-weight: 600;
            margin-bottom: 0.625rem;
            letter-spacing: -0.04em;
            line-height: 1.2;
        }}
        .lock-subtitle {{
            color: var(--text-secondary);
            font-size: 1rem;
            margin-bottom: 2.75rem;
            letter-spacing: -0.015em;
            line-height: 1.5;
            font-weight: 400;
        }}
        .error-message {{
            background: rgba(255, 59, 48, 0.15);
            border: 1px solid rgba(255, 59, 48, 0.3);
            border-radius: 12px;
            color: #FF453A;
            padding: 1rem;
            margin-top: 1.25rem;
            font-size: 0.875rem;
            animation: shake 0.5s cubic-bezier(0.36, 0.07, 0.19, 0.97);
            backdrop-filter: blur(10px);
            font-weight: 500;
        }}
        @keyframes shake {{
            0%, 100% {{ transform: translateX(0); }}
            10%, 30%, 50%, 70%, 90% {{ transform: translateX(-6px); }}
            20%, 40%, 60%, 80% {{ transform: translateX(6px); }}
        }}
        
        /* 로그인 Form 스타일 개선 */
        .lock-screen-wrapper .stTextInput > div > div > input {{
            background: rgba(255, 255, 255, 0.06) !important;
            border: 1px solid rgba(255, 255, 255, 0.14) !important;
            border-radius: 14px !important;
            padding: 1rem 1.25rem !important;
            font-size: 1rem !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            text-align: center !important;
        }}
        .lock-screen-wrapper .stTextInput > div > div > input:focus {{
            background: rgba(255, 255, 255, 0.09) !important;
            border-color: var(--accent-color) !important;
            box-shadow: 0 0 0 4px rgba(10, 132, 255, 0.12), 
                        0 8px 24px rgba(0, 0, 0, 0.3) !important;
            transform: translateY(-1px) !important;
        }}
        .lock-screen-wrapper .stButton > button {{
            background: linear-gradient(180deg, 
                var(--accent-color) 0%, 
                #0066CC 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 14px !important;
            padding: 1rem 1.5rem !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            margin-top: 0.75rem !important;
            box-shadow: 0 4px 16px rgba(10, 132, 255, 0.3) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }}
        .lock-screen-wrapper .stButton > button:hover {{
            background: linear-gradient(180deg, 
                #1F8FFF 0%, 
                #0077DD 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 24px rgba(10, 132, 255, 0.4) !important;
        }}
        .lock-screen-wrapper .stButton > button:active {{
            transform: translateY(0) !important;
        }}
    </style>
    """, unsafe_allow_html=True)
    
    # 잠금 화면 UI
    st.markdown('<div class="lock-screen-wrapper">', unsafe_allow_html=True)
    
    # 로고와 타이틀 HTML
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
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Form을 사용하여 Enter 키 지원 추가
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
    
    # 잠금 화면에서는 여기서 종료
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
            <div class="app-header-right">
                <!-- 유틸리티 아이콘 영역 (향후 확장 가능) -->
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