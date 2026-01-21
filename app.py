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
    /* 웹폰트 로드 - AI 앱 스타일 폰트 */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    /* Streamlit 기본 푸터만 숨기기 */
    footer {{visibility: hidden;}}
    
    /* 헤더의 텍스트는 숨기되, 버튼은 유지 */
    header .css-1d391kg {{visibility: hidden;}}
    header [data-testid="stHeader"] > div:first-child {{visibility: hidden;}}
    
    /* 사이드바 토글 버튼 - 항상 보이도록 강제 */
    button[data-testid="baseButton-header"],
    [data-testid="collapsedControl"],
    button[kind="header"],
    [data-testid="stHeader"] button {{
        visibility: visible !important;
        display: flex !important;
        opacity: 1 !important;
        z-index: 999 !important;
        position: fixed !important;
        top: 1rem !important;
        left: 1rem !important;
        background: rgba(6, 182, 212, 0.15) !important;
        border: 1.5px solid rgba(6, 182, 212, 0.3) !important;
        border-radius: 12px !important;
        padding: 0.6rem 0.8rem !important;
        box-shadow: 0 4px 20px rgba(6, 182, 212, 0.15) !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        backdrop-filter: blur(10px) !important;
    }}
    
    button[data-testid="baseButton-header"]:hover,
    [data-testid="collapsedControl"]:hover,
    button[kind="header"]:hover {{
        background: rgba(6, 182, 212, 0.25) !important;
        box-shadow: 0 0 30px rgba(6, 182, 212, 0.3) !important;
        transform: scale(1.05) !important;
        border-color: rgba(6, 182, 212, 0.5) !important;
    }}
    
    /* 햄버거 아이콘 색상 */
    button[data-testid="baseButton-header"] svg,
    [data-testid="collapsedControl"] svg,
    button[kind="header"] svg {{
        color: #06b6d4 !important;
        stroke: #06b6d4 !important;
        fill: #06b6d4 !important;
        width: 1.5rem !important;
        height: 1.5rem !important;
    }}
    
    /* 전체 배경 - 세련된 다크모드 그라데이션 */
    .stApp {{
        background: 
            /* 미묘한 그라데이션 레이어 */
            radial-gradient(ellipse at top left, rgba(6, 182, 212, 0.06) 0%, transparent 50%),
            radial-gradient(ellipse at top right, rgba(14, 165, 233, 0.05) 0%, transparent 50%),
            radial-gradient(ellipse at bottom center, rgba(20, 184, 166, 0.04) 0%, transparent 60%),
            /* 메인 다크 그라데이션 */
            linear-gradient(180deg, #0f0f1e 0%, #1a1a2e 30%, #1e1e3e 60%, #0f0f1e 100%);
        background-attachment: fixed;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
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
        background: radial-gradient(ellipse, rgba(6, 182, 212, 0.12) 0%, transparent 70%);
        filter: blur(60px);
        z-index: -1;
        animation: pulse 4s ease-in-out infinite;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ opacity: 0.5; }}
        50% {{ opacity: 0.8; }}
    }}
    
    .logo-container {{
        width: 80px;
        height: 80px;
        border-radius: 18px;
        overflow: hidden;
        box-shadow: 
            0 8px 32px rgba(6, 182, 212, 0.25),
            0 0 30px rgba(6, 182, 212, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
        border: 2px solid rgba(6, 182, 212, 0.35);
        position: relative;
        animation: glow 3s ease-in-out infinite alternate;
        backdrop-filter: blur(10px);
    }}
    
    @keyframes glow {{
        from {{
            box-shadow: 
                0 8px 32px rgba(6, 182, 212, 0.25),
                0 0 30px rgba(6, 182, 212, 0.15),
                inset 0 1px 0 rgba(255, 255, 255, 0.15);
        }}
        to {{
            box-shadow: 
                0 8px 32px rgba(6, 182, 212, 0.35),
                0 0 50px rgba(14, 165, 233, 0.25),
                inset 0 1px 0 rgba(255, 255, 255, 0.2);
        }}
    }}
    
    .logo-container img {{
        width: 100%;
        height: 100%;
        object-fit: contain;
        filter: drop-shadow(0 0 8px rgba(6, 182, 212, 0.35));
    }}
    
    .brand-title {{
        font-family: 'Space Grotesk', 'Inter', sans-serif;
        font-size: 3.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #06b6d4 0%, #0891b2 40%, #14b8a6 70%, #22d3ee 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.04em;
        position: relative;
        text-transform: uppercase;
        font-style: normal;
        line-height: 1.1;
    }}
    
    .brand-title::after {{
        content: '';
        position: absolute;
        top: 50%;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(6, 182, 212, 0.25), transparent);
        transform: translateY(55px);
    }}
    
    /* 사이드바 스타일 - 세련된 다크 배경 */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, rgba(15, 15, 30, 0.95) 0%, rgba(20, 20, 40, 0.95) 100%);
        border-right: 1px solid rgba(6, 182, 212, 0.15);
        box-shadow: 4px 0 40px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(20px) saturate(180%);
    }}
    
    /* 사이드바 헤더 스타일 */
    [data-testid="stSidebar"] h2 {{
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(6, 182, 212, 0.15);
        letter-spacing: -0.01em;
        font-family: 'Inter', sans-serif;
    }}
    
    [data-testid="stSidebar"] h3 {{
        font-size: 1.4rem;
        font-weight: 600;
        background: linear-gradient(135deg, #0891b2 0%, #14b8a6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(8, 145, 178, 0.15);
        font-family: 'Inter', sans-serif;
    }}
    
    /* 버튼 스타일 - 세련된 그라데이션 */
    .stButton > button {{
        background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 1.8rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 
            0 4px 20px rgba(6, 182, 212, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
        position: relative;
        overflow: hidden;
        font-family: 'Inter', sans-serif;
    }}
    
    .stButton > button::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.15), transparent);
        transition: left 0.5s;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 
            0 8px 30px rgba(6, 182, 212, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        background: linear-gradient(135deg, #0891b2 0%, #14b8a6 100%);
    }}
    
    .stButton > button:hover::before {{
        left: 100%;
    }}
    
    .stButton > button:active {{
        transform: translateY(0);
    }}
    
    /* 텍스트 입력창 스타일 - 세련된 Underline */
    .stTextInput > div > div > input {{
        background-color: rgba(255, 255, 255, 0.04);
        border: none;
        border-bottom: 1.5px solid rgba(6, 182, 212, 0.25);
        border-radius: 0;
        color: #ffffff;
        padding: 0.8rem 0.5rem;
        transition: all 0.3s ease;
        font-size: 0.95rem;
        font-family: 'Inter', sans-serif;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-bottom-color: #06b6d4;
        background-color: rgba(255, 255, 255, 0.06);
        box-shadow: 0 2px 8px rgba(6, 182, 212, 0.15);
        outline: none;
    }}
    
    .stTextInput > div > div > input::placeholder {{
        color: rgba(255, 255, 255, 0.35);
    }}
    
    /* 텍스트 영역 스타일 - 깔끔한 테두리 */
    .stTextArea > div > div > textarea {{
        background-color: rgba(255, 255, 255, 0.04);
        border: 1.5px solid rgba(6, 182, 212, 0.2);
        border-radius: 12px;
        color: #ffffff;
        padding: 1rem;
        transition: all 0.3s ease;
        font-size: 0.95rem;
        font-family: 'Inter', sans-serif;
    }}
    
    .stTextArea > div > div > textarea:focus {{
        border-color: #06b6d4;
        box-shadow: 
            0 0 0 2px rgba(6, 182, 212, 0.12),
            0 4px 16px rgba(6, 182, 212, 0.15);
        background-color: rgba(255, 255, 255, 0.06);
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
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(20px) saturate(180%);
        border: 1px solid rgba(6, 182, 212, 0.2);
        border-left: 3px solid rgba(6, 182, 212, 0.7);
        border-radius: 16px;
        padding: 1.5rem 1.8rem;
        margin-left: 0;
        box-shadow: 
            0 4px 24px rgba(0, 0, 0, 0.3),
            0 0 20px rgba(6, 182, 212, 0.12),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
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
        border-radius: 16px;
        padding: 1px;
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.15), rgba(8, 145, 178, 0.15));
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        pointer-events: none;
    }}
    
    /* 사용자 메시지 - 오른쪽 정렬, 세련된 그라데이션 */
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
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.2) 0%, rgba(8, 145, 178, 0.2) 100%);
        border: 1px solid rgba(6, 182, 212, 0.3);
        border-right: 3px solid rgba(6, 182, 212, 0.7);
        border-radius: 16px;
        padding: 1.5rem 1.8rem;
        margin-right: 0;
        box-shadow: 
            0 4px 24px rgba(6, 182, 212, 0.2),
            0 0 20px rgba(6, 182, 212, 0.12),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
        max-width: 75%;
        flex: 1;
        backdrop-filter: blur(15px);
    }}
    
    /* 채팅 메시지 텍스트 색상 */
    [data-testid="stChatMessage"] p {{
        color: rgba(255, 255, 255, 0.95);
        line-height: 1.8;
        margin: 0;
        font-size: 1rem;
    }}
    
    /* 아바타 스타일 - 세련된 그림자 */
    [data-testid="stChatMessage"] img {{
        border-radius: 50%;
        width: 3rem;
        height: 3rem;
        box-shadow: 
            0 4px 20px rgba(6, 182, 212, 0.25),
            0 0 15px rgba(6, 182, 212, 0.12);
        border: 2px solid rgba(6, 182, 212, 0.35);
    }}
    
    /* 채팅 입력창 스타일 - 세련된 테두리 */
    .stChatInput > div > div > textarea {{
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1.5px solid rgba(6, 182, 212, 0.2) !important;
        border-radius: 14px !important;
        color: #ffffff !important;
        padding: 1rem 1.2rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(15px) !important;
        font-family: 'Inter', sans-serif !important;
    }}
    
    .stChatInput > div > div > textarea:focus {{
        border-color: #06b6d4 !important;
        box-shadow: 
            0 0 0 2px rgba(6, 182, 212, 0.12),
            0 4px 20px rgba(6, 182, 212, 0.2) !important;
        background-color: rgba(255, 255, 255, 0.08) !important;
        outline: none !important;
    }}
    
    .stChatInput > div > div > textarea::placeholder {{
        color: rgba(255, 255, 255, 0.4) !important;
    }}
    
    /* 성공/에러/경고 메시지 스타일 */
    .stSuccess {{
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.08) 100%);
        border-left: 3px solid #10b981;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.15);
        backdrop-filter: blur(15px);
    }}
    
    .stError {{
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(239, 68, 68, 0.08) 100%);
        border-left: 3px solid #ef4444;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.15);
        backdrop-filter: blur(15px);
    }}
    
    .stWarning {{
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(245, 158, 11, 0.08) 100%);
        border-left: 3px solid #f59e0b;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 20px rgba(245, 158, 11, 0.15);
        backdrop-filter: blur(15px);
    }}
    
    /* 구분선 스타일 - 미묘한 효과 */
    hr {{
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(6, 182, 212, 0.25), transparent);
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
    
    /* 스피너 스타일 - 세련된 컬러 */
    .stSpinner > div {{
        border-color: #06b6d4;
        border-top-color: transparent;
    }}
    
    /* 스크롤바 스타일 */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: rgba(255, 255, 255, 0.03);
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(135deg, #0891b2 0%, #14b8a6 100%);
    }}
</style>
<script>
    // 사이드바 토글 버튼을 명시적으로 보이도록 설정
    function ensureSidebarToggle() {{
        // 여러 선택자로 버튼 찾기
        const selectors = [
            'button[data-testid="baseButton-header"]',
            '[data-testid="collapsedControl"]',
            'button[kind="header"]',
            '[data-testid="stHeader"] button',
            'button[aria-label*="sidebar"]',
            'button[aria-label*="menu"]'
        ];
        
        let sidebarToggle = null;
        for (const selector of selectors) {{
            sidebarToggle = document.querySelector(selector);
            if (sidebarToggle) break;
        }}
        
        // 버튼이 없으면 생성
        if (!sidebarToggle) {{
            sidebarToggle = document.createElement('button');
            sidebarToggle.setAttribute('data-testid', 'custom-sidebar-toggle');
            sidebarToggle.innerHTML = '☰';
            sidebarToggle.setAttribute('aria-label', 'Open sidebar');
            document.body.appendChild(sidebarToggle);
        }}
        
        // 스타일 적용
        sidebarToggle.style.cssText = `
            position: fixed !important;
            top: 1rem !important;
            left: 1rem !important;
            z-index: 999 !important;
            background: rgba(6, 182, 212, 0.15) !important;
            border: 1.5px solid rgba(6, 182, 212, 0.3) !important;
            border-radius: 12px !important;
            padding: 0.6rem 0.8rem !important;
            color: #06b6d4 !important;
            font-size: 1.5rem !important;
            cursor: pointer !important;
            box-shadow: 0 4px 20px rgba(6, 182, 212, 0.15) !important;
            transition: all 0.3s ease !important;
            visibility: visible !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            opacity: 1 !important;
            backdrop-filter: blur(10px) !important;
        `;
        
        // 호버 효과
        sidebarToggle.onmouseenter = function() {{
            this.style.background = 'rgba(6, 182, 212, 0.25)';
            this.style.boxShadow = '0 0 30px rgba(6, 182, 212, 0.3)';
            this.style.transform = 'scale(1.05)';
            this.style.borderColor = 'rgba(6, 182, 212, 0.5)';
        }};
        
        sidebarToggle.onmouseleave = function() {{
            this.style.background = 'rgba(6, 182, 212, 0.15)';
            this.style.boxShadow = '0 4px 20px rgba(6, 182, 212, 0.15)';
            this.style.transform = 'scale(1)';
            this.style.borderColor = 'rgba(6, 182, 212, 0.3)';
        }};
        
        // 클릭 이벤트 - Streamlit 사이드바 토글
        sidebarToggle.onclick = function(e) {{
            e.preventDefault();
            e.stopPropagation();
            
            // Streamlit의 사이드바 토글 이벤트 발생
            const sidebar = document.querySelector('[data-testid="stSidebar"]');
            if (sidebar) {{
                // Streamlit의 내부 함수 호출 시도
                if (window.parent && window.parent.postMessage) {{
                    window.parent.postMessage({{type: 'streamlit:setFrameHeight'}}, '*');
                }}
                
                // 직접 토글
                const isCollapsed = sidebar.classList.contains('css-1d391kg') || 
                                   sidebar.style.display === 'none' ||
                                   sidebar.offsetWidth === 0;
                
                if (isCollapsed) {{
                    sidebar.style.display = 'block';
                    sidebar.style.visibility = 'visible';
                }} else {{
                    // 사이드바를 닫지 않고 유지 (사용자가 X 버튼으로 닫을 수 있음)
                }}
            }}
            
            // Streamlit의 기본 토글 동작 시도
            const clickEvent = new MouseEvent('click', {{
                bubbles: true,
                cancelable: true,
                view: window
            }});
            
            // 원본 버튼이 있으면 클릭
            const originalBtn = document.querySelector('button[data-testid="baseButton-header"]') ||
                               document.querySelector('[data-testid="collapsedControl"]');
            if (originalBtn) {{
                originalBtn.dispatchEvent(clickEvent);
            }}
        }};
    }}
    
    // 즉시 실행
    ensureSidebarToggle();
    
    // DOM 로드 후 실행
    if (document.readyState === 'loading') {{
        document.addEventListener('DOMContentLoaded', ensureSidebarToggle);
    }}
    
    // Streamlit이 DOM을 업데이트할 때마다 실행 (debounce)
    let timeout;
    const observer = new MutationObserver(function() {{
        clearTimeout(timeout);
        timeout = setTimeout(ensureSidebarToggle, 100);
    }});
    observer.observe(document.body, {{ childList: true, subtree: true }});
</script>
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
        st.markdown('<div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.08) 100%); border-left: 3px solid #10b981; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; box-shadow: 0 4px 20px rgba(16, 185, 129, 0.15); backdrop-filter: blur(15px);">✅ <strong>OpenAI 자동 연결</strong></div>', unsafe_allow_html=True)
    else: 
        api_key = st.text_input("🔐 OpenAI Key", type="password", placeholder="sk-...")

    if secret_notion_key: 
        notion_key = secret_notion_key
        st.markdown('<div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.08) 100%); border-left: 3px solid #10b981; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; box-shadow: 0 4px 20px rgba(16, 185, 129, 0.15); backdrop-filter: blur(15px);">✅ <strong>Notion 자동 연결</strong></div>', unsafe_allow_html=True)
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