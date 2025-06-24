import streamlit as st
import pandas as pd
import requests
import random

# Configure page
st.set_page_config(
    page_title="CryptoLearn Pro",
    page_icon="🚀",
    layout="wide"
)

# CSS
st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    text-align: center;
    color: white;
}
.term-card {
    background: #f8f9fa;
    border-left: 5px solid #667eea;
    padding: 1.5rem;
    margin: 1rem 0;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# Data
@st.cache_data
def load_crypto_terms():
    return pd.DataFrame([
        {
            "term": "Diamond Hands",
            "definition": "Investors who hold cryptocurrency through extreme volatility, refusing to sell despite fear or losses.",
            "example": "Diamond hands held DOGE through the 2021 crash and were rewarded later. 💎🙌",
            "category": "Memecoins",
            "difficulty": "Beginner"
        },
        {
            "term": "Paper Hands",
            "definition": "Investors who sell quickly at signs of trouble or small profits, opposite of diamond hands.",
            "example": "Paper hands sold Bitcoin at $30k and missed the rally to $60k. 📄🙌",
            "category": "Memecoins",
            "difficulty": "Beginner"
        },
        {
            "term": "HODL",
            "definition": "Hold On for Dear Life - strategy of holding cryptocurrency long-term despite volatility.",
            "example": "Bitcoin HODLers who bought in 2017 were rewarded in 2021.",
            "category": "Trading",
            "difficulty": "Beginner"
        },
        {
            "term": "FOMO",
            "definition": "Fear of Missing Out - anxiety driving impulsive buying when seeing others profit.",
            "example": "FOMO drove retail investors to buy Bitcoin at its $69k peak in 2021.",
            "category": "Psychology",
            "difficulty": "Beginner"
        },
        {
            "term": "Rugpull",
            "definition": "A scam where developers abandon a project and steal funds by removing liquidity.",
            "example": "The Squid Game token was a rugpull that cost investors millions.",
            "category": "Memecoins",
            "difficulty": "Intermediate"
        },
        {
            "term": "WAGMI",
            "definition": "We're All Gonna Make It - optimistic phrase encouraging holding through difficult times.",
            "example": "Despite being down 70%, the community stays strong: 'WAGMI!' 💪",
            "category": "Memecoins",
            "difficulty": "Beginner"
        },
        {
            "term": "Whale",
            "definition": "Individual or entity holding large amounts of crypto, capable of influencing prices.",
            "example": "A Bitcoin whale moved 40,000 BTC to exchanges, causing market concern.",
            "category": "Trading",
            "difficulty": "Beginner"
        },
        {
            "term": "DeFi",
            "definition": "Decentralized Finance - financial applications built on blockchain without intermediaries.",
            "example": "DeFi protocols like Aave allow lending without traditional banks.",
            "category": "DeFi",
            "difficulty": "Intermediate"
        },
        {
            "term": "Gas Fees",
            "definition": "Transaction fees paid to miners/validators for processing blockchain transactions.",
            "example": "Ethereum gas fees can reach $100+ during network congestion.",
            "category": "Technical",
            "difficulty": "Beginner"
        },
        {
            "term": "Smart Contract",
            "definition": "Self-executing contracts with terms directly written into code, automatically enforcing agreements.",
            "example": "Ethereum smart contracts power DeFi applications like Uniswap.",
            "category": "Blockchain",
            "difficulty": "Intermediate"
        }
    ])

# API function
@st.cache_data(ttl=300)
def fetch_crypto_prices():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': 'bitcoin,ethereum,dogecoin',
            'vs_currencies': 'usd',
            'include_24hr_change': 'true'
        }
        response = requests.get(url, params=params, timeout=10)
        return response.json()
    except:
        return None

# Initialize session state
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'quiz_total' not in st.session_state:
    st.session_state.quiz_total = 0

# Load data
df = load_crypto_terms()

# Header
st.markdown("""
<div class="main-header">
    <h1>🚀 CryptoLearn Pro</h1>
    <h3>Master Crypto & Memecoin Terminology</h3>
    <p>🎯 Learn • 📈 Track • 🎮 Practice</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("### 🧭 Navigation")
page = st.sidebar.selectbox("Choose:", [
    "🏠 Dashboard",
    "🔍 Term Explorer", 
    "📊 Live Prices",
    "🎯 Quiz"
])

# Stats
st.sidebar.markdown("### 📊 Stats")
st.sidebar.metric("📚 Terms", len(df))
st.sidebar.metric("🐕 Memecoins", len(df[df['category'] == 'Memecoins']))
st.sidebar.metric("🎯 Quiz Score", f"{st.session_state.quiz_score}/{st.session_state.quiz_total}")

# Main content
if page == "🏠 Dashboard":
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📚 Total Terms", len(df))
    with col2:
        st.metric("🐕 Memecoin Terms", len(df[df['category'] == 'Memecoins']))
    with col3:
        st.metric("📂 Categories", df['category'].nunique())
    
    st.subheader("🚀 Quick Actions")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎲 Random Term"):
            term = df.sample(1).iloc[0]
            st.success(f"🐕 **{term['term']}** ({term['category']})")
            st.info(term['definition'])
            st.caption(f"💡 {term['example']}")
    
    with col2:
        if st.button("📈 Live Bitcoin Price"):
            prices = fetch_crypto_prices()
            if prices and 'bitcoin' in prices:
                btc = prices['bitcoin']
                change = btc.get('usd_24h_change', 0)
                st.metric("Bitcoin", f"${btc['usd']:,.2f}", f"{change:.2f}%")
            else:
                st.info("Live data unavailable")

elif page == "🔍 Term Explorer":
    st.header("🔍 Term Explorer")
    
    search = st.text_input("🔍 Search terms...")
    category = st.selectbox("📂 Category", ['All'] + list(df['category'].unique()))
    
    filtered_df = df.copy()
    
    if search:
        mask = (
            filtered_df['term'].str.contains(search, case=False, na=False) |
            filtered_df['definition'].str.contains(search, case=False, na=False)
        )
        filtered_df = filtered_df[mask]
    
    if category != 'All':
        filtered_df = filtered_df[filtered_df['category'] == category]
    
    st.subheader(f"Found {len(filtered_df)} terms")
    
    for _, term in filtered_df.iterrows():
        st.markdown(f"""
        <div class="term-card">
            <h3>{term['term']} ({term['category']})</h3>
            <p><strong>Definition:</strong> {term['definition']}</p>
            <p><strong>Example:</strong> {term['example']}</p>
            <p><strong>Difficulty:</strong> {term['difficulty']}</p>
        </div>
        """, unsafe_allow_html=True)

elif page == "📊 Live Prices":
    st.header("📊 Live Cryptocurrency Prices")
    
    if st.button("🔄 Refresh"):
        st.cache_data.clear()
        st.rerun()
    
    prices = fetch_crypto_prices()
    
    if prices:
        col1, col2, col3 = st.columns(3)
        
        coins = ['bitcoin', 'ethereum', 'dogecoin']
        names = ['Bitcoin', 'Ethereum', 'Dogecoin']
        
        for i, (coin, name) in enumerate(zip(coins, names)):
            if coin in prices:
                data = prices[coin]
                price = data.get('usd', 0)
                change = data.get('usd_24h_change', 0)
                
                with [col1, col2, col3][i]:
                    st.metric(name, f"${price:,.2f}", f"{change:.2f}%")
    else:
        st.warning("Live data temporarily unavailable")

elif page == "🎯 Quiz":
    st.header("🎯 Interactive Quiz")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Score", f"{st.session_state.quiz_score}/{st.session_state.quiz_total}")
    with col2:
        if st.session_state.quiz_total > 0:
            accuracy = (st.session_state.quiz_score / st.session_state.quiz_total) * 100
            st.metric("Accuracy", f"{accuracy:.1f}%")
    
    if st.button("🎲 New Question"):
        question = df.sample(1).iloc[0]
        st.session_state.current_question = question
        st.session_state.quiz_answered = False
        st.rerun()
    
    if hasattr(st.session_state, 'current_question'):
        question = st.session_state.current_question
        
        st.subheader("❓ Question")
        st.info(f"What does **{question['term']}** mean?")
        
        # Generate options
        correct = question['definition']
        wrong = df[df['term'] != question['term']].sample(2)['definition'].tolist()
        options = [correct] + wrong
        random.shuffle(options)
        
        answer = st.radio("Choose:", options)
        
        if st.button("Submit") and not getattr(st.session_state, 'quiz_answered', False):
            st.session_state.quiz_answered = True
            st.session_state.quiz_total += 1
            
            if answer == correct:
                st.session_state.quiz_score += 1
                st.success("🎉 Correct!")
            else:
                st.error("❌ Wrong!")
                st.info(f"Correct: {correct}")
            
            st.info(f"Example: {question['example']}")

# Footer
st.markdown("---")
st.markdown("### 🚀 CryptoLearn Pro - Master Crypto Terminology!")
st.markdown("Made with ❤️ for the crypto community")
