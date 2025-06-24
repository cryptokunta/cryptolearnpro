import streamlit as st
import pandas as pd
import requests
import random
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass
import plotly.express as px
import plotly.graph_objects as go

# Configure page
st.set_page_config(
    page_title="CryptoLearn Pro - Live Terminology Ecosystem",
    page_icon="🚀",
    layout="wide"
)

@dataclass
class CryptoTerm:
    term: str
    definition: str
    example: str
    category: str
    difficulty: str
    tags: List[str]
    importance: str
    trending_score: int = 0
    last_updated: str = datetime.now().strftime("%Y-%m-%d")

class TerminologyAggregator:
    def __init__(self):
        self.terms = self.load_base_terms()
    
    def load_base_terms(self):
        """Load comprehensive crypto terminology"""
        return [
            CryptoTerm("Diamond Hands", "Hold through extreme volatility", "💎🙌 DOGE diamond hands got rewarded", "Memecoins", "Beginner", ["culture", "holding"], "High", 95),
            CryptoTerm("Paper Hands", "Sell quickly on fear/small profits", "📄🙌 Paper hands sold BTC at 30k", "Memecoins", "Beginner", ["culture", "selling"], "High", 88),
            CryptoTerm("To the Moon", "Price will rise dramatically", "🚀🌙 DOGE to the moon!", "Memecoins", "Beginner", ["bullish", "price"], "High", 92),
            CryptoTerm("Rugpull", "Scam exit stealing liquidity", "SQUID token was a massive rugpull", "Memecoins", "Critical", ["scam", "danger"], "Critical", 75),
            CryptoTerm("WAGMI", "We're All Gonna Make It", "💪 Down 70% but WAGMI!", "Memecoins", "Beginner", ["optimism", "community"], "Medium", 85),
            CryptoTerm("NGMI", "Not Gonna Make It", "Selling at bottom? NGMI behavior", "Memecoins", "Beginner", ["pessimism"], "Medium", 65),
            CryptoTerm("Ape In", "Invest heavily without research", "Retail aped into memecoins", "Memecoins", "Beginner", ["impulsive", "fomo"], "Medium", 78),
            CryptoTerm("Degen", "High-risk crypto gambler", "Degens buying random shitcoins", "Memecoins", "Beginner", ["culture", "risky"], "Medium", 82),
            CryptoTerm("Chad", "Confident successful investor", "Chad bought BTC at 3k", "Memecoins", "Beginner", ["confidence", "success"], "Medium", 70),
            CryptoTerm("HODL", "Hold On for Dear Life", "Bitcoin HODLers rewarded in 2021", "Trading", "Beginner", ["strategy", "patience"], "Critical", 90),
            CryptoTerm("FOMO", "Fear of Missing Out", "FOMO drove buying at ATH", "Psychology", "Beginner", ["emotion", "psychology"], "Critical", 85),
            CryptoTerm("FUD", "Fear, Uncertainty, Doubt", "China ban created FUD", "Psychology", "Beginner", ["negativity", "manipulation"], "Critical", 80),
            CryptoTerm("Whale", "Large crypto holder", "Whale moved 40k BTC", "Trading", "Beginner", ["market_impact"], "High", 75),
            CryptoTerm("Rekt", "Totally destroyed/liquidated", "Got rekt on 100x leverage", "Trading", "Beginner", ["loss", "liquidation"], "High", 85),
            CryptoTerm("Moon Boy", "Extreme price optimist", "Moon boys calling $1M Bitcoin", "Culture", "Beginner", ["optimism", "price"], "Medium", 60),
            CryptoTerm("Bag Holder", "Stuck with worthless tokens", "ICP bag holders down 99%", "Trading", "Beginner", ["loss", "stuck"], "Medium", 65),
            CryptoTerm("Pump and Dump", "Artificial price manipulation", "Classic pump and dump scheme", "Trading", "Critical", ["scam", "manipulation"], "Critical", 70),
            CryptoTerm("DeFi", "Decentralized Finance", "DeFi protocols like Aave", "Technology", "Intermediate", ["finance", "decentralized"], "High", 88),
            CryptoTerm("Smart Contract", "Self-executing code contracts", "Ethereum smart contracts", "Technology", "Intermediate", ["ethereum", "automation"], "Critical", 85),
            CryptoTerm("Gas Fees", "Transaction processing fees", "ETH gas fees $100+", "Technology", "Beginner", ["fees", "network"], "High", 75),
            CryptoTerm("Staking", "Lock tokens for rewards", "ETH 2.0 staking rewards", "Technology", "Intermediate", ["rewards", "validation"], "High", 80),
            CryptoTerm("Yield Farming", "Maximize DeFi returns", "Yield farming 100%+ APY", "DeFi", "Advanced", ["farming", "rewards"], "High", 70),
            CryptoTerm("Liquidity Pool", "Token pairs for trading", "Uniswap liquidity pools", "DeFi", "Advanced", ["liquidity", "trading"], "High", 65),
            CryptoTerm("Impermanent Loss", "LP value vs holding", "IL risk in volatile pairs", "DeFi", "Advanced", ["risk", "loss"], "High", 60),
            CryptoTerm("Private Key", "Secret wallet control", "Not your keys, not your crypto", "Security", "Beginner", ["security", "control"], "Critical", 90),
        ]
    
    @st.cache_data(ttl=300)
    def get_trending_crypto_data(_self):
        """Fetch live trending crypto data"""
        try:
            trending_url = "https://api.coingecko.com/api/v3/search/trending"
            price_url = "https://api.coingecko.com/api/v3/simple/price"
            
            trending_response = requests.get(trending_url, timeout=10)
            
            if trending_response.status_code == 200:
                trending_data = trending_response.json()
                
                # Get coin IDs for price data
                coin_ids = [coin['item']['id'] for coin in trending_data['coins'][:10]]
                
                price_params = {
                    'ids': ','.join(coin_ids),
                    'vs_currencies': 'usd',
                    'include_24hr_change': 'true'
                }
                
                price_response = requests.get(price_url, params=price_params, timeout=10)
                price_data = price_response.json() if price_response.status_code == 200 else {}
                
                return trending_data, price_data
            
        except Exception as e:
            st.warning(f"📡 Live data temporarily unavailable")
            return None, None
        
        return None, None

# Initialize the aggregator
@st.cache_resource
def get_aggregator():
    return TerminologyAggregator()

aggregator = get_aggregator()

# Session state initialization - FIXED
if 'terms_learned' not in st.session_state:
    st.session_state.terms_learned = set()
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'quiz_total' not in st.session_state:
    st.session_state.quiz_total = 0
if 'user_streak' not in st.session_state:
    st.session_state.user_streak = 0

# Header
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; text-align: center; color: white; margin-bottom: 2rem;">
    <h1>🚀 CryptoLearn Pro - Live Terminology Ecosystem</h1>
    <h3>Real-Time Crypto Culture & Memecoin Dictionary</h3>
    <p>🔥 Trending • 📊 Live Data • 🎯 Adaptive Learning • 🌍 Community Driven</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with live stats
st.sidebar.markdown("### 🔥 Live Ecosystem Stats")

# Get trending data
trending_data, price_data = aggregator.get_trending_crypto_data()

if trending_data:
    st.sidebar.success("📡 Live Data Connected")
    trending_coins = trending_data.get('coins', [])[:5]
    
    st.sidebar.markdown("#### 🚀 Trending Now:")
    for coin in trending_coins:
        coin_data = coin['item']
        coin_id = coin_data['id']
        
        # Get price if available
        price_info = ""
        if price_data and coin_id in price_data:
            price = price_data[coin_id].get('usd', 0)
            change = price_data[coin_id].get('usd_24h_change', 0)
            price_info = f"${price:,.6f} ({change:+.1f}%)"
        
        st.sidebar.write(f"**{coin_data['symbol']}** {coin_data['name']}")
        if price_info:
            st.sidebar.caption(price_info)
else:
    st.sidebar.warning("📡 Connecting to live data...")

# User stats
total_terms = len(aggregator.terms)
learned_count = len(st.session_state.terms_learned)
progress_pct = (learned_count / total_terms) * 100

st.sidebar.markdown("#### 🎯 Your Progress")
st.sidebar.metric("📚 Terms Learned", f"{learned_count}/{total_terms}")
st.sidebar.metric("🎯 Quiz Accuracy", f"{(st.session_state.quiz_score/max(st.session_state.quiz_total,1)*100):.0f}%")
st.sidebar.metric("🔥 Streak", st.session_state.user_streak)

if learned_count > 0:
    st.sidebar.progress(progress_pct / 100)
    st.sidebar.caption(f"{progress_pct:.1f}% Complete")

# Main navigation
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 Dashboard", "🔥 Trending Terms", "🎯 Smart Quiz", "📊 Visualizations", "🔍 Term Explorer"])

with tab1:
    st.subheader("🌍 Live Crypto Terminology Ecosystem")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📚 Total Terms", total_terms, help="Comprehensive terminology database")
    
    with col2:
        meme_count = len([t for t in aggregator.terms if t.category == "Memecoins"])
        st.metric("🐕 Meme Culture", meme_count, help="Memecoin and culture terms")
    
    with col3:
        critical_count = len([t for t in aggregator.terms if t.importance == "Critical"])
        st.metric("⚡ Critical Terms", critical_count, help="Essential knowledge")
    
    with col4:
        avg_trending = sum(t.trending_score for t in aggregator.terms) / len(aggregator.terms)
        st.metric("🔥 Avg Trending", f"{avg_trending:.0f}", help="Community interest score")
    
    # Quick actions
    st.subheader("🚀 Quick Learning Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎲 Discover Trending Term", use_container_width=True):
            # Get highest trending terms
            trending_terms = sorted(aggregator.terms, key=lambda x: x.trending_score, reverse=True)[:5]
            term = random.choice(trending_terms)
            
            emoji = "🐕" if term.category == "Memecoins" else "💰"
            st.success(f"{emoji} **{term.term}** (🔥 {term.trending_score})")
            st.info(f"📖 {term.definition}")
            st.caption(f"💡 {term.example}")
            
            if term.term not in st.session_state.terms_learned:
                if st.button("✅ Mark as Learned", key="trending_learn"):
                    st.session_state.terms_learned.add(term.term)
                    st.balloons()
    
    with col2:
        if st.button("🔥 Show Live Market Pulse", use_container_width=True):
            if trending_data:
                st.subheader("📈 Live Market Pulse")
                
                # Create trending visualization
                coins_data = []
                for coin in trending_data['coins'][:8]:
                    coin_info = coin['item']
                    coin_id = coin_info['id']
                    
                    price_change = 0
                    if price_data and coin_id in price_data:
                        price_change = price_data[coin_id].get('usd_24h_change', 0)
                    
                    coins_data.append({
                        'name': coin_info['name'],
                        'symbol': coin_info['symbol'],
                        'rank': coin_info.get('market_cap_rank', 999),
                        'change_24h': price_change
                    })
                
                if coins_data:
                    df_trending = pd.DataFrame(coins_data)
                    
                    fig = px.bar(
                        df_trending,
                        x='symbol',
                        y='change_24h',
                        color='change_24h',
                        color_continuous_scale=['red', 'yellow', 'green'],
                        title="🔥 Trending Coins - 24h Performance",
                        labels={'change_24h': '24h Change (%)', 'symbol': 'Coin'}
                    )
                    fig.update_layout(height=400, showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("📡 Connecting to live market data...")
    
    with col3:
        if st.button("🧠 Adaptive Quiz", use_container_width=True):
            st.session_state.quiz_mode = "adaptive"
            st.info("🎯 Adaptive quiz mode activated! Go to Smart Quiz tab.")

with tab2:
    st.subheader("🔥 Trending Crypto Terms & Market Context")
    
    # Show trending terms
    trending_terms = sorted(aggregator.terms, key=lambda x: x.trending_score, reverse=True)
    
    st.markdown("### 📈 Hottest Terms Right Now")
    
    for i, term in enumerate(trending_terms[:10]):
        with st.expander(f"#{i+1} {term.term} 🔥 {term.trending_score}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                badge_class = "🐕" if term.category == "Memecoins" else "💰"
                st.markdown(f"""
                **{badge_class} {term.term}** ({term.category})
                
                📖 **Definition:** {term.definition}
                
                💡 **Example:** {term.example}
                
                🏷️ **Tags:** {', '.join(term.tags)}
                """)
            
            with col2:
                st.metric("🔥 Trending Score", term.trending_score)
                st.caption(f"⭐ {term.difficulty}")
                st.caption(f"🎯 {term.importance}")
                
                if term.term not in st.session_state.terms_learned:
                    if st.button("✅ Learn", key=f"trending_{i}"):
                        st.session_state.terms_learned.add(term.term)
                        st.success("Added to learned! 🎉")
                        st.rerun()

with tab3:
    st.subheader("🎯 Adaptive Smart Quiz")
    
    quiz_col1, quiz_col2, quiz_col3 = st.columns(3)
    
    with quiz_col1:
        if st.button("🧠 Smart Question", type="primary"):
            # Adaptive quiz logic
            unlearned_terms = [t for t in aggregator.terms if t.term not in st.session_state.terms_learned]
            
            if unlearned_terms:
                # Prioritize high-importance unlearned terms
                critical_unlearned = [t for t in unlearned_terms if t.importance == "Critical"]
                trending_unlearned = sorted(unlearned_terms, key=lambda x: x.trending_score, reverse=True)[:5]
                
                if critical_unlearned and random.random() < 0.4:
                    question = random.choice(critical_unlearned)
                    quiz_type = "🔴 Critical Knowledge"
                elif trending_unlearned and random.random() < 0.6:
                    question = random.choice(trending_unlearned)
                    quiz_type = "🔥 Trending Focus"
                else:
                    question = random.choice(unlearned_terms)
                    quiz_type = "📚 General Learning"
            else:
                question = random.choice(aggregator.terms)
                quiz_type = "🏆 Mastery Review"
            
            st.session_state.current_question = question
            st.session_state.quiz_type = quiz_type
            st.session_state.quiz_answered = False
            st.rerun()
    
    if hasattr(st.session_state, 'current_question'):
        question = st.session_state.current_question
        quiz_type = getattr(st.session_state, 'quiz_type', '🎯 Quiz')
        
        st.info(f"**{quiz_type}** • 🔥 Trending: {question.trending_score}")
        st.subheader(f"❓ What does '{question.term}' mean?")
        
        # Generate smart options
        correct_answer = question.definition
        
        # Get wrong answers from same category first
        same_category = [t for t in aggregator.terms if t.category == question.category and t.term != question.term]
        other_terms = [t for t in aggregator.terms if t.term != question.term]
        
        if len(same_category) >= 2:
            wrong_answers = random.sample(same_category, 2)
            wrong_answers.append(random.choice(other_terms))
        else:
            wrong_answers = random.sample(other_terms, 3)
        
        options = [correct_answer] + [t.definition for t in wrong_answers]
        random.shuffle(options)
        
        user_answer = st.radio("Choose the correct definition:", options, key="smart_quiz")
        
        if st.button("✅ Submit Answer", disabled=getattr(st.session_state, 'quiz_answered', False)):
            st.session_state.quiz_answered = True
            st.session_state.quiz_total += 1
            
            if user_answer == correct_answer:
                st.session_state.quiz_score += 1
                st.session_state.user_streak += 1
                st.session_state.terms_learned.add(question.term)
                
                st.success("🎉 Correct! Excellent work!")
                if question.importance == "Critical":
                    st.balloons()
                    st.success("🔴 Critical term mastered!")
                
                if st.session_state.user_streak % 5 == 0:
                    st.success(f"🔥 {st.session_state.user_streak} correct in a row!")
            else:
                st.session_state.user_streak = 0
                st.error("❌ Not quite right, but keep learning!")
            
            st.info(f"✅ **Correct Answer:** {correct_answer}")
            st.caption(f"💡 **Example:** {question.example}")
            st.caption(f"🏷️ **Tags:** {', '.join(question.tags)}")

with tab4:
    st.subheader("📊 Crypto Terminology Ecosystem Visualizations")
    
    # Create visualizations
    df_terms = pd.DataFrame([{
        'term': t.term,
        'category': t.category,
        'difficulty': t.difficulty,
        'importance': t.importance,
        'trending_score': t.trending_score,
        'learned': t.term in st.session_state.terms_learned
    } for t in aggregator.terms])
    
    vis_col1, vis_col2 = st.columns(2)
    
    with vis_col1:
        # Category distribution
        category_counts = df_terms['category'].value_counts()
        fig_cat = px.pie(
            values=category_counts.values,
            names=category_counts.index,
            title="📂 Terms by Category",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_cat, use_container_width=True)
    
    with vis_col2:
        # Trending heatmap
        fig_trending = px.scatter(
            df_terms,
            x='category',
            y='trending_score',
            size='trending_score',
            color='importance',
            hover_data=['term'],
            title="🔥 Trending Score by Category",
            color_discrete_map={'Critical': 'red', 'High': 'orange', 'Medium': 'yellow'}
        )
        fig_trending.update_layout(height=400)
        st.plotly_chart(fig_trending, use_container_width=True)
    
    # Learning progress visualization
    st.markdown("### 🎯 Your Learning Progress")
    
    progress_data = df_terms.groupby('category').agg({
        'learned': ['sum', 'count']
    }).round(2)
    progress_data.columns = ['Learned', 'Total']
    progress_data['Progress %'] = (progress_data['Learned'] / progress_data['Total'] * 100).round(1)
    
    fig_progress = px.bar(
        progress_data.reset_index(),
        x='category',
        y=['Learned', 'Total'],
        title="📈 Learning Progress by Category",
        barmode='group'
    )
    st.plotly_chart(fig_progress, use_container_width=True)

with tab5:
    st.subheader("🔍 Complete Term Explorer")
    
    # Filters
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        category_filter = st.selectbox("📂 Category", ['All'] + sorted(set(t.category for t in aggregator.terms)))
    
    with filter_col2:
        difficulty_filter = st.selectbox("⭐ Difficulty", ['All'] + sorted(set(t.difficulty for t in aggregator.terms)))
    
    with filter_col3:
        importance_filter = st.selectbox("🎯 Importance", ['All'] + sorted(set(t.importance for t in aggregator.terms)))
    
    # Search
    search_term = st.text_input("🔍 Search terms, definitions, or examples...")
    
    # Apply filters
    filtered_terms = aggregator.terms
    
    if category_filter != 'All':
        filtered_terms = [t for t in filtered_terms if t.category == category_filter]
    
    if difficulty_filter != 'All':
        filtered_terms = [t for t in filtered_terms if t.difficulty == difficulty_filter]
    
    if importance_filter != 'All':
        filtered_terms = [t for t in filtered_terms if t.importance == importance_filter]
    
    if search_term:
        search_lower = search_term.lower()
        filtered_terms = [t for t in filtered_terms if 
                         search_lower in t.term.lower() or 
                         search_lower in t.definition.lower() or 
                         search_lower in t.example.lower()]
    
    st.markdown(f"### 📚 Found {len(filtered_terms)} terms")
    
    # Sort by trending score
    filtered_terms = sorted(filtered_terms, key=lambda x: x.trending_score, reverse=True)
    
    for term in filtered_terms:
        is_learned = term.term in st.session_state.terms_learned
        
        with st.expander(f"{'✅' if is_learned else '📖'} {term.term} (🔥 {term.trending_score})"):
            term_col1, term_col2 = st.columns([3, 1])
            
            with term_col1:
                emoji = "🐕" if term.category == "Memecoins" else "💰"
                importance_emoji = {"Critical": "🔴", "High": "🟡", "Medium": "⚪"}.get(term.importance, "⚪")
                
                st.markdown(f"""
                **{emoji} {term.term}**
                
                📖 **Definition:** {term.definition}
                
                💡 **Example:** {term.example}
                
                📂 **Category:** {term.category} | ⭐ **Difficulty:** {term.difficulty} | {importance_emoji} **Importance:** {term.importance}
                
                🏷️ **Tags:** {', '.join(term.tags)}
                
                📅 **Last Updated:** {term.last_updated}
                """)
            
            with term_col2:
                st.metric("🔥 Trending", term.trending_score)
                
                if not is_learned:
                    if st.button("✅ Learn This", key=f"explorer_{term.term}"):
                        st.session_state.terms_learned.add(term.term)
                        st.success("Added to learned terms! 🎉")
                        st.rerun()
                else:
                    st.success("✅ Learned!")

# Footer
st.markdown("---")
st.markdown(f"""
### 🚀 CryptoLearn Pro - Live Terminology Ecosystem
**📊 Progress:** {learned_count}/{total_terms} terms learned ({progress_pct:.1f}%)  
**🎯 Quiz Performance:** {st.session_state.quiz_score}/{st.session_state.quiz_total} correct  
**🔥 Current Streak:** {st.session_state.user_streak}

*Real-time crypto culture dictionary powered by community trends*
""")
