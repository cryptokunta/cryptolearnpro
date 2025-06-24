import streamlit as st
import pandas as pd
import requests
import random
import time

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
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.2);
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
</style>
""", unsafe_allow_html=True)

# Comprehensive crypto terms database
@st.cache_data
def load_crypto_terms():
    """Load comprehensive crypto terminology database"""
    terms_data = [
        {
            "term": "Diamond Hands",
            "definition": "Investors who hold cryptocurrency through extreme volatility, refusing to sell despite fear or losses.",
            "example": "Diamond hands held DOGE through the 2021 crash and were rewarded later. 💎🙌",
            "category": "Memecoins",
            "difficulty": "Beginner",
            "tags": ["culture", "holding", "resilience"]
        },
        {
            "term": "Paper Hands",
            "definition": "Investors who sell quickly at signs of trouble or small profits, opposite of diamond hands.",
            "example": "Paper hands sold Bitcoin at $30k and missed the rally to $60k. 📄🙌",
            "category": "Memecoins",
            "difficulty": "Beginner",
            "tags": ["culture", "selling", "fear"]
        },
        {
            "term": "To the Moon",
            "definition": "Expression indicating belief that a cryptocurrency's price will rise dramatically.",
            "example": "The community chanted 'DOGE to the moon!' during the 2021 rally. 🚀🌙",
            "category": "Memecoins",
            "difficulty": "Beginner",
            "tags": ["bullish", "optimism", "price"]
        },
        {
            "term": "Ape In",
            "definition": "To invest heavily and quickly without thorough research, often driven by FOMO.",
            "example": "Many retail investors aped into memecoins during the 2021 bull run.",
            "category": "Memecoins",
            "difficulty": "Beginner",
            "tags": ["impulsive", "fomo", "risky"]
        },
        {
            "term": "Rugpull",
            "definition": "A scam where developers abandon a project and steal funds by removing liquidity.",
            "example": "The Squid Game token was a rugpull that cost investors millions.",
            "category": "Memecoins",
            "difficulty": "Intermediate",
            "tags": ["scam", "fraud", "danger"]
        },
        {
            "term": "WAGMI",
            "definition": "We're All Gonna Make It - optimistic phrase encouraging holding through difficult times.",
            "example": "Despite being down 70%, the community stays strong: 'WAGMI!' 💪",
            "category": "Memecoins",
            "difficulty": "Beginner",
            "tags": ["optimism", "community", "motivation"]
        },
        {
            "term": "NGMI",
            "definition": "Not Gonna Make It - describing poor investment decisions or lack of conviction.",
            "example": "Selling Bitcoin at $16k during the bear market? That's NGMI behavior.",
            "category": "Memecoins",
            "difficulty": "Beginner",
            "tags": ["pessimism", "poor_decisions"]
        },
        {
            "term": "Degen",
            "definition": "Short for 'degenerate' - someone who makes high-risk crypto investments with little research.",
            "example": "Degens bought random memecoins hoping for 100x gains during the bull run.",
            "category": "Memecoins",
            "difficulty": "Beginner",
            "tags": ["culture", "risky", "gambling"]
        },
        {
            "term": "HODL",
            "definition": "Hold On for Dear Life - strategy of holding cryptocurrency long-term despite volatility.",
            "example": "Bitcoin HODLers who bought in 2017 were rewarded in 2021.",
            "category": "Trading",
            "difficulty": "Beginner",
            "tags": ["strategy", "long_term", "patience"]
        },
        {
            "term": "FOMO",
            "definition": "Fear of Missing Out - anxiety driving impulsive buying when seeing others profit.",
            "example": "FOMO drove retail investors to buy Bitcoin at its $69k peak in 2021.",
            "category": "Psychology",
            "difficulty": "Beginner",
            "tags": ["emotion", "buying", "psychology"]
        },
        {
            "term": "FUD",
            "definition": "Fear, Uncertainty, and Doubt - negative information spread to damage crypto reputation.",
            "example": "China's mining ban created FUD that temporarily crashed Bitcoin prices.",
            "category": "Psychology",
            "difficulty": "Beginner",
            "tags": ["negativity", "manipulation", "market"]
        },
        {
            "term": "Whale",
            "definition": "Individual or entity holding large amounts of crypto, capable of influencing prices.",
            "example": "A Bitcoin whale moved 40,000 BTC to exchanges, causing market concern.",
            "category": "Trading",
            "difficulty": "Beginner",
            "tags": ["large_holder", "market_impact"]
        },
        {
            "term": "DeFi",
            "definition": "Decentralized Finance - financial applications built on blockchain without intermediaries.",
            "example": "DeFi protocols like Aave allow lending without traditional banks.",
            "category": "DeFi",
            "difficulty": "Intermediate",
            "tags": ["finance", "decentralized", "applications"]
        },
        {
            "term": "Staking",
            "definition": "Locking cryptocurrency to support network operations and earn rewards.",
            "example": "Ethereum 2.0 stakers earn approximately 4-6% annual rewards.",
            "category": "DeFi",
            "difficulty": "Intermediate",
            "tags": ["rewards", "network", "validation"]
        },
        {
            "term": "Gas Fees",
            "definition": "Transaction fees paid to miners/validators for processing blockchain transactions.",
            "example": "Ethereum gas fees can reach $100+ during network congestion.",
            "category": "Technical",
            "difficulty": "Beginner",
            "tags": ["fees", "transaction", "network"]
        },
        {
            "term": "Smart Contract",
            "definition": "Self-executing contracts with terms directly written into code, automatically enforcing agreements.",
            "example": "Ethereum smart contracts power DeFi applications like Uniswap.",
            "category": "Blockchain",
            "difficulty": "Intermediate",
            "tags": ["ethereum", "automation", "programming"]
        },
        {
            "term": "Private Key",
            "definition": "Secret cryptographic key giving complete control over cryptocurrency funds.",
            "example": "Losing your private key means losing access to your crypto forever.",
            "category": "Security",
            "difficulty": "Beginner",
            "tags": ["security", "wallet", "control"]
        },
        {
            "term": "Cold Storage",
            "definition": "Storing cryptocurrency offline to protect from hacks and online threats.",
            "example": "Hardware wallets like Ledger provide cold storage security.",
            "category": "Security",
            "difficulty": "Intermediate",
            "tags": ["security", "offline", "protection"]
        }
    ]
    return pd.DataFrame(terms_data)

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
    except requests.exceptions.Timeout:
        st.warning("⏰ API timeout - showing cached data")
        return None
    except requests.exceptions.ConnectionError:
        st.warning("🌐 Connection error - check internet")
        return None
    except Exception as e:
        st.warning(f"❌ API error: {str(e)[:50]}...")
        return None

# Initialize session state
def init_session_state():
    """Initialize session state variables"""
    defaults = {
        'quiz_score': 0,
        'quiz_total': 0,
        'current_question': None,
        'quiz_answered': False,
        'user_progress': {'terms_learned': set()},
        'selected_term': None
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Load data and initialize
df = load_crypto_terms()
init_session_state()

# Header
st.markdown("""
<div class="main-header">
    <h1>🚀 CryptoLearn Pro</h1>
    <h3>Master Crypto & Memecoin Terminology with Interactive Learning</h3>
    <p>🎯 Learn • 📈 Track • 🎮 Practice • 🌟 Master</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.markdown("### 🧭 Navigation Hub")
page = st.sidebar.selectbox(
    "Choose Your Learning Adventure:",
    [
        "🏠 Dashboard",
        "🔍 Term Explorer", 
        "📊 Live Market Data",
        "🎯 Interactive Quiz",
        "🎲 Discovery Mode"
    ]
)

# Sidebar Stats
st.sidebar.markdown("### 📊 Platform Stats")
total_terms = len(df)
categories = df['category'].nunique()
memecoins = len(df[df['category'] == 'Memecoins'])

col1, col2 = st.sidebar.columns(2)
with col1:
    st.metric("📚 Terms", total_terms)
    st.metric("🐕 Memecoins", memecoins)
with col2:
    st.metric("📂 Categories", categories)
    st.metric("⭐ Levels", df['difficulty'].nunique())

# User Progress in sidebar
if len(st.session_state.user_progress['terms_learned']) > 0:
    st.sidebar.markdown("### 🎯 Your Progress")
    progress = len(st.session_state.user_progress['terms_learned']) / total_terms
    st.sidebar.progress(progress)
    st.sidebar.caption(f"Learned: {len(st.session_state.user_progress['terms_learned'])}/{total_terms} terms")

# Main Content
if page == "🏠 Dashboard":
    # Welcome section with metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📚 Total Terms</h3>
            <h1>{total_terms}</h1>
            <p>Comprehensive database</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🐕 Memecoin Culture</h3>
            <h1>{memecoins}</h1>
            <p>Diamond hands & more</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🔥 Categories</h3>
            <h1>{categories}</h1>
            <p>Diverse topics covered</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        learned = len(st.session_state.user_progress['terms_learned'])
        st.markdown(f"""
        <div class="metric-card">
            <h3>🎯 Your Progress</h3>
            <h1>{learned}</h1>
            <p>Terms mastered</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Actions with working buttons
    st.subheader("🚀 Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎲 Random Term", key="dash_random", use_container_width=True):
            term = df.sample(1).iloc[0]
            st.session_state.selected_term = term
            emoji = "🐕" if term['category'] == 'Memecoins' else "💰"
            
            st.success(f"{emoji} **{term['term']}** ({term['category']})")
            st.info(f"📖 {term['definition']}")
            st.caption(f"💡 Example: {term['example']}")
            
            # Add to learned terms
            st.session_state.user_progress['terms_learned'].add(term['term'])
            
            if st.button("✅ Mark as Learned", key="mark_learned"):
                st.balloons()
                st.success("Added to your learned terms! 🎉")
    
    with col2:
        if st.button("📈 Live Crypto Prices", key="dash_prices", use_container_width=True):
            with st.spinner("Fetching live data..."):
                prices = fetch_crypto_prices()
                if prices:
                    if 'bitcoin' in prices:
                        btc = prices['bitcoin']
                        change = btc.get('usd_24h_change', 0)
                        emoji = "📈" if change > 0 else "📉"
                        st.metric("Bitcoin", f"${btc['usd']:,.2f}", f"{change:.2f}%")
                    
                    if 'ethereum' in prices:
                        eth = prices['ethereum']
                        change = eth.get('usd_24h_change', 0)
                        emoji = "📈" if change > 0 else "📉"
                        st.metric("Ethereum", f"${eth['usd']:,.2f}", f"{change:.2f}%")
                else:
                    st.info("📡 Live data temporarily unavailable")
    
    with col3:
        if st.button("🎯 Quick Quiz", key="dash_quiz", use_container_width=True):
            question = df.sample(1).iloc[0]
            st.session_state.current_question = question
            st.session_state.quiz_answered = False
            
            st.info(f"**Quiz Question Generated!**")
            st.write(f"What does **{question['term']}** mean?")
            st.caption("💡 Switch to 'Interactive Quiz' tab to answer!")
    
    # Category breakdown chart
    st.subheader("📊 Learning Categories Overview")
    category_counts = df['category'].value_counts()
    
    # Create simple chart
    chart_data = pd.DataFrame({
        'Category': category_counts.index,
        'Count': category_counts.values
    })
    st.bar_chart(chart_data.set_index('Category'))
    
    # Featured terms
    st.subheader("🌟 Featured Terms Today")
    featured = df.sample(3)
    
    for _, term in featured.iterrows():
        col1, col2 = st.columns([3, 1])
        with col1:
            badge_class = "memecoin-badge" if term['category'] == 'Memecoins' else "crypto-badge"
            st.markdown(f"""
            <div class="term-card">
                <h4>{term['term']} <span class="{badge_class}">{term['category']}</span></h4>
                <p>{term['definition'][:100]}...</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button(f"Learn More", key=f"featured_{term['term']}"):
                st.session_state.selected_term = term
                st.info(f"✅ Selected: {term['term']}")

elif page == "🔍 Term Explorer":
    st.header("🔍 Comprehensive Term Explorer")
    
    # Search interface
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        search_term = st.text_input(
            "🔍 Search crypto terms...",
            placeholder="diamond hands, blockchain, DeFi, rugpull...",
            help="Search across terms, definitions, and examples"
        )
    
    with col2:
        category_filter = st.selectbox("📂 Category", ['All'] + sorted(df['category'].unique()))
    
    with col3:
        difficulty_filter = st.selectbox("⭐ Difficulty", ['All'] + sorted(df['difficulty'].unique()))
    
    # Apply filters
    filtered_df = df.copy()
    
    if search_term:
        mask = (
            filtered_df['term'].str.contains(search_term, case=False, na=False) |
            filtered_df['definition'].str.contains(search_term, case=False, na=False) |
            filtered_df['example'].str.contains(search_term, case=False, na=False)
        )
        filtered_df = filtered_df[mask]
    
    if category_filter != 'All':
        filtered_df = filtered_df[filtered_df['category'] == category_filter]
    
    if difficulty_filter != 'All':
        filtered_df = filtered_df[filtered_df['difficulty'] == difficulty_filter]
    
    # Results
    st.subheader(f"📚 Found {len(filtered_df)} terms")
    
    for _, term in filtered_df.iterrows():
        badge_class = "memecoin-badge" if term['category'] == 'Memecoins' else "crypto-badge"
        difficulty_emoji = {'Beginner': '🟢', 'Intermediate': '🟡', 'Advanced': '🔴'}.get(term['difficulty'], '⚪')
        
        with st.expander(f"{term['term']} ({term['category']})"):
            st.markdown(f"""
            <div class="term-card">
                <h3>{term['term']} <span class="{badge_class}">{term['category']}</span></h3>
                <p><strong>📖 Definition:</strong> {term['definition']}</p>
                <p><strong>💡 Example:</strong> {term['example']}</p>
                <p><strong>{difficulty_emoji} Difficulty:</strong> {term['difficulty']} | <strong>🏷️ Tags:</strong> {', '.join(term['tags'])}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"✅ Mark as Learned", key=f"learn_{term['term']}"):
                    st.session_state.user_progress['terms_learned'].add(term['term'])
                    st.success(f"Added '{term['term']}' to your learned terms! 🎉")
            
            with col2:
                if st.button(f"🎯 Quiz Me", key=f"quiz_{term['term']}"):
                    st.session_state.current_question = term
                    st.session_state.quiz_answered = False
                    st.info("Quiz question set! Go to Interactive Quiz tab.")

elif page == "📊 Live Market Data":
    st.header("📊 Live Cryptocurrency Market Data")
    
    # Data refresh controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh Data", type="primary"):
            st.cache_data.clear()
            st.rerun()
    
    with col2:
        st.info("💡 Data refreshes automatically every 5 minutes")
    
    # Fetch and display data
    with st.spinner("🔄 Fetching live market data..."):
        prices = fetch_crypto_prices()
    
    if prices:
        st.subheader("💰 Live Cryptocurrency Prices")
        
        # Create price grid
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
                
                # Format price appropriately
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
        
        # Simple price comparison chart
        st.subheader("📈 Price Comparison")
        available_coins = [coin for coin in ['bitcoin', 'ethereum', 'dogecoin', 'shiba-inu'] if coin in prices]
        
        if available_coins:
            chart_data = pd.DataFrame({
                'Coin': [coin.replace('-', ' ').title() for coin in available_coins],
                'Price (USD)': [prices[coin]['usd'] for coin in available_coins]
            })
            st.bar_chart(chart_data.set_index('Coin'))
        
        # Market insights
        st.subheader("💡 Market Insights")
        if 'bitcoin' in prices:
            btc_change = prices['bitcoin'].get('usd_24h_change', 0)
            if btc_change > 5:
                st.success("🚀 Bitcoin is pumping! Great day for crypto!")
            elif btc_change < -5:
                st.warning("📉 Bitcoin is down today. Time to HODL!")
            else:
                st.info("📊 Bitcoin is stable today. Sideways action.")
                
    else:
        st.warning("📡 Live market data is temporarily unavailable. Please try again later.")
        st.info("💡 This usually happens when the API is down or network issues occur.")

elif page == "🎯 Interactive Quiz":
    st.header("🎯 Interactive Crypto Knowledge Quiz")
    
    # Quiz stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🎯 Score", f"{st.session_state.quiz_score}/{st.session_state.quiz_total}")
    with col2:
        if st.session_state.quiz_total > 0:
            accuracy = (st.session_state.quiz_score / st.session_state.quiz_total) * 100
            st.metric("📊 Accuracy", f"{accuracy:.1f}%")
        else:
            st.metric("📊 Accuracy", "0%")
    with col3:
        learned_count = len(st.session_state.user_progress['terms_learned'])
        st.metric("📚 Terms Learned", learned_count)
    
    # Generate new question
    if st.button("🎲 Generate New Question", type="primary", use_container_width=True):
        question = df.sample(1).iloc[0]
        st.session_state.current_question = question
        st.session_state.quiz_answered = False
        st.rerun()
    
    # Display current question
    if st.session_state.current_question is not None:
        question = st.session_state.current_question
        
        st.subheader("❓ Quiz Question")
        st.info(f"**What does '{question['term']}' mean?**")
        
        # Generate multiple choice options
        correct_answer = question['definition']
        other_terms = df[df['term'] != question['term']]
        
        if len(other_terms) >= 3:
            wrong_answers = other_terms.sample(3)['definition'].tolist()
        else:
            wrong_answers = other_terms['definition'].tolist()
        
        options = [correct_answer] + wrong_answers
        random.shuffle(options)
        
        # Radio button for answer selection
        user_answer = st.radio(
            "Choose the correct definition:",
            options,
            key="quiz_radio",
            disabled=st.session_state.quiz_answered
        )
        
        # Submit and feedback
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Submit Answer", disabled=st.session_state.quiz_answered):
                st.session_state.quiz_answered = True
                st.session_state.quiz_total += 1
                
                if user_answer == correct_answer:
                    st.session_state.quiz_score += 1
                    st.session_state.user_progress['terms_learned'].add(question['term'])
                    st.success("🎉 Correct! Well done!")
                    st.balloons()
                else:
                    st.error("❌ Incorrect. Don't worry, keep learning!")
                
                # Show correct answer and example
                st.info(f"✅ **Correct Definition:** {correct_answer}")
                st.caption(f"💡 **Example:** {question['example']}")
                
                # Show category and difficulty
                badge_class = "memecoin-badge" if question['category'] == 'Memecoins' else "crypto-badge"
                st.markdown(f"**Category:** <span class='{badge_class}'>{question['category']}</span> | **Difficulty:** {question['difficulty']}", unsafe_allow_html=True)
        
        with col2:
            if st.button("⏭️ Next Question"):
                question = df.sample(1).iloc[0]
                st.session_state.current_question = question
                st.session_state.quiz_answered = False
                st.rerun()
    else:
        st.info("👆 Click 'Generate New Question' to start the quiz!")
        
        # Show sample questions
        st.subheader("📝 Sample Questions")
        sample_terms = df.sample(3)
        for i, (_, term) in enumerate(sample_terms.iterrows(), 1):
            st.write(f"**{i}.** What does '{term['term']}' mean?")
            st.caption(f"Category: {term['category']} | Difficulty: {term['difficulty']}")

elif page == "🎲 Discovery Mode":
    st.header("🎲 Discovery Mode - Explore Crypto Terms")
    
    st.subheader("🎯 Discovery Options")
    
    # Discovery buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎲 Random Term", type="primary", use_container_width=True):
            term = df.sample(1).iloc[0]
            st.session_state.discovery_term = term
    
    with col2:
        if st.button("🐕 Random Memecoin Term", use_container_width=True):
            memecoin_terms = df[df['category'] == 'Memecoins']
            if not memecoin_terms.empty:
                term = memecoin_terms.sample(1).iloc[0]
                st.session_state.discovery_term = term
            else:
                st.warning("No memecoin terms available!")
    
    with col3:
        if st.button("⚡ Random Beginner Term", use_container_width=True):
            beginner_terms = df[df['difficulty'] == 'Beginner']
            if not beginner_terms.empty:
                term = beginner_terms.sample(1).iloc[0]
                st.session_state.discovery_term = term
            else:
                st.warning("No beginner terms available!")
    
    # Display discovered term
    if hasattr(st.session_state, 'discovery_term') and st.session_state.discovery_term is not None:
        term = st.session_state.discovery_term
        emoji = "🐕" if term['category'] == 'Memecoins' else "💰"
        difficulty_emoji = {'Beginner': '🟢', 'Intermediate': '🟡', 'Advanced': '🔴'}.get(term['difficulty'], '⚪')
        
        st.markdown(f"""
        <div class="term-card">
            <h2>{emoji} {term['term']}</h2>
            <p><strong>📖 Definition:</strong> {term['definition']}</p>
            <p><strong>💡 Example:</strong> {term['example']}</p>
            <p><strong>📂 Category:</strong> {term['category']} | <strong>{difficulty_emoji} Difficulty:</strong> {term['difficulty']}</p>
            <p><strong>🏷️ Tags:</strong> {', '.join(term['tags'])}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Learning actions
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ Mark as Learned", key="discovery_learn"):
                st.session_state.user_progress['terms_learned'].add(term['term'])
                st.success(f"Added '{term['term']}' to your learned terms! 🎉")
                st.balloons()
        
        with col2:
            if st.button("🎯 Quiz Me on This", key="discovery_quiz"):
                st.session_state.current_question = term
                st.session_state.quiz_answered = False
                st.info("Quiz question generated! Switch to 'Interactive Quiz' to answer.")
        
        with col3:
            if st.button("🔄 Discover Another", key="discovery_another"):
                new_term = df.sample(1).iloc[0]
                st.session_state.discovery_term = new_term
                st.rerun()
    
    # Category exploration
    st.subheader("📂 Explore by Category")
    
    categories = sorted(df['category'].unique())
    category_cols = st.columns(len(categories))
    
    for idx, category in enumerate(categories):
        with category_cols[idx]:
            category_count = len(df[df['category'] == category])
            if st.button(f"{category}\n({category_count} terms)", key=f"cat_{category}", use_container_width=True):
                category_terms = df[df['category'] == category]
                st.session_state.discovery_term = category_terms.sample(1).iloc[0]
                st.rerun()
    
    # Learning stats
    st.subheader("📊 Your Discovery Stats")
    
    if len(st.session_state.user_progress['terms_learned']) > 0:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            learned_count = len(st.session_state.user_progress['terms_learned'])
            st.metric("📚 Terms Learned", f"{learned_count}/{len(df)}")
        
        with col2:
            progress_percentage = (learned_count / len(df)) * 100
            st.metric("📈 Progress", f"{progress_percentage:.1f}%")
        
        with col3:
            # Calculate learning streak (simplified)
            if learned_count >= 5:
                st.metric("🔥 Learning Streak", "🔥🔥🔥")
            elif learned_count >= 3:
                st.metric("🔥 Learning Streak", "🔥🔥")
            elif learned_count >= 1:
                st.metric("🔥 Learning Streak", "🔥")
            else:
                st.metric("🔥 Learning Streak", "0")
        
        # Progress bar
        st.progress(progress_percentage / 100)
        
        # Achievement badges
        if progress_percentage >= 75:
            st.success("🏆 Achievement Unlocked: Crypto Master!")
        elif progress_percentage >= 50:
            st.success("🥇 Achievement Unlocked: Crypto Expert!")
        elif progress_percentage >= 25:
            st.success("🥈 Achievement Unlocked: Crypto Scholar!")
        elif progress_percentage >= 10:
            st.success("🥉 Achievement Unlocked: Crypto Learner!")
    else:
        st.info("Start discovering terms to see your progress!")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🚀 CryptoLearn Pro
    Master crypto terminology with interactive learning!
    
    **Features:**
    - 📚 18+ Comprehensive Terms
    - 🐕 Memecoin Culture Focus
    - 📊 Live Market Data
    - 🎯 Interactive Quizzes
    """)

with col2:
    st.markdown(f"""
    ### 📊 Your Learning Stats
    - **Terms Available:** {total_terms}
    - **Your Progress:** {len(st.session_state.user_progress['terms_learned'])}/{total_terms}
    - **Quiz Score:** {st.session_state.quiz_score}/{st.session_state.quiz_total}
    - **Categories Covered:** {categories}
    """)

with col3:
    st.markdown("""
    ### 🔗 Useful Links
    - [GitHub Repository](https://github.com/cryptokunta/cryptolearnpro)
    - [Report Issues](https://github.com/cryptokunta/cryptolearnpro/issues)
    - [CoinGecko API](https://coingecko.com/api)
    - [Streamlit Docs](https://docs.streamlit.io)
    """)

# Success celebrations
if st.session_state.quiz_score > 0:
    if st.session_state.quiz_score >= 10:
        if st.session_state.quiz_score % 10 == 0:  # Every 10 correct answers
            st.balloons()
            st.success("🎉 Congratulations! You're becoming a crypto expert!")
    elif st.session_state.quiz_score >= 5:
        if st.session_state.quiz_score % 5 == 0:  # Every 5 correct answers
            st.success("🌟 Great progress! Keep learning!")

# Performance tip
if page == "📊 Live Market Data":
    # Add a small delay to prevent excessive API calls
    time.sleep(0.1)
