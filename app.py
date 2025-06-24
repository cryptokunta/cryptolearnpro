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
            quiz_accuracy = (st.session_state.quiz_system['score'] / st.session_state.quiz_system['total_attempts']) *
