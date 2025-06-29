import streamlit as st
import requests
import random
import time
import os
from PIL import Image, ImageDraw, ImageFont
import base64

# 頁面配置
st.set_page_config(
    page_title="🔮 AI塔羅占卜",
    page_icon="🔮",
    layout="centered",
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

def get_tarot_reading(card_name, area, question, keywords):
    """使用 DeepSeek API 獲取塔羅解讀"""
    area_names = {
        'love': '愛情與關係',
        'career': '事業與財富',
        'spirituality': '靈性成長',
        'general': '整體生活指引'
    }
    
    system_prompt = """你是一位專業、智慧且充滿洞察力的塔羅占卜師。你擁有深厚的塔羅知識和豐富的人生智慧，能夠為來訪者提供溫暖、實用且具有啟發性的指引。
請用溫暖、專業且易懂的語言進行解讀，避免過於神秘或模糊的表達。重點是提供實用的建議和積極的指引。"""
    
    user_prompt = f"""請為以下塔羅占卜提供深入而有意義的解讀：
【抽到的牌卡】：{card_name}
【牌卡關鍵詞】：{', '.join(keywords)}
【問題領域】：{area_names[area]}
【具體問題】：{question}

請提供一個完整且個人化的塔羅解讀，包含以下要素：
1. **牌卡核心含義**：這張牌在當前情況下的主要象徵意義
2. **針對性指引**：針對提問者的具體問題給出的建議和洞察
3. **行動建議**：實際可行的行動方向或需要注意的事項  
4. **正面展望**：鼓勵性的訊息和未來的可能性

請用親切、專業的語調，字數控制在 300-500 字之間。重點是幫助提問者獲得清晰的指引和內心的平靜。"""
    
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
            'max_tokens': 800,
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
            return get_fallback_reading(card_name, area, question, keywords)
            
    except Exception as e:
        return get_fallback_reading(card_name, area, question, keywords)

def get_fallback_reading(card_name, area, question, keywords):
    """備用解讀"""
    fallback_interpretations = {
        'love': f"{card_name}在愛情方面為您帶來{', '.join(keywords)}的訊息。這張牌提醒您在感情中要保持開放的心態，相信直覺的指引。針對您的問題「{question}」，建議您多關注內心的聲音，勇敢表達真實的感受。感情需要時間培養，請保持耐心和真誠。",
        'career': f"{card_name}在事業領域象徵著{', '.join(keywords)}。現在是重新評估職業方向的好時機，專注於發揮您的核心優勢。針對您的問題「{question}」，這張牌建議您要相信自己的能力，勇敢面對職場挑戰。成功需要堅持和智慧的結合。",
        'spirituality': f"{card_name}在靈性成長上指向{', '.join(keywords)}。這是一個深入內省、連接內在智慧的重要時期。針對您的問題「{question}」，建議您多花時間靜心冥想，聆聽內心的聲音。靈性成長是一個漸進的過程，請保持開放和耐心。",
        'general': f"{card_name}為您帶來關於{', '.join(keywords)}的重要訊息。針對您的問題「{question}」，相信您內在的力量，勇敢面對當前的挑戰和機會。這張牌提醒您保持積極的心態，一切都會朝好的方向發展。記住，您擁有改變現狀的能力。"
    }
    return fallback_interpretations.get(area, fallback_interpretations['general'])

def create_stars_background():
    """創建星空背景動畫"""
    return """
    <div class="stars"></div>
    <div class="stars2"></div>
    <div class="stars3"></div>
    """

def apply_dark_mystical_theme():
    """應用黑色神秘主題"""
    st.markdown("""
    <style>
    /* 隱藏 Streamlit 預設元素 */
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        background: transparent;
    }
    
    /* 主背景 */
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
        min-height: 100vh;
        position: relative;
        overflow-x: hidden;
    }
    
    /* 星空動畫 */
    .stars, .stars2, .stars3 {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
    }
    
    .stars {
        background: transparent url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="1" fill="white" opacity="0.8"/><circle cx="80" cy="40" r="0.5" fill="white" opacity="0.6"/><circle cx="40" cy="70" r="1" fill="white" opacity="0.8"/><circle cx="90" cy="10" r="0.5" fill="white" opacity="0.7"/><circle cx="10" cy="90" r="0.8" fill="white" opacity="0.5"/></svg>') repeat;
        animation: move-stars 50s linear infinite;
    }
    
    .stars2 {
        background: transparent url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="30" cy="30" r="0.5" fill="white" opacity="0.7"/><circle cx="70" cy="70" r="1" fill="white" opacity="0.5"/><circle cx="50" cy="10" r="0.8" fill="white" opacity="0.6"/></svg>') repeat;
        animation: move-stars 100s linear infinite;
    }
    
    .stars3 {
        background: transparent url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="60" cy="20" r="0.3" fill="white" opacity="0.8"/><circle cx="25" cy="80" r="0.6" fill="white" opacity="0.4"/><circle cx="85" cy="60" r="0.4" fill="white" opacity="0.7"/></svg>') repeat;
        animation: move-stars 150s linear infinite;
    }
    
    @keyframes move-stars {
        from { transform: translateY(0px); }
        to { transform: translateY(-100vh); }
    }
    
    /* 主標題 */
    .main-title {
        text-align: center;
        color: #e6e6fa;
        font-size: 3.5rem;
        font-weight: 300;
        margin: 2rem 0;
        text-shadow: 0 0 20px rgba(230, 230, 250, 0.5);
        letter-spacing: 3px;
    }
    
    .subtitle {
        text-align: center;
        color: #9370db;
        font-size: 1.3rem;
        margin-bottom: 3rem;
        font-weight: 300;
        text-shadow: 0 0 10px rgba(147, 112, 219, 0.3);
    }
    
    /* 輸入區域 */
    .stTextArea > div > div > textarea {
        background: rgba(0, 0, 0, 0.7) !important;
        border: 2px solid #483d8b !important;
        border-radius: 15px !important;
        color: #e6e6fa !important;
        font-size: 1.1rem !important;
        padding: 1rem !important;
        box-shadow: 0 0 20px rgba(72, 61, 139, 0.3) !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #9370db !important;
        box-shadow: 0 0 30px rgba(147, 112, 219, 0.5) !important;
    }
    
    .stSelectbox > div > div > div {
        background: rgba(0, 0, 0, 0.7) !important;
        border: 2px solid #483d8b !important;
        border-radius: 15px !important;
        color: #e6e6fa !important;
    }
    
    /* 按鈕 */
    .stButton > button {
        background: linear-gradient(45deg, #483d8b, #9370db) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.8rem 3rem !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        box-shadow: 0 10px 30px rgba(147, 112, 219, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 40px rgba(147, 112, 219, 0.6) !important;
    }
    
    /* 卡牌顯示區域 */
    .card-reveal {
        background: rgba(0, 0, 0, 0.8);
        border: 3px solid #9370db;
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 0 40px rgba(147, 112, 219, 0.4);
        animation: cardAppear 1s ease-out;
    }
    
    @keyframes cardAppear {
        from {
            opacity: 0;
            transform: scale(0.8) rotateY(-180deg);
        }
        to {
            opacity: 1;
            transform: scale(1) rotateY(0deg);
        }
    }
    
    .card-name {
        color: #e6e6fa;
        font-size: 3rem;
        font-weight: 300;
        margin: 1rem 0;
        text-shadow: 0 0 20px rgba(230, 230, 250, 0.5);
    }
    
    .card-keywords {
        color: #dda0dd;
        font-size: 1.3rem;
        margin: 1rem 0;
        font-style: italic;
    }
    
    /* 解讀區域 */
    .interpretation-box {
        background: rgba(16, 16, 48, 0.9);
        border: 2px solid #6a5acd;
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 0 30px rgba(106, 90, 205, 0.3);
        animation: fadeInUp 1s ease-out 0.5s both;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .interpretation-title {
        color: #dda0dd;
        font-size: 1.8rem;
        font-weight: 400;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .interpretation-text {
        color: #e6e6fa;
        font-size: 1.1rem;
        line-height: 1.8;
        text-align: justify;
    }
    
    /* 載入動畫 */
    .loading-mystical {
        text-align: center;
        padding: 3rem;
        color: #9370db;
        font-size: 1.5rem;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.6; }
        50% { opacity: 1; }
    }
    
    /* 隱藏不必要元素 */
    .stProgress > div > div {
        background: linear-gradient(90deg, #483d8b, #9370db) !important;
        border-radius: 10px !important;
    }
    
    /* 標籤 */
    label {
        color: #dda0dd !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
    }
    
    /* 過場動畫 */
    .transition-screen {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 100%);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        z-index: 1000;
        animation: fadeOut 1s ease-out 3s both;
    }
    
    .transition-text {
        color: #9370db;
        font-size: 2rem;
        text-align: center;
        margin: 1rem 0;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 20px rgba(147, 112, 219, 0.5); }
        to { text-shadow: 0 0 30px rgba(147, 112, 219, 0.8); }
    }
    
    @keyframes fadeOut {
        to { opacity: 0; pointer-events: none; }
    }
    </style>
    """, unsafe_allow_html=True)

def show_question_page():
    """顯示問題輸入頁面"""
    apply_dark_mystical_theme()
    
    # 星空背景
    st.markdown(create_stars_background(), unsafe_allow_html=True)
    
    # 主標題
    st.markdown('<h1 class="main-title">🔮 塔羅神諭</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">✨ 探尋命運的指引，聆聽宇宙的智慧 ✨</p>', unsafe_allow_html=True)
    
    # 輸入區域
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 💭 向宇宙提出您的問題")
        question = st.text_area(
            "",
            placeholder="在星空下，靜心思考您最想了解的問題...",
            height=120,
            label_visibility="collapsed"
        )
        
        st.markdown("### 🌟 選擇問題的領域")
        area = st.selectbox(
            "",
            options=['general', 'love', 'career', 'spirituality'],
            format_func=lambda x: {
                'general': '🌌 整體生活指引',
                'love': '💜 愛情與關係', 
                'career': '⭐ 事業與財富',
                'spirituality': '🔮 靈性成長'
            }[x],
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🌙 開始神聖占卜", type="primary", use_container_width=True):
            if not question.strip():
                st.error("🌟 請先向宇宙傾訴您的問題")
                return
            
            # 儲存到 session state
            st.session_state.question = question
            st.session_state.area = area
            st.session_state.page = "result"
            st.rerun()

def show_transition():
    """顯示過場動畫"""
    st.markdown("""
    <div class="transition-screen">
        <div class="transition-text">🌟 星辰正在排列</div>
        <div class="transition-text">🔮 命運之牌即將顯現</div>
        <div class="transition-text">✨ 請靜心接收宇宙的訊息</div>
    </div>
    """, unsafe_allow_html=True)

def show_result_page():
    """顯示結果頁面"""
    apply_dark_mystical_theme()
    
    # 星空背景
    st.markdown(create_stars_background(), unsafe_allow_html=True)
    
    question = st.session_state.get('question', '')
    area = st.session_state.get('area', 'general')
    
    # 過場動畫
    if 'result_shown' not in st.session_state:
        show_transition()
        
        with st.spinner(""):
            # 抽牌
            selected_card = random.choice(TAROT_DECK)
            st.session_state.selected_card = selected_card
            
            # 載入AI解讀
            interpretation = get_tarot_reading(
                selected_card['name'],
                area,
                question,
                selected_card['keywords']
            )
            st.session_state.interpretation = interpretation
            st.session_state.result_shown = True
            
            time.sleep(3)  # 等待過場動畫
            st.rerun()
    
    else:
        selected_card = st.session_state.selected_card
        interpretation = st.session_state.interpretation
        
        # 顯示結果
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # 卡牌顯示
            st.markdown(f"""
            <div class="card-reveal">
                <div style="font-size: 2rem; margin-bottom: 1rem;">✨ 您的命運之牌 ✨</div>
                <div class="card-name">{selected_card['name']}</div>
                <div class="card-keywords">🔑 {' • '.join(selected_card['keywords'])}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 顯示卡牌圖片（如果存在）
            card_image = load_card_image(selected_card)
            if card_image:
                st.image(card_image, use_container_width=True)
            
            # 解讀結果
            st.markdown(f"""
            <div class="interpretation-box">
                <div class="interpretation-title">🔮 宇宙的神諭</div>
                <div class="interpretation-text">{interpretation}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 操作按鈕
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🌙 重新占卜", type="secondary", use_container_width=True):
                    # 清除結果，回到問題頁面
                    for key in ['selected_card', 'interpretation', 'result_shown']:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.session_state.page = "question"
                    st.rerun()
            
            with col_b:
                if st.button("🔮 新的問題", type="primary", use_container_width=True):
                    # 清除所有狀態
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.session_state.page = "question"
                    st.rerun()

def main():
    # 初始化頁面狀態
    if 'page' not in st.session_state:
        st.session_state.page = "question"
    
    # 根據頁面狀態顯示不同內容
    if st.session_state.page == "question":
        show_question_page()
    elif st.session_state.page == "result":
        show_result_page()

if __name__ == "__main__":
    main()
