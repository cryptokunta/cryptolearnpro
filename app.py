import streamlit as st
import pandas as pd
import requests
import random
import time
from datetime import datetime, timedelta

# Configure page
st.set_page_config(
    page_title="CryptoLearn Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS styling
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
    
    .progress-card {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 4px 20px rgba(86, 171, 47, 0.3);
    }
    
    .learned-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.2);
    }
    
    .streak-card {
        background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 4px 20px rgba(255, 107, 107, 0.3);
    }
    
    .achievement-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        text-align: center;
        color: #333;
        border: 2px solid #667eea;
    }
    
    .term-card {
        background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%);
        border-left: 5px solid #667eea;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .memecoin-badge {
        background: linear-gradient(90deg, #ff6b6b, #feca57);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .crypto-badge {
        background: linear-gradient(90deg, #4ecdc4, #45b7d1);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .learning-goal {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Comprehensive crypto terms database
@st.cache_data
def load_crypto_terms():
    """Load comprehensive crypto terminology database"""
    terms_data = [
        # Memecoin Culture
        {
            "term": "Diamond Hands",
            "definition": "Investors who hold cryptocurrency through extreme volatility, refusing to sell despite fear or losses.",
            "example": "Diamond hands held DOGE through the 2021 crash and were rewarded later. 💎🙌",
            "category": "Memecoins",
            "difficulty": "Beginner",
            "tags": ["culture", "holding", "resilience"],
            "importance": "High"
        },
        {
            "term": "Paper Hands",
            "definition": "Investors who sell quickly at signs of trouble or small profits, opposite of diamond hands.",
            "example": "Paper hands sold Bitcoin at $30k and missed the rally to $60k. 📄🙌",
            "category": "Memecoins",
            "difficulty": "Beginner",
            "tags": ["culture", "selling", "fear"],
            "importance": "High"
        },
        {
            "term": "To the Moon",
            "definition": "Expression indicating belief that a cryptocurrency's price will rise dramatically.",
            "example": "The community chanted 'DOGE to the moon!' during the 2021 rally. 🚀🌙",
            "category": "Memecoins",
            "difficulty": "Beginner",
            "tags": ["bullish", "optimism", "price"],
            "importance": "High"
        },
        {
            "term": "Ape In",
            "definition": "To invest heavily and quickly without thorough research, often driven by FOMO.",
            "example": "Many retail investors aped into memecoins during the 2021 bull run.",
            "category": "Memecoins",
            "difficulty": "Beginner",
            "tags": ["impulsive", "fomo", "risky"],
            "importance": "Medium"
        },
        {
            "term": "Rugpull",
            "definition": "A scam where developers abandon a project and steal funds by removing liquidity.",
            "example": "The Squid Game token was a rugpull that cost investors millions.",
            "category": "Memecoins",
            "difficulty": "Intermediate",
            "tags": ["scam", "fraud", "danger"],
            "importance": "Critical"
        },
        {
            "term": "WAGMI",
            "definition": "We're All Gonna Make It - optimistic phrase encouraging holding through difficult times.",
            "example": "Despite being down 70%, the community stays strong: 'WAGMI!' 💪",
            "category": "Memecoins",
            "difficulty": "Beginner",
            "tags": ["optimism", "community", "motivation"],
            "importance": "Medium"
        },
        {
            "term": "NGMI",
            "definition": "Not Gonna Make It - describing poor investment decisions or lack of conviction.",
            "example": "Selling Bitcoin at $16k during the bear market? That's NGMI behavior.",
            "category": "Memecoins",
            "difficulty": "Beginner",
            "tags": ["pessimism", "poor_decisions"],
            "importance": "Medium"
        },
        {
            "term": "Degen",
            "definition": "Short for 'degenerate' - someone who makes high-risk crypto investments with little research.",
            "example": "Degens bought random memecoins hoping for 100x gains during the bull run.",
            "category": "Memecoins",
            "difficulty": "Beginner",
            "tags": ["culture", "risky", "gambling"],
            "importance": "Medium"
        },
        
        # Trading Essentials
        {
            "term": "HODL",
            "definition": "Hold On for Dear Life - strategy of holding cryptocurrency long-term despite volatility.",
            "example": "Bitcoin HODLers who bought in 2017 were rewarded in 2021.",
            "category": "Trading",
            "difficulty": "Beginner",
            "tags": ["strategy", "long_term", "patience"],
            "importance": "Critical"
        },
        {
            "term": "FOMO",
            "definition": "Fear of Missing Out - anxiety driving impulsive buying when seeing others profit.",
            "example": "FOMO drove retail investors to buy Bitcoin at its $69k peak in 2021.",
            "category": "Psychology",
            "difficulty": "Beginner",
            "tags": ["emotion", "buying", "psychology"],
            "importance": "Critical"
        },
        {
            "term": "FUD",
            "definition": "Fear, Uncertainty, and Doubt - negative information spread to damage crypto reputation.",
            "example": "China's mining ban created FUD that temporarily crashed Bitcoin prices.",
            "category": "Psychology",
            "difficulty": "Beginner",
            "tags": ["negativity", "manipulation", "market"],
            "importance": "Critical"
        },
        {
            "term": "Whale",
            "definition": "Individual or entity holding large amounts of crypto, capable of influencing prices.",
            "example": "A Bitcoin whale moved 40,000 BTC to exchanges, causing market concern.",
            "category": "Trading",
            "difficulty": "Beginner",
            "tags": ["large_holder", "market_impact"],
            "importance": "High"
        },
        
        # DeFi & Technical
        {
            "term": "DeFi",
            "definition": "Decentralized Finance - financial applications built on blockchain without intermediaries.",
            "example": "DeFi protocols like Aave allow lending without traditional banks.",
            "category": "DeFi",
            "difficulty": "Intermediate",
            "tags": ["finance", "decentralized", "applications"],
            "importance": "High"
        },
        {
            "term": "Staking",
            "definition": "Locking cryptocurrency to support network operations and earn rewards.",
            "example": "Ethereum 2.0 stakers earn approximately 4-6% annual rewards.",
            "category": "DeFi",
            "difficulty": "Intermediate",
            "tags": ["rewards", "network", "validation"],
            "importance": "High"
        },
        {
            "term": "Smart Contract",
            "definition": "Self-executing contracts with terms directly written into code, automatically enforcing agreements.",
            "example": "Ethereum smart contracts power DeFi applications like Uniswap.",
            "category": "Blockchain",
            "difficulty": "Intermediate",
            "tags": ["ethereum", "automation", "programming"],
            "importance": "Critical"
        },
        {
            "term": "Gas Fees",
            "definition": "Transaction fees paid to miners/validators for processing blockchain transactions.",
            "example": "Ethereum gas fees can reach $100+ during network congestion.",
            "category": "Technical",
            "difficulty": "Beginner",
            "tags": ["fees", "transaction", "network"],
            "importance": "High"
        },
        
        # Security
        {
            "term": "Private Key",
            "definition": "Secret cryptographic key giving complete control over cryptocurrency funds.",
            "example": "Losing your private key means losing access to your crypto forever.",
            "category": "Security",
            "difficulty": "Beginner",
            "tags": ["security", "wallet", "control"],
            "importance": "Critical"
        },
        {
            "term": "Cold Storage",
            "definition": "Storing cryptocurrency offline to protect from hacks and online threats.",
            "example": "Hardware wallets like Ledger provide cold storage security.",
            "category": "Security",
            "difficulty": "Intermediate",
            "tags": ["security", "offline", "protection"],
            "importance": "High"
        }
    ]
    return pd.DataFrame(terms_data)

# Enhanced learning analytics
def calculate_learning_stats(df, learned_terms):
    """Calculate comprehensive learning statistics"""
    total_terms = len(df)
    learned_count = len(learned_terms)
    
    if learned_count == 0:
        return {
            'progress_percentage': 0,
            'level': 'Beginner',
            'next_milestone': 5,
            'categories_mastered': 0,
            'critical_terms_learned': 0,
            'recommendations': []
        }
    
    progress_percentage = (learned_count / total_terms) * 100
    
    if progress_percentage >= 80:
        level = 'Crypto Master 🏆'
    elif progress_percentage >= 60:
        level = 'Expert 🥇'
    elif progress_percentage >= 40:
        level = 'Advanced 🥈'
    elif progress_percentage >= 20:
        level = 'Intermediate 🥉'
    else:
        level = 'Beginner 📚'
    
    milestones = [5, 10, 15, 20, 25]
    next_milestone = next((m for m in milestones if m > learned_count), total_terms)
    
    learned_df = df[df['term'].isin(learned_terms)]
    categories_mastered = learned_df['category'].nunique() if len(learned_df) > 0 else 0
    
    critical_terms = df[df['importance'] == 'Critical']
    critical_learned = len(set(learned_terms) & set(critical_terms['term']))
    
    recommendations = []
    unlearned_critical = critical_terms[~critical_terms['term'].isin(learned_terms)]
    if len(unlearned_critical) > 0:
        recommendations.append(f"Focus on critical terms: {unlearned_critical.iloc[0]['term']}")
    
    return {
        'progress_percentage': progress_percentage,
        'level': level,
        'next_milestone': next_milestone,
        'categories_mastered': categories_mastered,
        'critical_terms_learned': critical_learned,
        'total_critical': len(critical_terms),
        'recommendations': recommendations
    }

# API function with proper error handling
@st.cache_data(ttl=300, show_spinner=False)
def fetch_crypto_prices():
    """Fetch live cryptocurrency prices"""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': 'bitcoin,ethereum,dogecoin,shiba-inu',
            'vs_currencies': 'usd',
            'include_24hr_change': 'true'
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except:
        return None

# Initialize session state
def init_session_state():
    """Initialize session state variables"""
    defaults = {
        'quiz_score': 0,
        'quiz_total': 0,
        'current_question': None,
        'quiz_answered': False,
        'user_progress': {
            'terms_learned': set(),
            'quiz_streak': 0
        },
        'selected_term': None
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Load data and initialize
df = load_crypto_terms()
init_session_state()

# Calculate learning stats
learned_terms = st.session_state.user_progress['terms_learned']
stats = calculate_learning_stats(df, learned_terms)

# Header
st.markdown("""
<div class="main-header">
    <h1>🚀 CryptoLearn Pro</h1>
    <h3>Master Crypto & Memecoin Terminology with Intelligent Learning</h3>
    <p>🎯 Personalized • 📊 Analytics • 🎮 Gamified • 🧠 Smart</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.markdown("### 🧭 Navigation Hub")
page = st.sidebar.selectbox(
    "Choose Your Learning Adventure:",
    [
        "🏠 Learning Dashboard",
        "🔍 Smart Term Explorer", 
        "📊 Live Market Data",
        "🎯 Adaptive Quiz",
        "🎲 Discovery Mode"
    ]
)

# Enhanced Sidebar Stats
st.sidebar.markdown("### 📊 Your Learning Profile")

progress_pct = stats['progress_percentage']
st.sidebar.markdown(f"**Level:** {stats['level']}")
st.sidebar.progress(progress_pct / 100)
st.sidebar.caption(f"Progress: {progress_pct:.1f}% ({len(learned_terms)}/{len(df)} terms)")

col1, col2 = st.sidebar.columns(2)
with col1:
    st.metric("🎯 Quiz Score", f"{st.session_state.quiz_score}/{st.session_state.quiz_total}")
    st.metric("📚 Learned", len(learned_terms))
with col2:
    st.metric("🔥 Quiz Streak", st.session_state.user_progress.get('quiz_streak', 0))
    st.metric("🏆 Categories", f"{stats['categories_mastered']}/{df['category'].nunique()}")

# Main Content
if page == "🏠 Learning Dashboard":
    # Personal Progress Section
    st.subheader("📊 Your Learning Journey")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="learned-card">
            <h3>📚 Terms Learned</h3>
            <h1>{len(learned_terms)}</h1>
            <p>Out of {len(df)} total</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="progress-card">
            <h3>📈 Progress Level</h3>
            <h1>{stats['level'].split()[0]}</h1>
            <p>{stats['progress_percentage']:.1f}% Complete</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="streak-card">
            <h3>🔥 Quiz Streak</h3>
            <h1>{st.session_state.user_progress.get('quiz_streak', 0)}</h1>
            <p>Correct answers</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        critical_ratio = f"{stats['critical_terms_learned']}/{stats['total_critical']}"
        st.markdown(f"""
        <div class="learned-card">
            <h3>⚡ Critical Terms</h3>
            <h1>{critical_ratio}</h1>
            <p>Essential knowledge</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Personalized Learning Actions
    st.subheader("🎯 Personalized Learning Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🧠 Smart Recommendation", type="primary", use_container_width=True):
            unlearned = df[~df['term'].isin(learned_terms)]
            
            if len(unlearned) > 0:
                critical_unlearned = unlearned[unlearned['importance'] == 'Critical']
                if len(critical_unlearned) > 0:
                    term = critical_unlearned.sample(1).iloc[0]
                    st.info("🔴 Critical Term Recommended!")
                else:
                    high_unlearned = unlearned[unlearned['importance'] == 'High']
                    if len(high_unlearned) > 0:
                        term = high_unlearned.sample(1).iloc[0]
                        st.info("🟡 High Priority Term!")
                    else:
                        term = unlearned.sample(1).iloc[0]
                        st.info("📚 Good Term to Learn!")
                
                emoji = "🐕" if term['category'] == 'Memecoins' else "💰"
                st.success(f"{emoji} **{term['term']}** ({term['category']})")
                st.write(f"📖 {term['definition']}")
                st.caption(f"💡 {term['example']}")
                
                if st.button("✅ Mark as Learned", key="smart_learn"):
                    st.session_state.user_progress['terms_learned'].add(term['term'])
                    st.balloons()
                    st.success("Great! Added to your learned terms! 🎉")
                    st.rerun()
            else:
                st.success("🎉 Congratulations! You've learned all available terms!")
    
    with col2:
        if st.button("📈 Live Market Check", use_container_width=True):
            with st.spinner("Fetching market data..."):
                prices = fetch_crypto_prices()
                if prices and 'bitcoin' in prices:
                    btc = prices['bitcoin']
                    change = btc.get('usd_24h_change', 0)
                    emoji = "📈" if change > 0 else "📉"
                    st.metric("Bitcoin", f"${btc['usd']:,.2f}", f"{change:.2f}%")
                else:
                    st.info("📡 Market data temporarily unavailable")
    
    with col3:
        if st.button("🎯 Adaptive Quiz", use_container_width=True):
            unlearned = df[~df['term'].isin(learned_terms)]
            
            if len(unlearned) > 0:
                if len(learned_terms) > 0 and random.random() < 0.3:
                    learned_df = df[df['term'].isin(learned_terms)]
                    question = learned_df.sample(1).iloc[0]
                    st.info("🔄 Review Mode: Testing a term you've learned!")
                else:
                    question = unlearned.sample(1).iloc[0]
                    st.info("🆕 Learning Mode: New term quiz!")
                
                st.session_state.current_question = question
                st.session_state.quiz_answered = False
                st.write(f"**Quiz:** What does '{question['term']}' mean?")
                st.caption("Switch to 'Adaptive Quiz' tab to answer!")
            else:
                st.success("🎉 You've mastered all terms! Try the review mode.")

elif page == "🔍 Smart Term Explorer":
    st.header("🔍 Smart Term Explorer with AI Recommendations")
    
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        search_term = st.text_input(
            "🔍 Search crypto terms...",
            placeholder="diamond hands, blockchain, DeFi, rugpull...",
            help="Search across terms, definitions, and examples"
        )
    
    with col2:
        category_filter = st.selectbox("📂 Category", ['All', 'Recommended'] + sorted(df['category'].unique()))
    
    with col3:
        learning_filter = st.selectbox("📚 Learning Status", ['All', 'Not Learned', 'Learned', 'Critical'])
    
    # Apply intelligent filters
    filtered_df = df.copy()
    
    if search_term:
        mask = (
            filtered_df['term'].str.contains(search_term, case=False, na=False) |
            filtered_df['definition'].str.contains(search_term, case=False, na=False) |
            filtered_df['example'].str.contains(search_term, case=False, na=False)
        )
        filtered_df = filtered_df[mask]
    
    if category_filter == 'Recommended':
        unlearned = filtered_df[~filtered_df['term'].isin(learned_terms)]
        critical_unlearned = unlearned[unlearned['importance'] == 'Critical']
        high_unlearned = unlearned[unlearned['importance'] == 'High']
        
        recommended_terms = pd.concat([critical_unlearned, high_unlearned]).drop_duplicates()
        filtered_df = recommended_terms if len(recommended_terms) > 0 else unlearned
        
    elif category_filter != 'All':
        filtered_df = filtered_df[filtered_df['category'] == category_filter]
    
    if learning_filter == 'Not Learned':
        filtered_df = filtered_df[~filtered_df['term'].isin(learned_terms)]
    elif learning_filter == 'Learned':
        filtered_df = filtered_df[filtered_df['term'].isin(learned_terms)]
    elif learning_filter == 'Critical':
        filtered_df = filtered_df[filtered_df['importance'] == 'Critical']
    
    st.subheader(f"📚 Found {len(filtered_df)} terms")
    
    if category_filter == 'Recommended':
        st.info("🎯 These terms are recommended based on your learning progress and their importance!")
    
    for _, term in filtered_df.iterrows():
        is_learned = term['term'] in learned_terms
        badge_class = "memecoin-badge" if term['category'] == 'Memecoins' else "crypto-badge"
        difficulty_emoji = {'Beginner': '🟢', 'Intermediate': '🟡', 'Advanced': '🔴'}.get(term['difficulty'], '⚪')
        importance_emoji = {'Critical': '🔴', 'High': '🟡', 'Medium': '⚪'}.get(term['importance'], '⚪')
        
        status_emoji = "✅" if is_learned else "📖"
        status_text = "Learned" if is_learned else "Not Learned"
        
        with st.expander(f"{status_emoji} {term['term']} ({term['category']}) - {status_text}"):
            st.markdown(f"""
            <div class="term-card">
                <h3>{term['term']} <span class="{badge_class}">{term['category']}</span></h3>
                <p><strong>📖 Definition:</strong> {term['definition']}</p>
                <p><strong>💡 Example:</strong> {term['example']}</p>
                <p><strong>{difficulty_emoji} Difficulty:</strong> {term['difficulty']} | 
                   <strong>{importance_emoji} Importance:</strong> {term['importance']} | 
                   <strong>🏷️ Tags:</strong> {', '.join(term['tags'])}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            if not is_learned:
                with col1:
                    if st.button(f"✅ Mark as Learned", key=f"learn_{term['term']}"):
                        st.session_state.user_progress['terms_learned'].add(term['term'])
                        st.success(f"Added '{term['term']}' to your learned terms! 🎉")
                        if term['importance'] == 'Critical':
                            st.balloons()
                        st.rerun()
                
                with col2:
                    if st.button(f"🎯 Quiz Me", key=f"quiz_{term['term']}"):
                        st.session_state.current_question = term
                        st.session_state.quiz_answered = False
                        st.info("Quiz question set! Go to Adaptive Quiz tab.")

elif page == "📊 Live Market Data":
    st.header("📊 Live Market Data with Learning Context")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh Data", type="primary"):
            st.cache_data.clear()
            st.rerun()
    
    with col2:
        st.info("💡 Data refreshes automatically every 5 minutes")
    
    with st.spinner("🔄 Fetching live market data..."):
        prices = fetch_crypto_prices()
    
    if prices:
        st.subheader("💰 Live Cryptocurrency Prices")
        
        coins_data = [
            ('bitcoin', 'Bitcoin', '₿'),
            ('ethereum', 'Ethereum', 'Ξ'),
            ('dogecoin', 'Dogecoin', '🐕'),
            ('shiba-inu', 'Shiba Inu', '🐕‍🦺')
        ]
        
        cols = st.columns(len(coins_data))
        
        for idx, (coin_id, name, symbol) in enumerate(coins_data):
            if coin_id in prices:
                data = prices[coin_id]
                price = data.get('usd', 0)
                change = data.get('usd_24h_change', 0)
                
                if price < 0.01:
                    price_str = f"${price:.6f}"
                elif price < 1:
                    price_str = f"${price:.4f}"
                else:
                    price_str = f"${price:,.2f}"
                
                with cols[idx]:
                    st.metric(
                        label=f"{symbol} {name}",
                        value=price_str,
                        delta=f"{change:.2f}%"
                    )
        
        # Market context with learning suggestions
        st.subheader("💡 Market Context & Learning Opportunities")
        
        if 'bitcoin' in prices:
            btc_change = prices['bitcoin'].get('usd_24h_change', 0)
            
            if btc_change > 5:
                st.success("🚀 Bitcoin is pumping! Perfect time to learn:")
                suggested_terms = ['To the Moon', 'FOMO', 'Diamond Hands']
                for term in suggested_terms:
                    if term not in learned_terms:
                        st.info(f"📚 Learn about '{term}' - relevant to today's market!")
                        break
                        
            elif btc_change < -5:
                st.warning("📉 Bitcoin is down today. Good time to understand:")
                suggested_terms = ['FUD', 'Paper Hands', 'HODL']
                for term in suggested_terms:
                    if term not in learned_terms:
                        st.info(f"📚 Learn about '{term}' - perfect for bear market psychology!")
                        break
            else:
                st.info("📊 Stable market today. Great time to learn fundamentals:")
                fundamental_terms = ['Smart Contract', 'DeFi', 'Staking']
                for term in fundamental_terms:
                    if term not in learned_terms:
                        st.info(f"📚 Learn about '{term}' - essential crypto knowledge!")
                        break
    else:
        st.warning("📡 Live market data temporarily unavailable")
        st.info("💡 Perfect time to focus on fundamental learning instead of price watching!")

elif page == "🎯 Adaptive Quiz":
    st.header("🎯 Adaptive Quiz System")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎯 Score", f"{st.session_state.quiz_score}/{st.session_state.quiz_total}")
    with col2:
        if st.session_state.quiz_total > 0:
            accuracy = (st.session_state.quiz_score / st.session_state.quiz_total) * 100
            st.metric("📊 Accuracy", f"{accuracy:.1f}%")
        else:
            st.metric("📊 Accuracy", "0%")
    with col3:
        streak = st.session_state.user_progress.get('quiz_streak', 0)
        st.metric("🔥 Streak", streak)
    with col4:
        st.metric("📚 Terms Learned", len(learned_terms))
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🧠 Smart Quiz", type="primary", use_container_width=True):
            unlearned = df[~df['term'].isin(learned_terms)]
            
            if len(unlearned) > 0:
                critical_unlearned = unlearned[unlearned['importance'] == 'Critical']
                if len(critical_unlearned) > 0:
                    question = critical_unlearned.sample(1).iloc[0]
                    quiz_type = "Critical Learning"
                else:
                    question = unlearned.sample(1).iloc[0]
                    quiz_type = "New Learning"
            else:
                question = df.sample(1).iloc[0]
                quiz_type = "Mastery Review"
            
            st.session_state.current_question = question
            st.session_state.quiz_answered = False
            st.session_state.quiz_type = quiz_type
            st.rerun()
    
    with col2:
        if st.button("🔄 Review Quiz", use_container_width=True):
            if len(learned_terms) > 0:
                learned_df = df[df['term'].isin(learned_terms)]
                question = learned_df.sample(1).iloc[0]
                st.session_state.current_question = question
                st.session_state.quiz_answered = False
                st.session_state.quiz_type = "Review Mode"
                st.rerun()
            else:
                st.info("Learn some terms first to enable review mode!")
    
    with col3:
        if st.button("🔴 Critical Only", use_container_width=True):
            critical_terms = df[df['importance'] == 'Critical']
            if len(critical_terms) > 0:
                question = critical_terms.sample(1).iloc[0]
                st.session_state.current_question = question
                st.session_state.quiz_answered = False
                st.session_state.quiz_type = "Critical Focus"
                st.rerun()
            else:
                st.error("No critical terms available!")
    
    if st.session_state.current_question is not None:
        question = st.session_state.current_question
        quiz_type = getattr(st.session_state, 'quiz_type', 'Standard')
        
        type_colors = {
            "Critical Learning": "🔴",
            "New Learning": "🟢", 
            "Mastery Review": "🟡",
            "Review Mode": "🔵",
            "Critical Focus": "🔴"
        }
        
        st.info(f"{type_colors.get(quiz_type, '🎯')} **{quiz_type}** Quiz Mode")
        
        st.subheader("❓ Quiz Question")
        st.info(f"**What does '{question['term']}' mean?**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.caption(f"📂 Category: {question['category']}")
        with col2:
            st.caption(f"⭐ Difficulty: {question['difficulty']}")
        with col3:
            importance_color = {'Critical': '🔴', 'High': '🟡', 'Medium': '⚪'}
            st.caption(f"{importance_color.get(question['importance'], '⚪')} Importance: {question['importance']}")
        
        correct_answer = question['definition']
        other_terms = df[df['term'] != question['term']]
        
        same_category = other_terms[other_terms['category'] == question['category']]
        if len(same_category) >= 2:
            wrong_answers = same_category.sample(min(2, len(same_category)))['definition'].tolist()
            remaining_needed = 3 - len(wrong_answers)
            if remaining_needed > 0:
                other_options = other_terms[~other_terms['definition'].isin(wrong_answers)]
                additional = other_options.sample(min(remaining_needed, len(other_options)))['definition'].tolist()
                wrong_answers.extend(additional)
        else:
            wrong_answers = other_terms.sample(min(3, len(other_terms)))['definition'].tolist()
        
        options = [correct_answer] + wrong_answers[:3]
        random.shuffle(options)
        
        user_answer = st.radio(
            "Choose the correct definition:",
            options,
            key="adaptive_quiz_radio",
            disabled=st.session_state.quiz_answered
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Submit Answer", disabled=st.session_state.quiz_answered):
                st.session_state.quiz_answered = True
                st.session_state.quiz_total += 1
                
                if user_answer == correct_answer:
                    st.session_state.quiz_score += 1
                    st.session_state.user_progress['quiz_streak'] += 1
                    st.session_state.user_progress['terms_learned'].add(question['term'])
                    
                    st.success("🎉 Correct! Excellent work!")
                    if question['importance'] == 'Critical':
                        st.balloons()
                        st.success("🔴 Critical term mastered! This is essential knowledge!")
                    
                    streak = st.session_state.user_progress['quiz_streak']
                    if streak > 0 and streak % 5 == 0:
                        st.success(f"🔥 Amazing! {streak} correct answers in a row!")
                        
                else:
                    st.session_state.user_progress['quiz_streak'] = 0
                    st.error("❌ Not quite right. Keep learning!")
                
                st.info(f"✅ **Correct Answer:** {correct_answer}")
                st.caption(f"💡 **Example:** {question['example']}")
        
        with col2:
            if st.button("⏭️ Next Question"):
                if quiz_type in ["Critical Learning", "Critical Focus"]:
                    critical_unlearned = df[(df['importance'] == 'Critical') & (~df['term'].isin(learned_terms))]
                    if len(critical_unlearned) > 0:
                        next_question = critical_unlearned.sample(1).iloc[0]
                    else:
                        next_question = df.sample(1).iloc[0]
                else:
                    unlearned = df[~df['term'].isin(learned_terms)]
                    next_question = unlearned.sample(1).iloc[0] if len(unlearned) > 0 else df.sample(1).iloc[0]
                
                st.session_state.current_question = next_question
                st.session_state.quiz_answered = False
                st.rerun()
                
    else:
        st.info("👆 Click a quiz mode button to start learning!")

elif page == "🎲 Discovery Mode":
    st.header("🎲 Intelligent Discovery Mode")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🧠 AI Recommendation", type="primary", use_container_width=True):
            unlearned = df[~df['term'].isin(learned_terms)]
            
            if len(unlearned) > 0:
                critical_unlearned = unlearned[unlearned['importance'] == 'Critical']
                if len(critical_unlearned) > 0:
                    term = critical_unlearned.sample(1).iloc[0]
                    discovery_type = "🔴 Critical Discovery"
                else:
                    beginner_unlearned = unlearned[unlearned['difficulty'] == 'Beginner']
                    if len(beginner_unlearned) > 0:
                        term = beginner_unlearned.sample(1).iloc[0]
                        discovery_type = "🟢 Beginner-Friendly Discovery"
                    else:
                        term = unlearned.sample(1).iloc[0]
                        discovery_type = "📚 General Discovery"
                
                st.session_state.discovery_term = term
                st.session_state.discovery_type = discovery_type
            else:
                st.success("🎉 You've learned everything! Try review mode.")
    
    with col2:
        if st.button("🐕 Memecoin Deep Dive", use_container_width=True):
            memecoin_terms = df[df['category'] == 'Memecoins']
            unlearned_meme = memecoin_terms[~memecoin_terms['term'].isin(learned_terms)]
            
            if len(unlearned_meme) > 0:
                term = unlearned_meme.sample(1).iloc[0]
                st.session_state.discovery_term = term
                st.session_state.discovery_type = "🐕 Memecoin Culture"
            else:
                learned_meme = memecoin_terms[memecoin_terms['term'].isin(learned_terms)]
                if len(learned_meme) > 0:
                    term = learned_meme.sample(1).iloc[0]
                    st.session_state.discovery_term = term
                    st.session_state.discovery_type = "🔄 Memecoin Review"
                else:
                    st.warning("No memecoin terms available!")
    
    with col3:
        if st.button("⚡ Quick Foundation", use_container_width=True):
            foundation_categories = ['Blockchain', 'Security', 'Trading']
            foundation_terms = df[df['category'].isin(foundation_categories)]
            unlearned_foundation = foundation_terms[~foundation_terms['term'].isin(learned_terms)]
            
            if len(unlearned_foundation) > 0:
                term = unlearned_foundation.sample(1).iloc[0]
                st.session_state.discovery_term = term
                st.session_state.discovery_type = "⚡ Foundation Building"
            else:
                st.info("Foundation terms completed! Try other categories.")
    
    if hasattr(st.session_state, 'discovery_term') and st.session_state.discovery_term is not None:
        term = st.session_state.discovery_term
        discovery_type = getattr(st.session_state, 'discovery_type', 'Discovery')
        
        st.info(f"**{discovery_type}**")
        
        emoji = "🐕" if term['category'] == 'Memecoins' else "💰"
        difficulty_emoji = {'Beginner': '🟢', 'Intermediate': '🟡', 'Advanced': '🔴'}.get(term['difficulty'], '⚪')
        importance_emoji = {'Critical': '🔴', 'High': '🟡', 'Medium': '⚪'}.get(term['importance'], '⚪')
        
        is_learned = term['term'] in learned_terms
        status = "✅ Already Learned" if is_learned else "📖 New Term"
        
        st.markdown(f"""
        <div class="term-card">
            <h2>{emoji} {term['term']} ({status})</h2>
            <p><strong>📖 Definition:</strong> {term['definition']}</p>
            <p><strong>💡 Example:</strong> {term['example']}</p>
            <p><strong>📂 Category:</strong> {term['category']} | 
               <strong>{difficulty_emoji} Difficulty:</strong> {term['difficulty']} | 
               <strong>{importance_emoji} Importance:</strong> {term['importance']}</p>
            <p><strong>🏷️ Tags:</strong> {', '.join(term['tags'])}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        if not is_learned:
            with col1:
                if st.button("✅ Mark as Learned", key="discovery_learn"):
                    st.session_state.user_progress['terms_learned'].add(term['term'])
                    st.success(f"Added '{term['term']}' to your learned terms! 🎉")
                    if term['importance'] == 'Critical':
                        st.balloons()
                        st.success("🔴 Critical term mastered!")
                    st.rerun()
        else:
            with col1:
                st.success("✅ Already learned!")
        
        with col2:
            if st.button("🎯 Quiz Me", key="discovery_quiz"):
                st.session_state.current_question = term
                st.session_state.quiz_answered = False
                quiz_mode = "Review" if is_learned else "Learning"
                st.info(f"{quiz_mode} quiz ready! Go to Adaptive Quiz.")
        
        with col3:
            if st.button("🔄 Discover Another", key="discovery_another"):
                unlearned = df[~df['term'].isin(learned_terms)]
                if len(unlearned) > 0:
                    if "Critical" in discovery_type:
                        critical_remaining = unlearned[unlearned['importance'] == 'Critical']
                        new_term = critical_remaining.sample(1).iloc[0] if len(critical_remaining) > 0 else unlearned.sample(1).iloc[0]
                    elif "Memecoin" in discovery_type:
                        meme_remaining = unlearned[unlearned['category'] == 'Memecoins']
                        new_term = meme_remaining.sample(1).iloc[0] if len(meme_remaining) > 0 else unlearned.sample(1).iloc[0]
                    else:
                        new_term = unlearned.sample(1).iloc[0]
                    
                    st.session_state.discovery_term = new_term
                    st.rerun()
                else:
                    st.success("🎉 All terms discovered!")
        
        with col4:
            if term['importance'] == 'Critical':
                st.error("🔴 Essential!")
            elif term['importance'] == 'High':
                st.warning("🟡 Important")
            else:
                st.info("📚 Good to know")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    ### 🚀 CryptoLearn Pro
    **Your Intelligent Crypto Learning Platform**
    
    **🎯 Features:**
    - {len(df)} Comprehensive Terms
    - Smart AI Recommendations
    - Adaptive Quiz System
    - Progress Analytics
    """)

with col2:
    st.markdown(f"""
    ### 📊 Your Learning Journey
    - **Progress Level:** {stats['level']}
    - **Terms Learned:** {len(learned_terms)}/{len(df)}
    - **Quiz Performance:** {st.session_state.quiz_score}/{st.session_state.quiz_total}
    - **Categories Explored:** {stats['categories_mastered']}/{len(df['category'].nunique())}
    - **Critical Terms:** {stats['critical_terms_learned']}/{stats['total_critical']}
    """)

with col3:
    st.markdown("""
    ### 🔗 Resources & Links
    - [📖 Crypto News](https://cointelegraph.com)
    - [📊 Market Data](https://coingecko.com)
    - [💬 Community](https://reddit.com/r/cryptocurrency)
    - [🛠️ GitHub Repo](https://github.com/cryptokunta/cryptolearnpro)
    """)

# Smart success celebrations
current_learned = len(learned_terms)
if 'last_learned_count' not in st.session_state:
    st.session_state.last_learned_count = 0

if current_learned > st.session_state.last_learned_count:
    newly_learned = current_learned - st.session_state.last_learned_count
    st.session_state.last_learned_count = current_learned
    
    if newly_learned > 0:
        if current_learned % 10 == 0:
            st.balloons()
            st.success(f"🎉 AMAZING! You've learned {current_learned} terms! You're becoming a crypto expert!")
        elif current_learned % 5 == 0:
            st.success(f"🌟 Great milestone! {current_learned} terms learned!")
        elif current_learned == 1:
            st.success("🎉 Congratulations on learning your first crypto term!")

# Performance optimization
if page == "📊 Live Market Data":
    time.sleep(0.1)
