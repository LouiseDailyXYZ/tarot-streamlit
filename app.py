import streamlit as st
import requests
import random
import time
import os
from PIL import Image

# 頁面配置
st.set_page_config(
    page_title="🔮 Tarot Reading",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 塔羅牌資料
TAROT_DECK = [
    {"name": "愚者", "image": "fool.jpg", "keywords": ["新開始", "冒險", "信任直覺"]},
    {"name": "魔術師", "image": "magician.jpg", "keywords": ["顯化", "創造力", "技能"]},
    {"name": "女祭司", "image": "high-priestess.jpg", "keywords": ["直覺", "內在智慧", "神秘"]},
    {"name": "皇后", "image": "empress.jpg", "keywords": ["創造力", "豐盛", "母性"]},
    {"name": "皇帝", "image": "emperor.jpg", "keywords": ["權威", "結構", "控制"]},
    {"name": "教皇", "image": "hierophant.jpg", "keywords": ["傳統", "精神指導", "學習"]},
    {"name": "戀人", "image": "lovers.jpg", "keywords": ["愛情", "選擇", "和諧"]},
    {"name": "戰車", "image": "chariot.jpg", "keywords": ["意志力", "勝利", "方向"]},
    {"name": "力量", "image": "strength.jpg", "keywords": ["內在力量", "勇氣", "耐心"]},
    {"name": "隱者", "image": "hermit.jpg", "keywords": ["內省", "尋求真理", "智慧"]},
    {"name": "命運之輪", "image": "wheel-of-fortune.jpg", "keywords": ["變化", "循環", "命運"]},
    {"name": "正義", "image": "justice.jpg", "keywords": ["平衡", "公正", "真相"]},
    {"name": "倒吊人", "image": "hanged-man.jpg", "keywords": ["犧牲", "新視角", "放手"]},
    {"name": "死神", "image": "death.jpg", "keywords": ["轉變", "結束", "重生"]},
    {"name": "節制", "image": "temperance.jpg", "keywords": ["平衡", "調和", "耐心"]},
    {"name": "惡魔", "image": "devil.jpg", "keywords": ["束縛", "誘惑", "物質主義"]},
    {"name": "高塔", "image": "tower.jpg", "keywords": ["突然變化", "啟示", "解放"]},
    {"name": "星星", "image": "star.jpg", "keywords": ["希望", "靈感", "療癒"]},
    {"name": "月亮", "image": "moon.jpg", "keywords": ["幻覺", "潛意識", "直覺"]},
    {"name": "太陽", "image": "sun.jpg", "keywords": ["成功", "快樂", "活力"]},
    {"name": "審判", "image": "judgement.jpg", "keywords": ["重生", "原諒", "新階段"]},
    {"name": "世界", "image": "world.jpg", "keywords": ["完成", "成就", "旅程結束"]}
]

def load_card_image(card):
    """載入卡牌圖片"""
    image_paths = [
        f"images/{card['image']}",
        f"./images/{card['image']}"
    ]
    
    for path in image_paths:
        if os.path.exists(path):
            try:
                return Image.open(path)
            except:
                continue
    return None

def get_tarot_reading(card_name, question, keywords):
    """使用 DeepSeek API 獲取塔羅解讀"""
    system_prompt = """你是一位專業、智慧且充滿洞察力的塔羅占卜師。你擁有深厚的塔羅知識和豐富的人生智慧，能夠為來訪者提供溫暖、實用且具有啟發性的指引。
請用溫暖、專業且易懂的語言進行解讀，避免過於神秘或模糊的表達。重點是提供實用的建議和積極的指引。"""
    
    user_prompt = f"""請為以下塔羅占卜提供深入而有意義的解讀：
【抽到的牌卡】：{card_name}
【牌卡關鍵詞】：{', '.join(keywords)}
【具體問題】：{question}

請提供一個完整且個人化的塔羅解讀，包含以下要素：
1. **牌卡核心含義**：這張牌在當前情況下的主要象徵意義
2. **針對性指引**：針對提問者的具體問題給出的建議和洞察
3. **行動建議**：實際可行的行動方向或需要注意的事項  
4. **正面展望**：鼓勵性的訊息和未來的可能性

請用親切、專業的語調，字數控制在 200-300 字之間。重點是幫助提問者獲得清晰的指引和內心的平靜。"""
    
    try:
        api_key = st.secrets["DEEPSEEK_API_KEY"]
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'deepseek-chat',
            'messages': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt}
            ],
            'max_tokens': 600,
            'temperature': 0.7,
            'top_p': 0.9
        }
        
        response = requests.post(
            'https://api.deepseek.com/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        else:
            return get_fallback_reading(card_name, question, keywords)
            
    except Exception as e:
        return get_fallback_reading(card_name, question, keywords)

def get_fallback_reading(card_name, question, keywords):
    """備用解讀"""
    return f"{card_name}為您帶來{', '.join(keywords)}的訊息。針對您的問題「{question}」，這張牌提醒您要相信內在的智慧，勇敢面對當前的挑戰和機會。{card_name}象徵著轉變和成長的時期，建議您保持開放的心態，聆聽內心的聲音。記住，您擁有改變現狀的能力，相信自己的直覺，一切都會朝好的方向發展。"

def apply_modern_dark_theme():
    """應用現代黑色主題"""
    st.markdown("""
    <style>
    /* 隱藏 Streamlit 預設元素 */
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    .stApp {
        background: #1a1a1a !important;
        font-family: "Noto Serif", "Noto Sans", sans-serif !important;
    }
    
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    .stDeployButton {
        display: none !important;
    }
    
    /* 主容器 */
    .main-container {
        min-height: 100vh;
        background: #1a1a1a;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
    }
    
    /* 標題樣式 */
    .page-title {
        color: white;
        font-size: 28px;
        font-weight: 700;
        line-height: 1.2;
        text-align: center;
        padding: 1rem;
        margin-bottom: 0.75rem;
        margin-top: 1.25rem;
    }
    
    .page-subtitle {
        color: white;
        font-size: 16px;
        font-weight: 400;
        line-height: 1.5;
        text-align: center;
        padding: 0.25rem 1rem 0.75rem;
        margin-bottom: 0.75rem;
    }
    
    /* 卡牌名稱 */
    .card-name {
        color: white;
        font-size: 22px;
        font-weight: 700;
        line-height: 1.2;
        text-align: center;
        padding: 1rem;
        margin-bottom: 0.75rem;
        margin-top: 1.25rem;
    }
    
    /* 輸入框樣式 */
    .stTextInput > div > div > input {
        background: #363636 !important;
        border: none !important;
        border-radius: 12px !important;
        color: white !important;
        font-size: 16px !important;
        font-weight: 400 !important;
        height: 56px !important;
        padding: 1rem !important;
        box-shadow: none !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #adadad !important;
    }
    
    .stTextInput > div > div > input:focus {
        outline: none !important;
        ring: none !important;
        border: none !important;
    }
    
    /* 文字區域樣式 */
    .stTextArea > div > div > textarea {
        background: #363636 !important;
        border: none !important;
        border-radius: 12px !important;
        color: white !important;
        font-size: 16px !important;
        font-weight: 400 !important;
        min-height: 120px !important;
        padding: 1rem !important;
        resize: vertical !important;
        box-shadow: none !important;
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: #adadad !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        outline: none !important;
        ring: none !important;
        border: none !important;
    }
    
    /* 按鈕樣式 */
    .stButton > button {
        background: black !important;
        color: white !important;
        border: none !important;
        border-radius: 9999px !important;
        height: 48px !important;
        padding: 0 1.25rem !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        letter-spacing: 0.015em !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        background: #333 !important;
        transform: translateY(-1px) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* 關閉按鈕 */
    .close-button {
        position: absolute;
        top: 1rem;
        right: 1rem;
        background: transparent;
        border: none;
        color: white;
        cursor: pointer;
        padding: 0.75rem;
        border-radius: 9999px;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10;
    }
    
    .close-button:hover {
        background: rgba(255, 255, 255, 0.1);
    }
    
    /* 輸入容器 */
    .input-container {
        max-width: 480px;
        padding: 0.75rem 1rem;
        display: flex;
        flex-wrap: wrap;
        align-items: end;
        gap: 1rem;
    }
    
    /* 底部按鈕容器 */
    .bottom-button-container {
        padding: 0.75rem 1rem;
        display: flex;
    }
    
    .bottom-spacer {
        height: 1.25rem;
        background: #1a1a1a;
    }
    
    /* 卡牌圖片容器 */
    .card-image-container {
        padding: 0.75rem 1rem;
        width: 100%;
    }
    
    .card-image-wrapper {
        width: 100%;
        aspect-ratio: 2/3;
        border-radius: 12px;
        overflow: hidden;
        background: #363636;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* 選擇器容器 */
    .selector-container {
        padding: 1rem;
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        max-width: 480px;
    }
    
    .selector-item {
        flex: 1;
        min-width: 120px;
    }
    
    /* 下拉選單樣式 */
    .stSelectbox > div > div > div {
        background: #363636 !important;
        border: none !important;
        border-radius: 12px !important;
        color: white !important;
        font-size: 16px !important;
        height: 48px !important;
        box-shadow: none !important;
    }
    
    .stSelectbox > div > div > div:focus-within {
        outline: none !important;
        ring: none !important;
        border: none !important;
    }
    
    /* 隱藏標籤 */
    .stTextInput > label,
    .stTextArea > label,
    .stSelectbox > label {
        display: none !important;
    }
    
    /* 響應式設計 */
    @media (min-width: 480px) {
        .card-image-container {
            padding: 0.75rem;
        }
        
        .card-image-wrapper {
            border-radius: 12px;
        }
        
        .input-container {
            padding: 0.75rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def show_welcome_page():
    """顯示歡迎頁面"""
    apply_modern_dark_theme()
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # 上半部分
    st.markdown('<div>', unsafe_allow_html=True)
    
    # 主標題和描述
    st.markdown('<h2 class="page-title">Welcome to Your Tarot Journey</h2>', unsafe_allow_html=True)
    st.markdown('''
    <p class="page-subtitle">
        Embark on a mystical adventure with our tarot app. Uncover insights and guidance from the universe. 
        Enter your question below to begin your reading.
    </p>
    ''', unsafe_allow_html=True)
    
    # 輸入區域
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    question = st.text_input(
        "",
        placeholder="Ask your question",
        label_visibility="collapsed",
        key="welcome_question"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 下半部分
    st.markdown('<div>', unsafe_allow_html=True)
    st.markdown('<div class="bottom-button-container">', unsafe_allow_html=True)
    
    if st.button("Start Reading", key="start_reading"):
        if question.strip():
            st.session_state.question = question
            st.session_state.page = "selector"
            st.rerun()
        else:
            st.error("Please enter your question first")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="bottom-spacer"></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_selector_page():
    """顯示選擇器頁面"""
    apply_modern_dark_theme()
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # 關閉按鈕
    col1, col2, col3 = st.columns([1, 8, 1])
    with col3:
        if st.button("✕", key="close_selector", help="返回首頁"):
            if 'question' in st.session_state:
                del st.session_state.question
            st.session_state.page = "welcome"
            st.rerun()
    
    # 上半部分
    st.markdown('<div>', unsafe_allow_html=True)
    
    st.markdown('<h3 class="page-title">Choose a card</h3>', unsafe_allow_html=True)
    
    # 卡牌圖片區域（可以省略圖片，只顯示占位符）
    st.markdown('''
    <div class="card-image-container">
        <div class="card-image-wrapper">
            <div style="color: #adadad; font-size: 48px;">🔮</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # 選擇區域
    st.markdown('<div class="selector-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        area = st.selectbox(
            "",
            options=['general', 'love', 'career', 'spirituality'],
            format_func=lambda x: {
                'general': '整體指引',
                'love': '愛情關係',
                'career': '事業財富',
                'spirituality': '靈性成長'
            }[x],
            label_visibility="collapsed",
            key="area_selector"
        )
    
    with col2:
        if st.button("Draw Card", key="draw_card"):
            # 進行抽牌和解讀
            with st.spinner("🔮 正在為您抽牌..."):
                selected_card = random.choice(TAROT_DECK)
                question = st.session_state.get('question', '')
                
                interpretation = get_tarot_reading(
                    selected_card['name'],
                    question,
                    selected_card['keywords']
                )
                
                st.session_state.selected_card = selected_card
                st.session_state.interpretation = interpretation
                st.session_state.area = area
                st.session_state.page = "result"
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 下半部分
    st.markdown('<div>', unsafe_allow_html=True)
    st.markdown('<div class="bottom-spacer"></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_result_page():
    """顯示結果頁面"""
    apply_modern_dark_theme()
    
    selected_card = st.session_state.get('selected_card')
    interpretation = st.session_state.get('interpretation')
    
    if not selected_card or not interpretation:
        st.session_state.page = "welcome"
        st.rerun()
        return
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # 關閉按鈕
    col1, col2, col3 = st.columns([1, 8, 1])
    with col3:
        if st.button("✕", key="close_result", help="返回首頁"):
            # 清除所有狀態
            for key in ['question', 'selected_card', 'interpretation', 'area']:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.page = "welcome"
            st.rerun()
    
    # 上半部分
    st.markdown('<div>', unsafe_allow_html=True)
    
    # 卡牌圖片區域
    st.markdown('<div class="card-image-container">', unsafe_allow_html=True)
    
    card_image = load_card_image(selected_card)
    if card_image:
        st.image(card_image, use_container_width=True)
    else:
        st.markdown('''
        <div class="card-image-wrapper">
            <div style="color: white; font-size: 24px; text-align: center;">
                🔮<br>''' + selected_card['name'] + '''
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 卡牌名稱
    st.markdown(f'<h1 class="card-name">{selected_card["name"]}</h1>', unsafe_allow_html=True)
    
    # 解讀內容
    st.markdown(f'''
    <p class="page-subtitle">
        {interpretation}
    </p>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 下半部分
    st.markdown('<div>', unsafe_allow_html=True)
    st.markdown('<div class="bottom-button-container">', unsafe_allow_html=True)
    
    if st.button("Ask a question", key="ask_again"):
        # 清除結果，保留問題，回到選擇頁面
        for key in ['selected_card', 'interpretation']:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.page = "welcome"
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="bottom-spacer"></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    # 初始化頁面狀態
    if 'page' not in st.session_state:
        st.session_state.page = "welcome"
    
    # 根據頁面狀態顯示不同內容
    if st.session_state.page == "welcome":
        show_welcome_page()
    elif st.session_state.page == "selector":
        show_selector_page()
    elif st.session_state.page == "result":
        show_result_page()

if __name__ == "__main__":
    main()
