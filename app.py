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

# CSS styling
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
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem;
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

# Load crypto terms
@st.cache_data
def load_crypto_terms():
    terms_data = [
        {
            "term": "Diamond Hands",
            "definition": "Investors who hold cryptocurrency through extreme volatility, refusing to sell despite fear or losses.",
            "example": "Diamond hands held DOGE through the 2021 crash and were rewarded later. 💎🙌",
            "category": "Memecoins",
            "difficulty": "Beginner"
        },        {
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
            "term": "FUD",
            "definition": "Fear, Uncertainty, and Doubt - negative information spread to damage crypto reputation.",
            "example": "China's mining ban created FUD that temporarily crashed Bitcoin prices.",
            "category": "Psychology",
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
            "term": "To the Moon",
            "definition": "Expression indicating belief that a cryptocurrency's price will rise dramatically.",
            "example": "The community chanted 'DOGE to the moon!' during the 2021 rally. 🚀🌙",
            "category": "Memecoins",
            "difficulty": "Beginner"
        }
    ]
    return pd.DataFrame(terms_data)
# Initialize session state - SIMPLE VERSION
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'quiz_total' not in st.session_state:
    st.session_state.quiz_total = 0
if 'terms_learned' not in st.session_state:
    st.session_state.terms_learned = set()

# Load data
df = load_crypto_terms()

# Header
st.markdown("""
<div class="main-header">
    <h1>🚀 CryptoLearn Pro</h1>
    <h3>Master Crypto & Memecoin Terminology</h3>
    <p>🎯 Learn • 📊 Track • 🎮 Practice • 🌟 Master</p>
</div>
""", unsafe_allow_html=True)

# Dashboard
st.subheader("📊 Your Learning Journey")

col1, col2, col3 = st.columns(3)

with col1:
    total_terms = len(df)
    st.markdown(f"""
    <div class="metric-card">
        <h3>📚 Total Terms</h3>
        <h1>{total_terms}</h1>
        <p>Available to learn</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    learned_count = len(st.session_state.terms_learned)
    st.markdown(f"""
    <div class="metric-card">
        <h3>✅ Learned</h3>
        <h1>{learned_count}</h1>
        <p>Your progress</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    memecoins = len(df[df['category'] == 'Memecoins'])
    st.markdown(f"""
    <div class="metric-card">
        <h3>🐕 Memecoins</h3>
        <h1>{memecoins}</h1>
        <p>Culture terms</p>
    </div>
    """, unsafe_allow_html=True)

# Quick Actions
st.subheader("🚀 Quick Actions")
col1, col2 = st.columns(2)

with col1:
    if st.button("🎲 Learn Random Term", use_container_width=True):
        term = df.sample(1).iloc[0]
        emoji = "🐕" if term['category'] == 'Memecoins' else "💰"
        st.success(f"{emoji} **{term['term']}**")
        st.info(term['definition'])
        st.caption(f"💡 {term['example']}")
        st.session_state.terms_learned.add(term['term'])

with col2:
    if st.button("🎯 Start Quiz", use_container_width=True):
        st.session_state.current_question = df.sample(1).iloc[0]
        st.info("Quiz question loaded! See below.")

# Quiz Section
if 'current_question' in st.session_state and st.session_state.current_question is not None:
    st.subheader("🎯 Quiz Time")
    question = st.session_state.current_question
    
    st.info(f"**What does '{question['term']}' mean?**")
    
    # Generate options
    correct_answer = question['definition']
    wrong_answers = df[df['term'] != question['term']].sample(min(3, len(df)-1))['definition'].tolist()
    options = [correct_answer] + wrong_answers
    random.shuffle(options)
    
    user_answer = st.radio("Choose the correct definition:", options, key="quiz_radio")
    
    if st.button("✅ Submit Answer"):
        st.session_state.quiz_total += 1
        
        if user_answer == correct_answer:
            st.session_state.quiz_score += 1
            st.session_state.terms_learned.add(question['term'])
            st.success("🎉 Correct! Well done!")
        else:
            st.error("❌ Not quite right, but keep learning!")
        
        st.info(f"✅ **Correct Answer:** {correct_answer}")
        st.caption(f"💡 **Example:** {question['example']}")

# Terms Explorer
st.subheader("🔍 Explore All Terms")

for _, term in df.iterrows():
    is_learned = term['term'] in st.session_state.terms_learned
    status = "✅ Learned" if is_learned else "📖 New"
    
    with st.expander(f"{term['term']} ({term['category']}) - {status}"):
        st.markdown(f"""
        <div class="term-card">
            <h3>{term['term']}</h3>
            <p><strong>📖 Definition:</strong> {term['definition']}</p>
            <p><strong>💡 Example:</strong> {term['example']}</p>
            <p><strong>📂 Category:</strong> {term['category']} | <strong>⭐ Difficulty:</strong> {term['difficulty']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not is_learned:
            if st.button(f"✅ Mark as Learned", key=f"learn_{term['term']}"):
                st.session_state.terms_learned.add(term['term'])
                st.success("Added to learned terms! 🎉")
                st.rerun()

# Footer
st.markdown("---")
if learned_count > 0:
    progress = (learned_count / total_terms) * 100
    st.success(f"🎉 Progress: {progress:.1f}% ({learned_count}/{total_terms} terms learned)")

st.markdown("### 🚀 CryptoLearn Pro - Master Crypto Terminology")
st.markdown("Made with ❤️ for the crypto community")
