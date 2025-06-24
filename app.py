# CryptoLearn Pro - Professional Streamlit App
# Created for GitHub repo: cryptokunta/cryptolearnpro

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
from datetime import datetime
import time
import random

# Configure page FIRST - before any other Streamlit commands
st.set_page_config(
    page_title="CryptoLearn Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/cryptokunta/cryptolearnpro',
        'Report a bug': "https://github.com/cryptokunta/cryptolearnpro/issues",
        'About': "# CryptoLearn Pro\nMaster Crypto & Memecoin Terminology!"
    }
)

# Custom CSS for professional UI/UX
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.2);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .term-card {
        background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%);
        border-left: 5px solid #667eea;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .term-card:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.15);
    }
    
    .memecoin-badge {
        background: linear-gradient(90deg, #ff6b6b, #feca57);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .crypto-badge {
        background: linear-gradient(90deg, #4ecdc4, #45b7d1);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .price-up {
        color: #00ff88;
        font-weight: bold;
    }
    
    .price-down {
        color: #ff4757;
        font-weight: bold;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    .quiz-correct {
        background: linear-gradient(90deg, #00ff88, #00d4aa);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .quiz-incorrect {
        background: linear-gradient(90deg, #ff4757, #ff3742);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .feature-box {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin: 1rem 0;
        border: 1px solid #e9ecef;
    }
</style>
""", unsafe_allow_html=True)

# Comprehensive crypto terms database
@st.cache_data
def load_crypto_terms():
    terms_data = [
        # Blockchain Fundamentals
        {
            "term": "Blockchain",
            "definition": "A decentralized, secure ledger of transactions shared across multiple computers in a network.",
            "example": "Bitcoin uses a blockchain to record every transaction publicly and immutably.",
            "category": "Blockchain",
            "difficulty": "Beginner",
            "tags": ["fundamental", "technology", "ledger"]
        },
        {
            "term": "Smart Contract",
            "definition": "Self-executing contracts with terms directly written into code, automatically enforcing agreements.",
            "example": "Ethereum smart contracts automatically execute when predetermined conditions are met.",
            "category": "Blockchain",
            "difficulty": "Intermediate",
            "tags": ["ethereum", "automation", "programming"]
        },
        {
            "term": "Consensus Mechanism",
            "definition": "The method by which blockchain networks agree on the validity of transactions and maintain network integrity.",
            "example": "Bitcoin uses Proof of Work, while Ethereum 2.0 uses Proof of Stake as consensus mechanisms.",
            "category": "Blockchain",
            "difficulty": "Intermediate",
            "tags": ["validation", "network", "security"]
        },
        
        # Memecoin Culture & Slang
        {
            "term": "Diamond Hands",
            "definition": "Investors who hold cryptocurrency through extreme volatility, refusing to sell despite market crashes or fear.",
            "example": "Even when DOGE dropped 70%, the diamond hands community kept holding. 💎🙌",
            "category": "Memecoins",
            "difficulty": "Beginner",
            "tags": ["culture", "holding", "community", "resilience"]
        },
        {
            "term": "Paper Hands",
            "definition": "Investors who sell quickly at the first sign of trouble or small profits, opposite of diamond hands.",
            "example": "Don't be paper hands - HODL through the dip! 📄🙌",
            "category": "Memecoins",
            "difficulty": "Beginner",
            "tags": ["culture", "selling", "weak", "fear"]
        },
        {
            "term": "To the Moon",
            "definition": "Expression indicating belief that a cryptocurrency's price will rise dramatically to very high levels.",
            "example": "DOGE to the moon! 🚀🌙 The community rallied behind this rallying cry.",
            "category": "Memecoins",
            "difficulty": "Beginner",
            "tags": ["bullish", "optimism", "price", "rally"]
        },
        {
            "term": "Ape In",
            "definition": "To invest heavily and quickly into a cryptocurrency without thorough research, often driven by FOMO.",
            "example": "I'm going to ape in to this new memecoin before it pumps to 100x!",
            "category": "Memecoins",
            "difficulty": "Beginner",
            "tags": ["impulsive", "fomo", "risky", "quick"]
        },
        {
            "term": "Rugpull",
            "definition": "A scam where developers abandon a project and steal investors' money by removing liquidity from trading pools.",
            "example": "The new memecoin turned out to be a rugpull - the devs disappeared overnight with $2M.",
            "category": "Memecoins",
            "difficulty": "Intermediate",
            "tags": ["scam", "danger", "liquidity", "fraud"]
        },
        {
            "term": "WAGMI",
            "definition": "We're All Gonna Make It - an optimistic phrase used in crypto communities to encourage holding through tough times.",
            "example": "Even though we're down 50% this month, WAGMI! 💎🙌",
            "category": "Memecoins",
            "difficulty": "Beginner",
            "tags": ["optimism", "community", "motivation", "belief"]
        },
        {
            "term": "NGMI",
            "definition": "Not Gonna Make It - used to describe someone making poor investment decisions or lacking conviction.",
            "example": "Selling at a 20% loss during a temporary dip? That's NGMI behavior.",
            "category": "Memecoins",
            "difficulty": "Beginner",
            "tags": ["pessimism", "poor_decisions", "criticism"]
        },
        {
            "term": "Degen",
            "definition": "Short for 'degenerate gambler' - someone who makes high-risk cryptocurrency investments with little research.",
            "example": "Only a true degen would invest their entire life savings in a memecoin with no utility.",
            "category": "Memecoins",
            "difficulty": "Intermediate",
            "tags": ["risky", "gambling", "culture", "extreme"]
        },
        {
            "term": "Shilling",
            "definition": "Aggressively promoting a cryptocurrency for personal gain, especially on social media platforms.",
            "example": "Stop shilling that memecoin on Twitter - it's clearly a pump and dump scheme!",
            "category": "Memecoins",
            "difficulty": "Beginner",
            "tags": ["promotion", "manipulation", "social_media"]
        },
        
        # Trading & Market Terms
        {
            "term": "HODL",
            "definition": "Hold On for Dear Life - a strategy of holding cryptocurrency long-term despite market volatility.",
            "example": "Many Bitcoin investors choose to HODL through multiple market cycles for maximum gains.",
            "category": "Trading",
            "difficulty": "Beginner",
            "tags": ["strategy", "long_term", "patience"]
        },
        {
            "term": "FOMO",
            "definition": "Fear of Missing Out - the anxiety that leads to impulsive buying when seeing others profit from investments.",
            "example": "FOMO drove me to buy the memecoin at its all-time high price, and now I'm down 80%.",
            "category": "Psychology",
            "difficulty": "Beginner",
            "tags": ["emotion", "buying", "psychology"]
        },
        {
            "term": "FUD",
            "definition": "Fear, Uncertainty, and Doubt - negative information spread to damage a cryptocurrency's reputation and price.",
            "example": "Don't listen to the FUD about this project - the fundamentals are still strong!",
            "category": "Psychology",
            "difficulty": "Beginner",
            "tags": ["negativity", "manipulation", "market"]
        },
        {
            "term": "Whale",
            "definition": "An individual or entity that holds large amounts of cryptocurrency and can influence market prices with their trades.",
            "example": "A Bitcoin whale just moved 10,000 BTC to an exchange, causing market panic.",
            "category": "Trading",
            "difficulty": "Beginner",
            "tags": ["large_holder", "market_impact", "influence"]
        },
        {
            "term": "Pump and Dump",
            "definition": "An illegal scheme where the price of an asset is artificially inflated (pumped) then sold off (dumped) for profit.",
            "example": "That memecoin was clearly a pump and dump - it went up 1000% then crashed 95% in one day.",
            "category": "Trading",
            "difficulty": "Intermediate",
            "tags": ["scam", "manipulation", "illegal"]
        },
        
        # DeFi & Technical
        {
            "term": "DeFi",
            "definition": "Decentralized Finance - an ecosystem of financial applications built on blockchain technology without traditional intermediaries.",
            "example": "DeFi platforms like Uniswap allow users to trade tokens without centralized exchanges.",
            "category": "DeFi",
            "difficulty": "Intermediate",
            "tags": ["finance", "decentralized", "applications"]
        },
        {
            "term": "Yield Farming",
            "definition": "A DeFi strategy of earning rewards by providing liquidity to decentralized protocols and earning tokens in return.",
            "example": "Yield farming on Compound can provide 15% APY but comes with smart contract risks.",
            "category": "DeFi",
            "difficulty": "Advanced",
            "tags": ["farming", "rewards", "liquidity", "apy"]
        },
        {
            "term": "Staking",
            "definition": "Locking up cryptocurrency to support network operations (like validation) and earn rewards in return.",
            "example": "I'm staking my ETH in Ethereum 2.0 to earn approximately 5% annual rewards.",
            "category": "DeFi",
            "difficulty": "Intermediate",
            "tags": ["rewards", "network", "validation"]
        },
        {
            "term": "Gas Fees",
            "definition": "Transaction fees paid to blockchain miners or validators for processing and confirming transactions.",
            "example": "Ethereum gas fees can spike to $100+ during network congestion, making small transactions uneconomical.",
            "category": "Technical",
            "difficulty": "Beginner",
            "tags": ["fees", "transaction", "network"]
        },
        {
            "term": "Private Key",
            "definition": "A secret cryptographic key that gives you complete control over your cryptocurrency funds - must be kept secure.",
            "example": "Never share your private key - 'Not your keys, not your coins' is a fundamental crypto principle.",
            "category": "Security",
            "difficulty": "Beginner",
            "tags": ["security", "wallet", "control"]
        },
        
        # NFTs & Gaming
        {
            "term": "NFT",
            "definition": "Non-Fungible Token - unique digital assets verified using blockchain technology, often representing art or collectibles.",
            "example": "The Bored Ape Yacht Club NFTs became status symbols, with some selling for millions of dollars.",
            "category": "NFTs",
            "difficulty": "Beginner",
            "tags": ["unique", "digital", "collectible"]
        },
        {
            "term": "Minting",
            "definition": "The process of creating new tokens or NFTs on a blockchain network, often the first sale by creators.",
            "example": "The new NFT collection will start minting tomorrow at 0.08 ETH per piece.",
            "category": "NFTs",
            "difficulty": "Intermediate",
            "tags": ["creation", "new", "blockchain"]
        }
    ]
    return pd.DataFrame(terms_data)

# API Functions with error handling
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_live_prices():
    """Fetch live prices for popular memecoins and cryptocurrencies"""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': 'bitcoin,ethereum,dogecoin,shiba-inu,pepe,floki,bonk,chainlink,cardano,solana',
            'vs_currencies': 'usd',
            'include_24hr_change': 'true',
            'include_market_cap': 'true',
            'include_24hr_vol': 'true'
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
    except requests.exceptions.Timeout:
        st.error("⏰ Request timed out. The API might be slow.")
    except requests.exceptions.RequestException as e:
        st.error(f"🌐 Network error: {str(e)}")
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
    return None

@st.cache_data(ttl=600)  # Cache for 10 minutes  
def fetch_trending():
    """Fetch trending cryptocurrencies"""
    try:
        url = "https://api.coingecko.com/api/v3/search/trending"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Trending API Error: {response.status_code}")
    except Exception as e:
        st.error(f"❌ Error fetching trending data: {str(e)}")
    return None

# Initialize session state for quiz
def init_session_state():
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0
    if 'quiz_total' not in st.session_state:
        st.session_state.quiz_total = 0
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'quiz_answered' not in st.session_state:
        st.session_state.quiz_answered = False
    if 'user_progress' not in st.session_state:
        st.session_state.user_progress = {
            'terms_learned': set(),
            'categories_explored': set(),
            'quiz_streak': 0
        }

# Load data
df = load_crypto_terms()
init_session_state()

# Header
st.markdown("""
<div class="main-header">
    <h1>🚀 CryptoLearn Pro</h1>
    <h3>Master Crypto & Memecoin Terminology with Interactive Learning</h3>
    <p>🎯 Learn • 📈 Track • 🎮 Practice • 🌟 Master • 🚀 Succeed</p>
    <p style="font-size: 0.9rem; opacity: 0.9;">From blockchain basics to memecoin madness - become a crypto expert!</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation & Stats
st.sidebar.markdown("### 🧭 Navigation Hub")
page = st.sidebar.selectbox(
    "Choose Your Learning Adventure:",
    [
        "🏠 Dashboard", 
        "🔍 Term Explorer", 
        "📊 Live Market Data", 
        "🎯 Interactive Quiz", 
        "📚 Study Guide", 
        "🎲 Discovery Mode",
        "➕ Contribute Terms",
        "📈 Progress Tracker"
    ]
)

# Sidebar Quick Stats
st.sidebar.markdown("### 📊 Quick Stats")
total_terms = len(df)
categories = df['category'].nunique()
difficulties = df['difficulty'].nunique()
memecoins = len(df[df['category'] == 'Memecoins'])

col1, col2 = st.sidebar.columns(2)
with col1:
    st.metric("📚 Terms", total_terms)
    st.metric("🐕 Memecoins", memecoins)
with col2:
    st.metric("📂 Categories", categories)
    st.metric("⭐ Levels", difficulties)

# User Progress
st.sidebar.markdown("### 🎯 Your Progress")
progress_percentage = (len(st.session_state.user_progress['terms_learned']) / total_terms) * 100
st.sidebar.progress(progress_percentage / 100)
st.sidebar.caption(f"Learned: {len(st.session_state.user_progress['terms_learned'])}/{total_terms} terms ({progress_percentage:.1f}%)")

if st.session_state.quiz_total > 0:
    accuracy = (st.session_state.quiz_score / st.session_state.quiz_total) * 100
    st.sidebar.metric("🎯 Quiz Accuracy", f"{accuracy:.1f}%")

# Main Content Based on Page Selection
if page == "🏠 Dashboard":
    # Quick Stats Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📚 Total Terms</h3>
            <h1>{total_terms}</h1>
            <p>Learn them all!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🐕 Memecoins</h3>
            <h1>{memecoins}</h1>
            <p>Degen knowledge</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🔥 Categories</h3>
            <h1>{categories}</h1>
            <p>Diverse topics</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        user_learned = len(st.session_state.user_progress['terms_learned'])
        st.markdown(f"""
        <div class="metric-card">
            <h3>🎯 Your Progress</h3>
            <h1>{user_learned}</h1>
            <p>Terms mastered</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Feature Boxes
    st.markdown("### 🌟 Platform Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h3>🔍 Smart Search</h3>
            <p>Find any crypto term instantly with our intelligent search engine. Filter by category, difficulty, or tags.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h3>📈 Live Data</h3>
            <p>Real-time prices, trending coins, and market data from CoinGecko API. Stay updated with the latest crypto movements.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-box">
            <h3>🎯 Interactive Quizzes</h3>
            <p>Test your knowledge with dynamic quizzes. Track your progress and become a crypto expert through practice.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Category Distribution Chart
    st.subheader("📊 Learning Content Distribution")
    
    category_counts = df['category'].value_counts()
    fig = px.pie(
        values=category_counts.values,
        names=category_counts.index,
        title="Terms by Category",
        color_discrete_sequence=px.colors.qualitative.Set3,
        hole=0.4
    )
    fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=12)
    fig.update_layout(
        title_font_size=20,
        title_x=0.5,
        font=dict(size=14),
        showlegend=True
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Quick Actions
    st.subheader("🚀 Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🎲 Random Term", key="random_dash"):
            random_term = df.sample(1).iloc[0]
            st.success(f"**{random_term['term']}** ({random_term['category']})")
            st.info(random_term['definition'])
            st.session_state.user_progress['terms_learned'].add(random_term['term'])
    
    with col2:
        if st.button("🐕 Random Memecoin", key="memecoin_dash"):
            memecoin_terms = df[df['category'] == 'Memecoins']
            if len(memecoin_terms) > 0:
                random_memecoin = memecoin_terms.sample(1).iloc[0]
                st.success(f"**{random_memecoin['term']}**")
                st.info(random_memecoin['definition'])
    
    with col3:
        if st.button("📈 Live Prices", key="prices_dash"):
            with st.spinner("Fetching live data..."):
                prices = fetch_live_prices()
                if prices and 'bitcoin' in prices:
                    btc_price = prices['bitcoin']['usd']
                    btc_change = prices['bitcoin'].get('usd_24h_change', 0)
                    trend = "📈" if btc_change > 0 else "📉"
                    st.success(f"BTC: ${btc_price:,.2f} {trend} {btc_change:.2f}%")
    
    with col4:
        if st.button("🎯 Start Quiz", key="quiz_dash"):
            st.session_state.current_question = df.sample(1).iloc[0]
            st.rerun()

elif page == "🔍 Term Explorer":
    st.header("🔍 Comprehensive Term Explorer")
    
    # Advanced Search and Filters
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        search_term = st.text_input(
            "🔍 Search crypto terms...", 
            placeholder="Try: diamond hands, blockchain, DeFi, rugpull, yield farming...",
            help="Search across term names, definitions, and examples"
        )
    
    with col2:
        category_filter = st.selectbox(
            "📂 Category", 
            ['All'] + sorted(df['category'].unique()),
            help="Filter by specific category"
        )
    
    with col3:
        difficulty_filter = st.selectbox(
            "⭐ Difficulty", 
            ['All'] + sorted(df['difficulty'].unique()),
            help="Filter by learning difficulty"
        )
    
    # Advanced filters
    with st.expander("🔧 Advanced Filters"):
        col1, col2 = st.columns(2)
        with col1:
            tag_filter = st.multiselect(
                "🏷️ Tags",
                options=sorted(set([tag for tags in df['tags'] for tag in tags])),
                help="Filter by specific tags"
            )
        with col2:
            sort_by = st.selectbox(
                "📊 Sort by",
                ["Relevance", "Alphabetical", "Category", "Difficulty"],
                help="Choose how to sort results"
            )
    
    # Apply filters
    filtered_df = df.copy()
    
    if search_term:
        mask = (
            filtered_df['term'].str.contains(search_term, case=False, na=False) |
            filtered_df['definition'].str.contains(search_term, case=False, na=False) |
            filtered_df['example'].str.contains(search_term, case=False, na=False) |
            filtered_df['tags'].astype(str).str.contains(search_term, case=False, na=False)
        )
        filtered_df = filtered_df[mask]
    
    if category_filter != 'All':
        filtered_df = filtered_df[filtered_df['category'] == category_filter]
    
    if difficulty_filter != 'All':
        filtered_df = filtered_df[filtered_df['difficulty'] == difficulty_filter]
    
    if tag_filter:
        mask = filtered_df['tags'].apply(lambda x: any(tag in x for tag in tag_filter))
        filtered_df = filtered_df[mask]
    
    # Sort results
    if sort_by == "Alphabetical":
        filtered_df = filtered_df.sort_values('term')
    elif sort_by == "Category":
        filtered_df = filtered_df.sort_values(['category', 'term'])
    elif sort_by == "Difficulty":
        difficulty_order = {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3}
        filtered_df['difficulty_num'] = filtered_df['difficulty'].map(difficulty_order)
        filtered_df = filtered_df.sort_values('difficulty_num').drop('difficulty_num', axis=1)
    
    # Display results
    st.subheader(f"📚 Found {len(filtered_df)} terms")
    
    if len(filtered_df) == 0:
        st.warning("No terms found matching your criteria. Try adjusting your filters.")
        st.info("💡 **Suggestions:** Try broader search terms or remove some filters")
    
    for idx, term in filtered_df.iterrows():
        badge_class = "memecoin-badge" if term['category'] == 'Memecoins' else "crypto-badge"
        difficulty_color = {
            'Beginner': '🟢',
            'Intermediate': '🟡', 
            'Advanced': '🔴'
        }.get(term['difficulty'], '⚪')
        
        st.markdown(f"""
        <div class="term-card">
            <h3>{term['term']} <span class="{badge_class}">{term['category']}</span></h3>
            <p><strong>📖 Definition:</strong> {term['definition']
