import streamlit as st
import pandas as pd
import requests
import random
import time
import json
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Optional

# Configure page
st.set_page_config(
    page_title="CryptoLearn Pro - Master Crypto & Web3",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://cryptolearn.pro/help',
        'Report a bug': "https://github.com/cryptokunta/cryptolearnpro/issues",
        'About': "# CryptoLearn Pro\nThe most comprehensive crypto education platform"
    }
)

# Advanced CSS styling for professional look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 100%);
        pointer-events: none;
    }
    
    .value-prop-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(245, 87, 108, 0.3);
        transform: translateY(0);
        transition: transform 0.3s ease;
    }
    
    .value-prop-card:hover {
        transform: translateY(-5px);
    }
    
    .feature-card {
        background: white;
        border: 1px solid #e1e5e9;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border-left: 4px solid #667eea;
    }
    
    .feature-card:hover {
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    .learning-path-card {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(86, 171, 47, 0.3);
    }
    
    .term-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .term-card:hover {
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        transform: translateY(-3px);
    }
    
    .progress-bar {
        background: #f0f2f6;
        border-radius: 10px;
        height: 12px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    .achievement-badge {
        display: inline-block;
        background: linear-gradient(45deg, #ffd700, #ffed4e);
        color: #333;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 600;
        margin: 0.25rem;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
    }
    
    .market-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    .market-card:hover {
        transform: translateY(-5px);
    }
    
    .quiz-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .cta-button {
        background: linear-gradient(90deg, #ff6b6b 0%, #feca57 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3);
    }
    
    .cta-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(255, 107, 107, 0.4);
    }
    
    .testimonial-card {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        border-left: 4px solid #28a745;
        font-style: italic;
    }
    
    .pricing-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        text-align: center;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .pricing-card.featured {
        border-color: #667eea;
        transform: scale(1.05);
    }
    
    .pricing-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# Comprehensive crypto education database
@st.cache_data
def load_comprehensive_crypto_database():
    """Load the most comprehensive crypto education database"""
    return {
        "memecoin_culture": [
            {
                "term": "Diamond Hands",
                "definition": "Investors who hold through extreme volatility, never selling despite fear or significant losses.",
                "example": "Diamond hands held DOGE from $0.002 to $0.70 during the 2021 rally. 💎🙌",
                "category": "Memecoin Culture",
                "difficulty": "Beginner",
                "importance": "Critical",
                "real_world_value": "Understanding market psychology and long-term investing discipline",
                "earnings_potential": "High - Prevents panic selling during dips",
                "tags": ["psychology", "holding", "discipline", "investing"]
            },
            {
                "term": "Paper Hands",
                "definition": "Investors who sell quickly at first sign of trouble or small profits, lacking conviction.",
                "example": "Paper hands sold Bitcoin at $30k in 2022 and missed the 2024 rally to $70k+. 📄🙌",
                "category": "Memecoin Culture", 
                "difficulty": "Beginner",
                "importance": "High",
                "real_world_value": "Recognizing emotional trading mistakes to avoid",
                "earnings_potential": "Medium - Avoiding early exits improves returns",
                "tags": ["psychology", "selling", "fear", "mistakes"]
            },
            {
                "term": "To the Moon",
                "definition": "Battle cry indicating belief that a cryptocurrency will achieve massive price appreciation.",
                "example": "GameStop and DOGE communities united with 'To the Moon!' 🚀🌙",
                "category": "Memecoin Culture",
                "difficulty": "Beginner", 
                "importance": "Medium",
                "real_world_value": "Understanding community-driven price movements",
                "earnings_potential": "Medium - Spotting momentum trends early",
                "tags": ["bullish", "community", "hype", "momentum"]
            },
            {
                "term": "Ape In",
                "definition": "Investing heavily without research, driven by FOMO and social media hype.",
                "example": "Retail investors aped into SHIB after seeing 1000x gains stories on TikTok.",
                "category": "Memecoin Culture",
                "difficulty": "Beginner",
                "importance": "Critical",
                "real_world_value": "Recognizing impulsive behavior that leads to losses",
                "earnings_potential": "High - Avoiding FOMO saves money",
                "tags": ["impulsive", "fomo", "risky", "social_media"]
            },
            {
                "term": "Rugpull",
                "definition": "Exit scam where developers abandon project and steal investor funds.",
                "example": "Squid Game token rugpulled for $3.3M, token became worthless in minutes.",
                "category": "Memecoin Culture",
                "difficulty": "Intermediate",
                "importance": "Critical",
                "real_world_value": "Identifying scams before losing money",
                "earnings_potential": "Critical - Prevents total loss of investment",
                "tags": ["scam", "fraud", "security", "due_diligence"]
            },
            {
                "term": "WAGMI",
                "definition": "We're All Gonna Make It - community rallying cry during difficult times.",
                "example": "Despite 80% portfolio drop, NFT community stayed strong: 'WAGMI!' 💪",
                "category": "Memecoin Culture",
                "difficulty": "Beginner",
                "importance": "Medium",
                "real_world_value": "Building resilience and community support",
                "earnings_potential": "Medium - Maintains conviction during downturns",
                "tags": ["optimism", "community", "resilience", "support"]
            }
        ],
        
        "defi_revolution": [
            {
                "term": "DeFi",
                "definition": "Decentralized Finance - financial services without traditional banks or intermediaries.",
                "example": "Uniswap enables trading without KYC, Aave offers loans without credit checks.",
                "category": "DeFi",
                "difficulty": "Intermediate",
                "importance": "Critical",
                "real_world_value": "Access to global financial services 24/7",
                "earnings_potential": "Very High - New income streams through yield farming",
                "tags": ["decentralized", "finance", "innovation", "yield"]
            },
            {
                "term": "Yield Farming",
                "definition": "Earning rewards by providing liquidity to decentralized protocols.",
                "example": "Compound offered 20%+ APY for lending USDC during DeFi summer 2020.",
                "category": "DeFi",
                "difficulty": "Advanced",
                "importance": "High",
                "real_world_value": "Passive income generation from crypto holdings",
                "earnings_potential": "Very High - 5-50%+ annual returns possible",
                "tags": ["farming", "liquidity", "rewards", "passive_income"]
            },
            {
                "term": "Impermanent Loss",
                "definition": "Temporary loss from providing liquidity when token prices diverge significantly.",
                "example": "ETH/USDC LP lost 5% when ETH pumped 50% due to impermanent loss.",
                "category": "DeFi",
                "difficulty": "Advanced",
                "importance": "Critical",
                "real_world_value": "Understanding risks in liquidity provision",
                "earnings_potential": "Critical - Prevents unexpected losses",
                "tags": ["risk", "liquidity", "pools", "calculation"]
            },
            {
                "term": "TVL",
                "definition": "Total Value Locked - measure of assets deposited in DeFi protocols.",
                "example": "Ethereum's TVL reached $100B+ at peak, showing massive adoption.",
                "category": "DeFi",
                "difficulty": "Intermediate",
                "importance": "High",
                "real_world_value": "Evaluating protocol adoption and security",
                "earnings_potential": "High - Identifies promising protocols early",
                "tags": ["metrics", "adoption", "security", "analysis"]
            }
        ],
        
        "trading_mastery": [
            {
                "term": "HODL",
                "definition": "Hold On for Dear Life - long-term holding strategy regardless of volatility.",
                "example": "Bitcoin HODLers from 2017 ($20k peak) were rewarded in 2021 ($69k peak).",
                "category": "Trading",
                "difficulty": "Beginner",
                "importance": "Critical",
                "real_world_value": "Building wealth through patient long-term investing",
                "earnings_potential": "Very High - Historical outperformance vs trading",
                "tags": ["strategy", "long_term", "patience", "wealth_building"]
            },
            {
                "term": "Dollar Cost Averaging",
                "definition": "Buying fixed dollar amount regularly regardless of price to reduce volatility impact.",
                "example": "Buying $100 Bitcoin weekly for 4 years dramatically outperformed lump sum.",
                "category": "Trading",
                "difficulty": "Beginner",
                "importance": "Critical",
                "real_world_value": "Reducing emotional decision-making in investing",
                "earnings_potential": "High - Smooth returns with less stress",
                "tags": ["strategy", "systematic", "risk_reduction", "automation"]
            },
            {
                "term": "Support and Resistance",
                "definition": "Price levels where buying (support) or selling (resistance) pressure typically emerges.",
                "example": "Bitcoin's $20k level acted as resistance in 2017, then support in 2022.",
                "category": "Trading",
                "difficulty": "Intermediate",
                "importance": "High",
                "real_world_value": "Timing entries and exits more effectively",
                "earnings_potential": "High - Improves buy/sell timing",
                "tags": ["technical_analysis", "levels", "psychology", "timing"]
            },
            {
                "term": "Market Cap",
                "definition": "Total value of cryptocurrency calculated as circulating supply × current price.",
                "example": "Bitcoin's $1.3T market cap makes it larger than most countries' GDP.",
                "category": "Trading",
                "difficulty": "Beginner",
                "importance": "Critical",
                "real_world_value": "Evaluating relative size and investment potential",
                "earnings_potential": "High - Identifies undervalued opportunities",
                "tags": ["valuation", "size", "comparison", "fundamentals"]
            }
        ],
        
        "blockchain_fundamentals": [
            {
                "term": "Blockchain",
                "definition": "Immutable distributed ledger recording transactions across multiple computers.",
                "example": "Bitcoin's blockchain contains every transaction since 2009, totaling $15T+ moved.",
                "category": "Blockchain",
                "difficulty": "Beginner",
                "importance": "Critical",
                "real_world_value": "Foundation of all crypto understanding",
                "earnings_potential": "Critical - Enables all other crypto activities",
                "tags": ["fundamental", "technology", "ledger", "decentralization"]
            },
            {
                "term": "Smart Contract",
                "definition": "Self-executing code that automatically enforces agreements without intermediaries.",
                "example": "Ethereum smart contracts power $200B+ DeFi ecosystem automatically.",
                "category": "Blockchain",
                "difficulty": "Intermediate",
                "importance": "Critical",
                "real_world_value": "Enables programmable money and automated services",
                "earnings_potential": "Very High - Powers entire DeFi and NFT ecosystems",
                "tags": ["automation", "programming", "ethereum", "innovation"]
            },
            {
                "term": "Gas Fees",
                "definition": "Transaction costs paid to validators for processing blockchain operations.",
                "example": "Ethereum gas fees hit $500+ during NFT mania, making small trades uneconomical.",
                "category": "Blockchain",
                "difficulty": "Beginner",
                "importance": "High",
                "real_world_value": "Optimizing transaction costs and timing",
                "earnings_potential": "Medium - Saves money on transaction fees",
                "tags": ["fees", "optimization", "network", "costs"]
            }
        ],
        
        "security_essentials": [
            {
                "term": "Private Key",
                "definition": "Secret cryptographic key providing complete control over cryptocurrency funds.",
                "example": "Lost private keys have permanently locked $100B+ worth of Bitcoin forever.",
                "category": "Security",
                "difficulty": "Beginner",
                "importance": "Critical",
                "real_world_value": "Absolute control and security of digital assets",
                "earnings_potential": "Critical - Protects entire portfolio from loss",
                "tags": ["security", "control", "responsibility", "backup"]
            },
            {
                "term": "Hardware Wallet",
                "definition": "Physical device storing private keys offline for maximum security.",
                "example": "Ledger and Trezor protect billions in crypto from exchange hacks.",
                "category": "Security", 
                "difficulty": "Intermediate",
                "importance": "Critical",
                "real_world_value": "Protection from hacks, malware, and exchange failures",
                "earnings_potential": "Critical - Prevents total portfolio loss",
                "tags": ["hardware", "cold_storage", "protection", "best_practice"]
            },
            {
                "term": "Seed Phrase",
                "definition": "12-24 word backup phrase that can restore access to crypto wallet.",
                "example": "Seed phrases have recovered millions in crypto after device failures.",
                "category": "Security",
                "difficulty": "Beginner", 
                "importance": "Critical",
                "real_world_value": "Wallet recovery and backup security",
                "earnings_potential": "Critical - Prevents permanent loss of funds",
                "tags": ["backup", "recovery", "mnemonic", "restoration"]
            }
        ]
    }

# Advanced learning analytics system
class LearningAnalytics:
    def __init__(self):
        self.skill_weights = {
            "Memecoin Culture": 0.2,
            "DeFi": 0.25,
            "Trading": 0.25, 
            "Blockchain": 0.2,
            "Security": 0.1
        }
        
    def calculate_mastery_score(self, learned_terms: set, all_terms: dict) -> dict:
        total_terms = sum(len(category) for category in all_terms.values())
        learned_count = len(learned_terms)
        
        category_scores = {}
        for category, terms in all_terms.items():
            category_learned = sum(1 for term in terms if term["term"] in learned_terms)
            category_scores[category] = (category_learned / len(terms)) * 100
        
        overall_score = sum(
            score * self.skill_weights.get(category, 0.2) 
            for category, score in category_scores.items()
        )
        
        return {
            "overall_score": overall_score,
            "category_scores": category_scores,
            "total_learned": learned_count,
            "total_available": total_terms,
            "completion_percentage": (learned_count / total_terms) * 100
        }
    
    def get_personalized_recommendations(self, learned_terms: set, all_terms: dict) -> list:
        recommendations = []
        
        for category, terms in all_terms.items():
            unlearned_critical = [
                term for term in terms 
                if term["term"] not in learned_terms and term["importance"] == "Critical"
            ]
            
            if unlearned_critical:
                recommendations.append({
                    "type": "critical",
                    "category": category,
                    "term": unlearned_critical[0],
                    "reason": f"Critical {category.lower()} knowledge gap"
                })
        
        return recommendations[:3]  # Top 3 recommendations

# Market data integration with educational context
@st.cache_data(ttl=300)
def fetch_educational_market_data():
    """Fetch market data with educational insights"""
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 10,
            'page': 1,
            'sparkline': False,
            'price_change_percentage': '24h,7d'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Add educational context
        educational_context = {
            'bitcoin': {
                'lesson': 'Digital Gold',
                'key_concept': 'Store of Value',
                'learning_focus': 'Understand why Bitcoin is considered digital gold'
            },
            'ethereum': {
                'lesson': 'Smart Contract Platform',
                'key_concept': 'Programmable Money',
                'learning_focus': 'Learn how Ethereum enables DeFi and NFTs'
            },
            'dogecoin': {
                'lesson': 'Memecoin Culture',
                'key_concept': 'Community Power',
                'learning_focus': 'See how memes and community drive value'
            }
        }
        
        for coin in data:
            coin_id = coin['id']
            if coin_id in educational_context:
                coin.update(educational_context[coin_id])
        
        return data
        
    except Exception as e:
        return None

# Advanced session state management
def init_advanced_session_state():
    """Initialize comprehensive session state"""
    defaults = {
        'user_profile': {
            'experience_level': 'Beginner',
            'learning_goals': [],
            'preferred_categories': [],
            'daily_streak': 0,
            'total_study_time': 0,
            'last_visit': None
        },
        'learning_progress': {
            'terms_learned': set(),
            'quiz_history': [],
            'skill_assessments': {},
            'achievements_unlocked': [],
            'learning_path_progress': {}
        },
        'quiz_system': {
            'current_question': None,
            'score': 0,
            'total_attempts': 0,
            'streak': 0,
            'difficulty_level': 'adaptive',
            'answered': False
        },
        'engagement_metrics': {
            'session_start': datetime.now(),
            'pages_visited': [],
            'features_used': [],
            'time_per_section': {}
        }
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Initialize everything
crypto_db = load_comprehensive_crypto_database()
analytics = LearningAnalytics()
init_advanced_session_state()

# Create flattened terms list for easier processing
all_terms = []
for category_terms in crypto_db.values():
    all_terms.extend(category_terms)

# Calculate learning analytics
learned_terms = st.session_state.learning_progress['terms_learned']
mastery_stats = analytics.calculate_mastery_score(learned_terms, crypto_db)
recommendations = analytics.get_personalized_recommendations(learned_terms, crypto_db)

# HEADER - Value-driven hero section
st.markdown("""
<div class="main-header">
    <h1>🚀 CryptoLearn Pro</h1>
    <h2>Master Crypto & Web3 • Earn Real Returns • Build Wealth</h2>
    <p style="font-size: 1.2rem; margin: 1rem 0;">
        The only crypto education platform that directly connects learning to earning potential
    </p>
    <div style="margin-top: 2rem;">
        <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 25px; margin: 0.5rem;">
            💰 $50B+ Market Cap Knowledge
        </span>
        <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 25px; margin: 0.5rem;">
            🎯 Personalized Learning Paths
        </span>
        <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 25px; margin: 0.5rem;">
            📊 Real-Time Market Integration
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar - Enhanced navigation with progress
st.sidebar.markdown("### 🎯 Your Learning Dashboard")

# User level and progress
overall_score = mastery_stats['overall_score']
if overall_score >= 80:
    level = "Crypto Expert 🥇"
    level_color = "#FFD700"
elif overall_score >= 60:
    level = "Advanced Trader 🥈"
    level_color = "#C0C0C0"
elif overall_score >= 40:
    level = "Intermediate 🥉"
    level_color = "#CD7F32"
elif overall_score >= 20:
    level = "Learning 📚"
    level_color = "#667eea"
else:
    level = "Beginner 🌱"
    level_color = "#28a745"

st.sidebar.markdown(f"""
<div style="background: {level_color}; color: white; padding: 1rem; border-radius: 10px; text-align: center; margin-bottom: 1rem;">
    <h3>{level}</h3>
    <p>Mastery Score: {overall_score:.1f}%</p>
</div>
""", unsafe_allow_html=True)

# Progress breakdown
st.sidebar.markdown("#### 📊 Skill Breakdown")
for category, score in mastery_stats['category_scores'].items():
    st.sidebar.progress(score / 100)
    st.sidebar.caption(f"{category}: {score:.1f}%")

# Navigation
page = st.sidebar.selectbox(
    "🧭 Navigate Your Journey:",
    [
        "🏠 Learning Dashboard",
        "🎯 Personalized Learning", 
        "📊 Market + Education",
        "🧠 Adaptive Quiz System",
        "💡 Discovery & Insights",
        "🏆 Achievements & Progress",
        "💰 Earning Opportunities"
    ]
)

# Track page visits
if page not in st.session_state.engagement_metrics['pages_visited']:
    st.session_state.engagement_metrics['pages_visited'].append(page)

# MAIN CONTENT SECTIONS
if page == "🏠 Learning Dashboard":
    # Value proposition section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="value-prop-card">
            <h3>💰 Learn & Earn</h3>
            <h2>$2,847</h2>
            <p>Average additional income potential from DeFi knowledge</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="value-prop-card">
            <h3>🎯 Personalized</h3>
            <h2>AI-Driven</h2>
            <p>Adaptive learning paths based on your goals and progress</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="value-prop-card">
            <h3>📊 Real-Time</h3>
            <h2>Live Data</h2>
            <p>Market data integrated with learning for practical application</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick stats
    st.subheader("📈 Your Learning Impact")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Terms Mastered", 
            f"{len(learned_terms)}/{len(all_terms)}", 
            f"+{len(learned_terms) - st.session_state.get('last_learned_count', 0)}"
        )
    
    with col2:
        quiz_accuracy = 0
        if st.session_state.quiz_system['total_attempts'] > 0:
            quiz_accuracy = (st.session_state.quiz_system['score'] / st.session_state.quiz_system['total_attempts']) * 100
        
        st.metric(
            "Quiz Accuracy",
            f"{quiz_accuracy:.1f}%",
            f"🔥 {st.session_state.quiz_system['streak']} streak"
        )
    
    with col3:
        earning_potential = len(learned_terms) * 150  # Estimated earning potential per term
        st.metric(
            "Earning Potential",
            f"${earning_potential:,}",
            "Based on mastered skills"
        )
    
    with col4:
        st.metric(
            "Learning Level",
            level.split()[0],
            f"{overall_score:.1f}% mastery"
        )
    
    # Personalized recommendations
    st.subheader("🎯 AI-Powered Recommendations for You")
    
    if recommendations:
        for i, rec in enumerate(recommendations):
            term = rec['term']
            
            with st.expander(f"🚨 Priority: Learn '{term['term']}' - {rec['reason']}", expanded=i==0):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"""
                    **📖 Definition:** {term['definition']}
                    
                    **💡 Real-World Value:** {term['real_world_value']}
                    
                    **💰 Earning Potential:** {term['earnings_potential']}
                    
                    **🎯 Example:** {term['example']}
                    """)
                
                with col2:
                    if st.button(f"✅ Master This Term", key=f"rec_{i}"):
                        st.session_state.learning_progress['terms_learned'].add(term['term'])
                        st.balloons()
                        st.success(f"🎉 Mastered '{term['term']}'! Earning potential increased!")
                        st.rerun()
                    
                    if st.button(f"🎯 Quiz Me", key=f"quiz_rec_{i}"):
                        st.session_state.quiz_system['current_question'] = term
                        st.session_state.quiz_system['answered'] = False
                        st.info("Quiz ready! Go to Adaptive Quiz System.")
    else:
        st.success("🎉 Amazing! You've mastered all critical terms. You're ready for advanced strategies!")
    
    # Recent market movements with learning opportunities
    st.subheader("📊 Market Movements + Learning Opportunities")
    
    market_data = fetch_educational_market_data()
    
    if market_data:
        for coin in market_data[:3]:
            price_change_24h = coin.get('price_change_percentage_24h', 0)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                st.markdown(f"""
                <div class="market-card">
                    <h3>{coin['name']}</h3>
                    <h2>${coin['current_price']:,.2f}</h2>
                    <p style="color: {'green' if price_change_24h > 0 else 'red'}">
                        {price_change_24h:+.2f}% (24h)
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if hasattr(coin, 'lesson'):
                    st.info(f"💡 **Learning Opportunity:** {coin['lesson']} - {coin['learning_focus']}")
                
                # Suggest relevant terms to learn
                if price_change_24h > 10:
                    st.success("🚀 Big pump! Perfect time to learn: 'To the Moon', 'FOMO', 'Diamond Hands'")
                elif price_change_24h < -10:
                    st.warning("📉 Correction happening. Learn about: 'FUD', 'HODL', 'Dollar Cost Averaging'")
            
            with col3:
                if st.button(f"Learn about {coin['name']}", key=f"learn_{coin['id']}"):
                    # Find related terms
                    if coin['id'] == 'bitcoin':
                        suggested_terms = ['HODL', 'Digital Gold', 'Store of Value']
                    elif coin['id'] == 'ethereum':
                        suggested_terms = ['Smart Contract', 'DeFi', 'Gas Fees']
                    else:
                        suggested_terms = ['Market Cap', 'Trading', 'Volatility']
                    
                    st.info(f"💡 Study these terms: {', '.join(suggested_terms)}")

elif page == "🎯 Personalized Learning":
    st.header("🎯 Your Personalized Learning Journey")
    
    # Learning path assessment
    if not st.session_state.user_profile.get('learning_goals'):
        st.subheader("🎨 Customize Your Learning Experience")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 What's Your Primary Goal?")
            goal = st.selectbox(
                "Choose your main objective:",
                [
                    "💰 Generate Passive Income through DeFi",
                    "📈 Become a Profitable Trader", 
                    "🏗️ Understand Blockchain Technology",
                    "🐕 Master Memecoin Culture",
                    "🛡️ Secure My Crypto Assets",
                    "🚀 Build a Web3 Career"
                ]
            )
        
        with col2:
            st.markdown("#### ⭐ Current Experience Level?")
            experience = st.selectbox(
                "Be honest about your current level:",
                [
                    "🌱 Complete Beginner",
                    "📚 Some Basic Knowledge", 
                    "📊 Intermediate Understanding",
                    "🎯 Advanced but Want to Fill Gaps",
                    "🥇 Expert Looking for Latest Trends"
                ]
            )
        
        if st.button("🚀 Create My Learning Path", type="primary"):
            st.session_state.user_profile['learning_goals'] = [goal]
            st.session_state.user_profile['experience_level'] = experience
            st.success("🎉 Learning path created! Refresh to see your personalized curriculum.")
            st.rerun()
    
    else:
        # Show personalized curriculum
        user_goal = st.session_state.user_profile['learning_goals'][0]
        user_level = st.session_state.user_profile['experience_level']
        
        st.markdown(f"""
        <div class="learning-path-card">
            <h2>🎯 Your Learning Path: {user_goal}</h2>
            <p><strong>Experience Level:</strong> {user_level}</p>
            <p><strong>Progress:</strong> {overall_score:.1f}% Complete</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate curriculum based on goals
        if "DeFi" in user_goal:
            curriculum = ["DeFi", "Trading", "Security", "Blockchain"]
            focus_message = "Master DeFi to unlock passive income opportunities worth $1000s annually"
        elif "Trading" in user_goal:
            curriculum = ["Trading", "Memecoin Culture", "Blockchain", "DeFi"]
            focus_message = "Develop trading skills that could generate 20%+ annual returns"
        elif "Blockchain" in user_goal:
            curriculum = ["Blockchain", "Security", "DeFi", "Trading"]
            focus_message = "Build fundamental knowledge for Web3 career opportunities"
        elif "Memecoin" in user_goal:
            curriculum = ["Memecoin Culture", "Trading", "Security", "DeFi"]
            focus_message = "Understand memecoin dynamics to spot 100x opportunities early"
        elif "Secure" in user_goal:
            curriculum = ["Security", "Blockchain", "DeFi", "Trading"]
            focus_message = "Protect your crypto assets from the $3B+ lost annually to hacks"
        else:
            curriculum = ["Blockchain", "DeFi", "Trading", "Security"]
            focus_message = "Build comprehensive Web3 knowledge for career advancement"
        
        st.info(f"💡 **Focus:** {focus_message}")
        
        # Show curriculum with progress
        for i, category in enumerate(curriculum):
            category_score = mastery_stats['category_scores'].get(category, 0)
            category_terms = crypto_db.get(category.lower().replace(' ', '_'), [])
            
            if not category_terms:
                # Map display names to database keys
                category_map = {
                    "DeFi": "defi_revolution",
                    "Trading": "trading_mastery", 
                    "Security": "security_essentials",
                    "Blockchain": "blockchain_fundamentals",
                    "Memecoin Culture": "memecoin_culture"
                }
                category_terms = crypto_db.get(category_map.get(category, ""), [])
            
            with st.expander(f"📚 Module {i+1}: {category} ({category_score:.1f}% Complete)", expanded=i==0):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.progress(category_score / 100)
                    
                    # Show next term to learn
                    unlearned = [t for t in category_terms if t['term'] not in learned_terms]
                    if unlearned:
                        next_term = unlearned[0]
                        st.markdown(f"""
                        **🎯 Next to Master:** {next_term['term']}
                        
                        **Definition:** {next_term['definition']}
                        
                        **💰 Earning Potential:** {next_term['earnings_potential']}
                        """)
                        
                        if st.button(f"✅ Master '{next_term['term']}'", key=f"master_{category}_{i}"):
                            st.session_state.learning_progress['terms_learned'].add(next_term['term'])
                            st.success(f"🎉 Mastered! Your {category} knowledge increased!")
                            st.rerun()
                    else:
                        st.success(f"🎉 {category} module completed! Moving to next level...")
                
                with col2:
                    completed = len([t for t in category_terms if t['term'] in learned_terms])
                    st.metric("Progress", f"{completed}/{len(category_terms)}")
                    
                    if category_score > 0:
                        estimated_earning = int(category_score * 50)  # $50 per percentage point
                        st.metric("Est. Value", f"${estimated_earning}")

elif page == "📊 Market + Education":
    st.header("📊 Live Market Data with Educational Context")
    
    # Market overview with learning integration
    market_data = fetch_educational_market_data()
    
    if market_data:
        st.subheader("💰 Top Cryptocurrencies + Learning Opportunities")
        
        # Market sentiment analysis
        total_positive = sum(1 for coin in market_data if coin.get('price_change_percentage_24h', 0) > 0)
        market_sentiment = "Bullish 🐂" if total_positive >= len(market_data) / 2 else "Bearish 🐻"
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Market Sentiment", market_sentiment)
        with col2:
            avg_change = sum(coin.get('price_change_percentage_24h', 0) for coin in market_data) / len(market_data)
            st.metric("Avg 24h Change", f"{avg_change:+.2f}%")
        with col3:
            total_mcap = sum(coin.get('market_cap', 0) for coin in market_data) / 1e12
            st.metric("Total Market Cap", f"${total_mcap:.2f}T")
        
        # Individual coin analysis with educational context
        for coin in market_data[:5]:
            price_change = coin.get('price_change_percentage_24h', 0)
            
            with st.expander(f"📈 {coin['name']} (${coin['current_price']:,.2f}) - {price_change:+.2f}%"):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.markdown(f"""
                    **Current Price:** ${coin['current_price']:,.2f}
                    **Market Cap:** ${coin['market_cap']:,}
                    **24h Volume:** ${coin['total_volume']:,}
                    **7d Change:** {coin.get('price_change_percentage_7d_in_currency', 0):+.2f}%
                    """)
                
                with col2:
                    # Educational context based on coin performance
                    if price_change > 15:
                        st.success("🚀 **Strong Pump!** Learn about: FOMO, To the Moon, Market Manipulation")
                        educational_focus = "Study bubble psychology and risk management"
                    elif price_change > 5:
                        st.info("📈 **Steady Growth** Learn about: Technical Analysis, Support Levels")
                        educational_focus = "Good time to study trend analysis"
                    elif price_change < -15:
                        st.error("📉 **Major Correction** Learn about: FUD, Diamond Hands, Dollar Cost Averaging")
                        educational_focus = "Perfect time to understand bear market psychology"
                    elif price_change < -5:
                        st.warning("📊 **Minor Dip** Learn about: Buying the Dip, Volatility")
                        educational_focus = "Study accumulation strategies"
                    else:
                        st.info("😴 **Sideways Action** Learn about: Consolidation, Range Trading")
                        educational_focus = "Good time for fundamental analysis study"
                    
                    st.caption(f"💡 {educational_focus}")
                
                with col3:
                    if hasattr(coin, 'lesson'):
                        if st.button(f"Learn {coin['lesson']}", key=f"learn_market_{coin['id']}"):
                            # Find relevant terms
                            relevant_terms = []
                            for category_terms in crypto_db.values():
                                for term in category_terms:
                                    if any(keyword in term['tags'] for keyword in coin['key_concept'].lower().split()):
                                        relevant_terms.append(term['term'])
                            
                            if relevant_terms:
                                st.info(f"💡 Study: {', '.join(relevant_terms[:3])}")
        
        # Market-based learning suggestions
        st.subheader("🎯 Today's Market-Based Learning Plan")
        
        if market_sentiment == "Bullish 🐂":
            st.success("""
            **🐂 Bull Market Learning Focus:**
            - Study 'FOMO' and 'Bubble Psychology' to avoid overinvestment
            - Learn 'Profit Taking' strategies 
            - Understand 'Market Cycles' for better timing
            """)
            suggested_terms = ['FOMO', 'To the Moon', 'Market Cap']
        else:
            st.info("""
            **🐻 Bear Market Learning Focus:**
            - Master 'Dollar Cost Averaging' for accumulation
            - Study 'Diamond Hands' psychology
            - Learn about 'Fundamental Analysis' for long-term value
            """)
            suggested_terms = ['Diamond Hands', 'Dollar Cost Averaging', 'HODL']
        
        # Quick learning buttons
        col1, col2, col3 = st.columns(3)
        for i, term_name in enumerate(suggested_terms):
            # Find the term in our database
            found_term = None
            for category_terms in crypto_db.values():
                for term in category_terms:
                    if term['term'] == term_name:
                        found_term = term
                        break
                if found_term:
                    break
            
            with [col1, col2, col3][i]:
                if found_term and st.button(f"📚 Learn '{term_name}'", key=f"market_learn_{i}"):
                    if found_term['term'] not in learned_terms:
                        st.session_state.learning_progress['terms_learned'].add(found_term['term'])
                        st.success(f"🎉 Mastered '{term_name}'!")
                        st.rerun()
                    else:
                        st.info(f"✅ You already know '{term_name}'!")

elif page == "🧠 Adaptive Quiz System":
    st.header("🧠 AI-Powered Adaptive Quiz System")
    
    # Quiz performance dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Quiz Score", 
            f"{st.session_state.quiz_system['score']}/{st.session_state.quiz_system['total_attempts']}"
        )
    
    with col2:
        accuracy = 0
        if st.session_state.quiz_system['total_attempts'] > 0:
            accuracy = (st.session_state.quiz_system['score'] / st.session_state.quiz_system['total_attempts']) * 100
        st.metric("Accuracy", f"{accuracy:.1f}%")
    
    with col3:
        st.metric("Current Streak", st.session_state.quiz_system['streak'])
    
    with col4:
        est_knowledge_value = len(learned_terms) * 200  # $200 per mastered term
        st.metric("Knowledge Value", f"${est_knowledge_value:,}")
    
    # Adaptive quiz modes
    st.subheader("🎯 Choose Your Challenge")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🧠 AI Adaptive Quiz", type="primary", use_container_width=True):
            # AI selects optimal question based on user progress
            if len(learned_terms) < 5:
                # Focus on fundamentals for beginners
                fundamental_terms = []
                for term in all_terms:
                    if term['difficulty'] == 'Beginner' and term['importance'] == 'Critical':
                        fundamental_terms.append(term)
                
                if fundamental_terms:
                    question = random.choice(fundamental_terms)
                    quiz_type = "🎯 Fundamental Learning"
                else:
                    question = random.choice(all_terms)
                    quiz_type = "📚 General Knowledge"
            else:
                # Advanced adaptive selection
                unlearned = [t for t in all_terms if t['term'] not in learned_terms]
                
                if unlearned:
                    # Prioritize high-value terms
                    high_value = [t for t in unlearned if 'High' in t['earnings_potential'] or 'Critical' in t['earnings_potential']]
                    question = random.choice(high_value if high_value else unlearned)
                    quiz_type = "💰 High-Value Learning"
                else:
                    # Review mode for completed users
                    question = random.choice(all_terms)
                    quiz_type = "🔄 Mastery Review"
            
            st.session_state.quiz_system['current_question'] = question
            st.session_state.quiz_system['answered'] = False
            st.session_state.quiz_type = quiz_type
            st.rerun()
    
    with col2:
        if st.button("💰 High-Earning Focus", use_container_width=True):
            # Focus on terms with highest earning potential
            high_earning_terms = [
                t for t in all_terms 
                if 'Very High' in t['earnings_potential'] or 'Critical' in t['earnings_potential']
            ]
            
            if high_earning_terms:
                unlearned_high_value = [t for t in high_earning_terms if t['term'] not in learned_terms]
                question = random.choice(unlearned_high_value if unlearned_high_value else high_earning_terms)
                
                st.session_state.quiz_system['current_question'] = question
                st.session_state.quiz_system['answered'] = False
                st.session_state.quiz_type = "💰 Earning-Focused Quiz"
                st.rerun()
    
    with col3:
        if st.button("🐕 Memecoin Mastery", use_container_width=True):
            # Focus on memecoin culture
            memecoin_terms = crypto_db.get('memecoin_culture', [])
            
            if memecoin_terms:
                question = random.choice(memecoin_terms)
                st.session_state.quiz_system['current_question'] = question
                st.session_state.quiz_system['answered'] = False
                st.session_state.quiz_type = "🐕 Memecoin Culture Quiz"
                st.rerun()
    
    # Display current question
    if st.session_state.quiz_system.get('current_question'):
        question = st.session_state.quiz_system['current_question']
        quiz_type = getattr(st.session_state, 'quiz_type', 'Standard Quiz')
        
        st.markdown(f"""
        <div class="quiz-card">
            <h3>{quiz_type}</h3>
            <h2>❓ What does '{question['term']}' mean?</h2>
            <p><strong>💰 Earning Potential:</strong> {question['earnings_potential']}</p>
            <p><strong>🎯 Real-World Value:</strong> {question['real_world_value']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate multiple choice options
        correct_answer = question['definition']
        
        # Get wrong answers from same category for better difficulty
        same_category_terms = []
        for category_terms in crypto_db.values():
            for term in category_terms:
                if term['category'] == question['category'] and term['term'] != question['term']:
                    same_category_terms.append(term)
        
        if len(same_category_terms) >= 3:
            wrong_answers = [t['definition'] for t in random.sample(same_category_terms, 3)]
        else:
            # Fallback to random terms
            other_terms = [t for t in all_terms if t['term'] != question['term']]
            wrong_answers = [t['definition'] for t in random.sample(other_terms, min(3, len(other_terms)))]
        
        options = [correct_answer] + wrong_answers
        random.shuffle(options)
        
        # Quiz interface
        user_answer = st.radio(
            "Select the correct definition:",
            options,
            key="adaptive_quiz_answer",
            disabled=st.session_state.quiz_system['answered']
        )
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ Submit Answer", disabled=st.session_state.quiz_system['answered']):
                st.session_state.quiz_system['answered'] = True
                st.session_state.quiz_system['total_attempts'] += 1
                
                if user_answer == correct_answer:
                    st.session_state.quiz_system['score'] += 1
                    st.session_state.quiz_system['streak'] += 1
                    st.session_state.learning_progress['terms_learned'].add(question['term'])
                    
                    st.success("🎉 Correct! Knowledge and earning potential increased!")
                    
                    # Bonus for high-value terms
                    if 'Critical' in question['earnings_potential'] or 'Very High' in question['earnings_potential']:
                        st.balloons()
                        st.success("💰 HIGH-VALUE TERM MASTERED! This knowledge can directly increase your income!")
                    
                    # Streak bonuses
                    streak = st.session_state.quiz_system['streak']
                    if streak == 5:
                        st.success("🔥 5-question streak! You're on fire!")
                    elif streak == 10:
                        st.success("🚀 10-question streak! Expert level achieved!")
                        st.balloons()
                
                else:
                    st.session_state.quiz_system['streak'] = 0
                    st.error("❌ Not quite right. Keep learning!")
                
                # Show educational context
                st.info(f"💡 **Correct Answer:** {correct_answer}")
                st.info(f"🎯 **Example:** {question['example']}")
                
                # Show earning potential context
                if 'High' in question['earnings_potential']:
                    st.success(f"💰 **Value:** Understanding '{question['term']}' can help you: {question['real_world_value']}")
        
        with col2:
            if st.button("⏭️ Next Question"):
                # Generate next question with same quiz type
                if 'Earning-Focused' in quiz_type:
                    high_earning = [t for t in all_terms if 'Very High' in t['earnings_potential']]
                    next_question = random.choice(high_earning)
                elif 'Memecoin' in quiz_type:
                    next_question = random.choice(crypto_db['memecoin_culture'])
                else:
                    # Adaptive selection
                    unlearned = [t for t in all_terms if t['term'] not in learned_terms]
                    next_question = random.choice(unlearned if unlearned else all_terms)
                
                st.session_state.quiz_system['current_question'] = next_question
                st.session_state.quiz_system['answered'] = False
                st.rerun()
        
        with col3:
            if st.button("💡 Get Hint"):
                # Provide contextual hints
                hint_keywords = question['tags'][:2]
                st.info(f"💡 **Hint:** This term relates to: {', '.join(hint_keywords)}")
                
                if question['category'] == 'Memecoin Culture':
                    st.caption("🐕 Think about community behavior and psychology")
                elif question['category'] == 'DeFi':
                    st.caption("🏦 Consider decentralized financial services")
                elif question['category'] == 'Trading':
                    st.caption("📈 Think about market strategies and analysis")
    
    else:
        st.info("👆 Choose a quiz mode above to start learning and earning!")
        
        # Show quiz statistics
        if st.session_state.quiz_system['total_attempts'] > 0:
            st.subheader("📊 Your Quiz Performance")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Performance chart
                accuracy_pct = (st.session_state.quiz_system['score'] / st.session_state.quiz_system['total_attempts']) * 100
                
                fig = go.Figure(data=go.Bar(
                    x=['Correct', 'Incorrect'],
                    y=[st.session_state.quiz_system['score'], 
                       st.session_state.quiz_system['total_attempts'] - st.session_state.quiz_system['score']],
                    marker_color=['#28a745', '#dc3545']
                ))
                fig.update_layout(title="Quiz Performance", height=300)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown(f"""
                ### 🎯 Performance Insights
                
                **Accuracy Rate:** {accuracy_pct:.1f}%
                **Best Streak:** {max(st.session_state.quiz_system.get('best_streak', 0), st.session_state.quiz_system['streak'])}
                **Knowledge Value:** ${len(learned_terms) * 200:,}
                
                ### 🚀 Next Level Goals
                - **Target Accuracy:** 85%+
                - **Streak Goal:** 15 questions
                - **Terms to Master:** {max(0, 50 - len(learned_terms))} remaining
                """)

elif page == "💡 Discovery & Insights":
    st.header("💡 Discovery & Deep Insights")
    
    # Advanced discovery modes
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🧠 AI Discovery", type="primary", use_container_width=True):
            # AI-powered term discovery based on user profile
            unlearned = [t for t in all_terms if t['term'] not in learned_terms]
            
            if unlearned:
                # Score terms by relevance to user goals
                user_goal = st.session_state.user_profile.get('learning_goals', [''])[0]
                
                scored_terms = []
                for term in unlearned:
                    score = 0
                    
                    # Goal alignment scoring
                    if 'DeFi' in user_goal and term['category'] == 'DeFi':
                        score += 3
                    elif 'Trading' in user_goal and term['category'] == 'Trading':
                        score += 3
                    elif 'Memecoin' in user_goal and term['category'] == 'Memecoin Culture':
                        score += 3
                    
                    # Importance scoring
                    if term['importance'] == 'Critical':
                        score += 2
                    elif term['importance'] == 'High':
                        score += 1
                    
                    # Earning potential scoring
                    if 'Very High' in term['earnings_potential']:
                        score += 2
                    elif 'High' in term['earnings_potential']:
                        score += 1
                    
                    scored_terms.append((term, score))
                
                # Select highest scoring term
                if scored_terms:
                    best_term = max(scored_terms, key=lambda x: x[1])[0]
                    st.session_state.discovery_term = best_term
                    st.session_state.discovery_type = "🧠 AI Recommendation"
            else:
                st.success("🎉 You've discovered all available terms!")
    
    with col2:
        if st.button("💎 Hidden Gems", use_container_width=True):
            # Find lesser-known but valuable terms
            unlearned = [t for t in all_terms if t['term'] not in learned_terms]
            hidden_gems = [
                t for t in unlearned 
                if t['difficulty'] in ['Intermediate', 'Advanced'] and 'High' in t['earnings_potential']
            ]
            
            if hidden_gems:
                gem = random.choice(hidden_gems)
                st.session_state.discovery_term = gem
