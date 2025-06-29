import streamlit as st
import requests
import random
import time
import os
from PIL import Image
import base64

# 頁面配置
st.set_page_config(
    page_title="🔮 AI塔羅占卜",
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

def apply_original_styles():
    """應用與原始網站完全相同的樣式"""
    st.markdown("""
    <style>
    /* 隱藏 Streamlit 預設元素 */
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        min-height: 100vh;
        font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
    }
    
    /* 完全隱藏 Streamlit 的 header 和 footer */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    .stDeployButton {
        display: none !important;
    }
    
    /* 主容器 */
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    /* 主標題 */
    .main-title {
        text-align: center;
        color: white;
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        letter-spacing: 2px;
    }
    
    .subtitle {
        text-align: center;
        color: rgba(255,255,255,0.9);
        font-size: 1.4rem;
        margin-bottom: 3rem;
        font-weight: 300;
    }
    
    /* 主要內容區域 */
    .content-area {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 3rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
        margin: 0 auto;
        max-width: 800px;
        width: 100%;
    }
    
    /* 表單樣式 */
    .form-section {
        margin-bottom: 2rem;
    }
    
    .form-label {
        font-size: 1.2rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 0.8rem;
        display: block;
    }
    
    /* 文字輸入區域 */
    .stTextArea > div > div > textarea {
        border: 2px solid #e0e0e0 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        background: white !important;
        color: #333 !important;
        min-height: 120px !important;
        resize: vertical !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
        outline: none !important;
    }
    
    /* 下拉選單 */
    .stSelectbox > div > div > div {
        border: 2px solid #e0e0e0 !important;
        border-radius: 12px !important;
        background: white !important;
        color: #333 !important;
        font-size: 1rem !important;
        padding: 0.5rem !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }
    
    .stSelectbox > div > div > div:focus-within {
        border-color: #667eea !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* 按鈕樣式 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 1rem 3rem !important;
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        text-transform: none !important;
        letter-spacing: 1px !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin-top: 1rem !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.5) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* 卡牌顯示區域 */
    .card-container {
        text-align: center;
        margin: 2rem 0;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .card-title {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 1rem;
    }
    
    .card-name {
        font-size: 2.5rem;
        font-weight: 600;
        color: #333;
        margin: 1rem 0;
    }
    
    .card-keywords {
        font-size: 1.2rem;
        color: #666;
        font-style: italic;
        margin-bottom: 1.5rem;
    }
    
    .card-image {
        max-width: 300px;
        margin: 1rem auto;
        border-radius: 10px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    /* 解讀結果區域 */
    .interpretation-container {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        border-left: 5px solid #667eea;
    }
    
    .interpretation-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .interpretation-text {
        font-size: 1.1rem;
        line-height: 1.8;
        color: #444;
        text-align: justify;
    }
    
    /* 載入動畫 */
    .loading-container {
        text-align: center;
        padding: 3rem;
        color: #667eea;
        font-size: 1.3rem;
    }
    
    .loading-spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #667eea;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 0 auto 1rem;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* 響應式設計 */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
        }
        
        .content-area {
            padding: 2rem 1.5rem;
            margin: 0 1rem;
        }
        
        .card-image {
            max-width: 250px;
        }
    }
    
    /* 隱藏標籤 */
    .stTextArea > label,
    .stSelectbox > label {
        display: none !important;
    }
    
    /* 進度條 */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
        border-radius: 10px !important;
        height: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    # 應用原始樣式
    apply_original_styles()
    
    # 主容器
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # 主標題
    st.markdown('<h1 class="main-title">🔮 AI塔羅占卜</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">✨ 探索內心智慧，獲得人生指引 ✨</p>', unsafe_allow_html=True)
    
    # 主要內容區域
    st.markdown('<div class="content-area">', unsafe_allow_html=True)
    
    # 表單區域
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<label class="form-label">💭 請輸入您想詢問的問題</label>', unsafe_allow_html=True)
        question = st.text_area(
            "",
            placeholder="例如：我在工作上遇到困難，應該如何處理？",
            height=120,
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<label class="form-label">🎯 選擇問題領域</label>', unsafe_allow_html=True)
        area = st.selectbox(
            "",
            options=['general', 'love', 'career', 'spirituality'],
            format_func=lambda x: {
                'general': '整體生活指引',
                'love': '愛情與關係',
                'career': '事業與財富',
                'spirituality': '靈性成長'
            }[x],
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 占卜按鈕
    if st.button("🔮 開始占卜", type="primary"):
        if not question.strip():
            st.error("請輸入您的問題後再開始占卜")
        else:
            # 載入動畫
            with st.container():
                st.markdown("""
                <div class="loading-container">
                    <div class="loading-spinner"></div>
                    <div>🌟 正在為您抽牌並解讀...</div>
                </div>
                """, unsafe_allow_html=True)
                
                # 進度條
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.02)
                    progress_bar.progress(i + 1)
                progress_bar.empty()
            
            # 清除載入動畫
            st.empty()
            
            # 抽牌
            selected_card = random.choice(TAROT_DECK)
            
            # 顯示卡牌結果
            st.markdown(f"""
            <div class="card-container">
                <div class="card-title">✨ 您抽到的牌卡 ✨</div>
                <div class="card-name">{selected_card['name']}</div>
                <div class="card-keywords">🔑 關鍵詞：{' • '.join(selected_card['keywords'])}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 顯示卡牌圖片
            card_image = load_card_image(selected_card)
            if card_image:
                col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
                with col_img2:
                    st.image(card_image, use_container_width=True)
            
            # 獲取 AI 解讀
            with st.spinner("🤖 AI 正在為您解讀..."):
                interpretation = get_tarot_reading(
                    selected_card['name'],
                    area,
                    question,
                    selected_card['keywords']
                )
            
            # 顯示解讀結果
            st.markdown(f"""
            <div class="interpretation-container">
                <div class="interpretation-title">🔮 您的塔羅解讀</div>
                <div class="interpretation-text">{interpretation}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 重新占卜按鈕
            if st.button("🔄 重新占卜", type="secondary"):
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)  # 結束 content-area
    st.markdown('</div>', unsafe_allow_html=True)  # 結束 main-container

if __name__ == "__main__":
    main()
