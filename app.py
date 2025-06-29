import streamlit as st
import requests
import random
import time
import os
from PIL import Image, ImageDraw, ImageFont
from streamlit_lottie import st_lottie

# 頁面配置
st.set_page_config(
    page_title="🔮 AI塔羅占卜",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 塔羅牌資料 - 直接從您的 JavaScript 轉換
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

def load_lottieurl(url):
    """載入 Lottie 動畫"""
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def create_card_placeholder(card_name, keywords):
    """創建美觀的文字卡牌"""
    width, height = 300, 450
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    
    # 漸變背景
    for y in range(height):
        ratio = y / height
        r = int(102 + (118 - 102) * ratio)  # 紫色漸變
        g = int(70 + (162 - 70) * ratio)
        b = int(193 + (234 - 193) * ratio)
        color = (r, g, b)
        draw.line([(0, y), (width, y)], fill=color)
    
    # 邊框
    draw.rectangle([10, 10, width-10, height-10], outline='#FFFFFF', width=3)
    
    # 文字 (使用預設字體)
    font_large = ImageFont.load_default()
    font_small = ImageFont.load_default()
    
    # 卡牌名稱
    text_bbox = draw.textbbox((0, 0), card_name, font=font_large)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (width - text_width) // 2
    
    draw.text((text_x, 80), card_name, fill='white', font=font_large)
    draw.text((width//2 - 20, height//2 - 20), '🔮', fill='white')
    
    # 關鍵詞
    keywords_text = ' • '.join(keywords[:2])
    draw.text((30, height-80), keywords_text, fill='white', font=font_small)
    
    return image

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
    
    # 如果找不到圖片，創建文字卡牌
    return create_card_placeholder(card['name'], card['keywords'])

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
        # 從 secrets 讀取 API 金鑰
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
        st.error(f"API 呼叫錯誤，使用備用解讀")
        return get_fallback_reading(card_name, area, question, keywords)

def get_fallback_reading(card_name, area, question, keywords):
    """備用解讀"""
    area_names = {
        'love': '愛情與關係',
        'career': '事業與財富', 
        'spirituality': '靈性成長',
        'general': '整體生活指引'
    }
    
    fallback_interpretations = {
        'love': f"{card_name}在愛情方面為您帶來{', '.join(keywords)}的訊息。這張牌提醒您在感情中要保持開放的心態，相信直覺的指引。針對您的問題「{question}」，建議您多關注內心的聲音，勇敢表達真實的感受。感情需要時間培養，請保持耐心和真誠。",
        
        'career': f"{card_name}在事業領域象徵著{', '.join(keywords)}。現在是重新評估職業方向的好時機，專注於發揮您的核心優勢。針對您的問題「{question}」，這張牌建議您要相信自己的能力，勇敢面對職場挑戰。成功需要堅持和智慧的結合。",
        
        'spirituality': f"{card_name}在靈性成長上指向{', '.join(keywords)}。這是一個深入內省、連接內在智慧的重要時期。針對您的問題「{question}」，建議您多花時間靜心冥想，聆聽內心的聲音。靈性成長是一個漸進的過程，請保持開放和耐心。",
        
        'general': f"{card_name}為您帶來關於{', '.join(keywords)}的重要訊息。針對您的問題「{question}」，相信您內在的力量，勇敢面對當前的挑戰和機會。這張牌提醒您保持積極的心態，一切都會朝好的方向發展。記住，您擁有改變現狀的能力。"
    }
    
    return fallback_interpretations.get(area, fallback_interpretations['general'])

def main():
    # 自定義 CSS
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { filter: brightness(100%); }
        to { filter: brightness(150%); }
    }
    
    .card-display {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
        margin: 2rem 0;
        animation: fadeIn 1s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .interpretation {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #6B46C1;
        margin: 1rem 0;
        animation: slideIn 1s ease-out;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 主標題
    st.markdown('<h1 class="main-header">🔮 AI塔羅占卜</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #64748b; font-size: 1.2rem;">✨ 探索內心智慧，獲得人生指引 ✨</p>', unsafe_allow_html=True)
    
    # Lottie 動畫
    lottie_magic = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_kkflmtur.json")
    if lottie_magic:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st_lottie(lottie_magic, height=200, key="magic")
    
    st.divider()
    
    # 輸入區域
    col1, col2 = st.columns([2, 1])
    
    with col1:
        question = st.text_area(
            "💭 請輸入您想詢問的問題",
            placeholder="例如：我在工作上遇到困難，應該如何處理？",
            height=100
        )
    
    with col2:
        area = st.selectbox(
            "🎯 選擇問題領域",
            options=['general', 'love', 'career', 'spirituality'],
            format_func=lambda x: {
                'general': '整體生活指引',
                'love': '愛情與關係',
                'career': '事業與財富',
                'spirituality': '靈性成長'
            }[x]
        )
    
    # 占卜按鈕
    if st.button("🔮 開始占卜", type="primary", use_container_width=True):
        if not question.strip():
            st.error("請輸入您的問題後再開始占卜")
            return
        
        with st.spinner("🌟 正在為您抽牌並解讀..."):
            # 進度條動畫
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.02)
                progress_bar.progress(i + 1)
            progress_bar.empty()
            
            # 隨機抽牌
            selected_card = random.choice(TAROT_DECK)
            
            # 顯示抽到的牌
            st.markdown(f"""
            <div class="card-display">
                <h2>✨ 您抽到的牌卡 ✨</h2>
                <h1>{selected_card['name']}</h1>
                <p style="font-size: 1.2rem; margin-top: 1rem;">
                    🔑 關鍵詞：{' • '.join(selected_card['keywords'])}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # 顯示卡牌圖片
            card_image = load_card_image(selected_card)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
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
            <div class="interpretation">
                <h3>🔮 您的塔羅解讀</h3>
                <p style="line-height: 1.8; font-size: 1.1rem;">{interpretation}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 重新占卜按鈕
            if st.button("🔄 重新占卜", type="secondary"):
                st.rerun()

    # 側邊欄資訊
    with st.sidebar:
        st.header("🔮 關於塔羅占卜")
        st.write("""
        塔羅占卜是一種古老的占卜方式，通過22張大阿卡納牌來獲得內在的智慧和指引。
        
        **如何使用**：
        1. 在心中專注於您的問題
        2. 選擇問題的領域
        3. 點擊開始占卜
        4. 仔細閱讀解讀內容
        
        **提醒**：塔羅占卜是一種自我反思的工具，請以開放的心態對待解讀結果。
        """)

if __name__ == "__main__":
    main()
