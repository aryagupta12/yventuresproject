import streamlit as st
import openai
import random

# Set your OpenAI API key securely
# Get API key from environment variable or Streamlit secrets
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    import os
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        st.error("Please set your OpenAI API key in Streamlit secrets or as an environment variable 'OPENAI_API_KEY'")
        st.stop()

# Page configuration
st.set_page_config(
    page_title="Investment Memo Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark mode and sophisticated styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@300;400;700&display=swap');
    
    /* Global dark theme */
    .main {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Welcome page styling */
    .welcome-container {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #0e1117 0%, #1a1d2a 100%);
    }
    
    .welcome-title {
        font-size: 3.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1rem;
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.02em;
    }
    
    .welcome-subtitle {
        font-size: 1.25rem;
        color: #a0a0a0;
        margin-bottom: 2rem;
        font-weight: 400;
        max-width: 600px;
        line-height: 1.6;
    }
    
    .welcome-features {
        display: flex;
        gap: 2rem;
        margin: 2rem 0;
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        min-width: 200px;
    }
    
    .feature-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        font-size: 0.9rem;
        color: #a0a0a0;
        line-height: 1.5;
    }
    
    /* Main form styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        text-align: center;
        margin-bottom: 1rem;
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.02em;
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #ffffff;
        border-bottom: 2px solid #3b82f6;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-family: 'Inter', sans-serif;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        margin-bottom: 1rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        border: none;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #000000;
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
    }
    
    .stTextArea > div > div > textarea {
        background-color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #000000;
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
    }
    
    .stSelectbox > div > div > select {
        background-color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #000000;
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1a1d2a;
    }
    
    /* Smooth transitions */
    .fade-in {
        animation: fadeIn 0.8s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Memo display styling */
    .memo-container {
        background: #ffffff;
        color: #000000;
        padding: 2rem;
        border-radius: 12px;
        margin: 1rem 0;
        font-family: 'Merriweather', serif;
        line-height: 1.6;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    .memo-container h1, .memo-container h2, .memo-container h3 {
        font-family: 'Inter', sans-serif;
        color: #1a1a1a;
        margin-top: 2rem;
        margin-bottom: 1rem;
        page-break-after: avoid;
    }
    
    .memo-container h1 {
        font-size: 2rem;
        font-weight: 700;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 0.5rem;
    }
    
    .memo-container h2 {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2563eb;
        page-break-before: always;
    }
    
    .memo-container h3 {
        font-size: 1.25rem;
        font-weight: 600;
        color: #374151;
    }
    
    .memo-container p {
        margin-bottom: 1rem;
        color: #1f2937;
    }
    
    .memo-container ul, .memo-container ol {
        margin-bottom: 1rem;
        padding-left: 1.5rem;
    }
    
    .memo-container li {
        margin-bottom: 0.5rem;
        color: #1f2937;
    }
    
    .memo-container strong {
        color: #1a1a1a;
        font-weight: 600;
    }
    
    .memo-container em {
        color: #6b7280;
        font-style: italic;
    }
    
    /* Page break styling */
    .page-break {
        page-break-before: always;
        margin-top: 2rem;
    }
    
    @media print {
        .memo-container h2 {
            page-break-before: always;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'show_welcome' not in st.session_state:
    st.session_state.show_welcome = True

# Function to intelligently categorize and populate company data
def categorize_company_data(company_name, company_description, market_category):
    categorization_prompt = f"""
    Based on this company information, intelligently categorize and populate all investment memo fields:
    
    Company Name: {company_name}
    Company Description: {company_description}
    Market Category: {market_category}
    
    Generate a complete company profile in JSON format with realistic data:
    - website: A realistic website URL
    - launch_year: A year between 2020-2024
    - team_size: A number between 2-50
    - stage: One of: Pre-seed, Seed, Series A, Series B, Series C (based on description)
    - one_liner: A compelling one-sentence description
    - market_size: Realistic market size for this category (e.g., "$10B TAM")
    - current_cash: Current cash position (e.g., "$500k in cash")
    - burn_rate: Monthly burn rate (e.g., "$50k/month")
    - revenue: Current revenue (e.g., "$200k ARR")
    - prev_raised: Previously raised amount (e.g., "$2M Seed")
    - round_size: Current round size (e.g., "$5M Series A")
    - post_money_valuation: Post-money valuation (e.g., "$25M")
    - use_of_capital: What they need money for (2-3 sentences)
    - named_competitors: 3-4 realistic competitor names for this market
    - founder_1_name: First founder name
    - founder_1_bio: First founder bio (2-3 sentences)
    - founder_2_name: Second founder name
    - founder_2_bio: Second founder bio (2-3 sentences)
    - founder_3_name: Third founder name (optional)
    - founder_3_bio: Third founder bio (optional)
    - founder_4_name: Fourth founder name (optional)
    - founder_4_bio: Fourth founder bio (optional)
    - misc_notes: Additional context about the company
    - pros: 3-4 key advantages
    - cons: 3-4 key risks
    - best_case: Best case scenario (2-3 sentences)
    - worst_case: Worst case scenario (2-3 sentences)
    
    Make it realistic and varied. Base the stage, financials, and team size on the description and market category.
    Return only valid JSON.
    """
    
    try:
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": categorization_prompt}],
            temperature=0.7,
            max_tokens=1500
        )
        
        import json
        data_text = response.choices[0].message.content
        
        try:
            start_idx = data_text.find('{')
            end_idx = data_text.rfind('}') + 1
            json_str = data_text[start_idx:end_idx]
            return json.loads(json_str)
        except:
            # Fallback data
            return {
                "website": f"https://{company_name.lower().replace(' ', '')}.com",
                "launch_year": "2023",
                "team_size": "8",
                "stage": "Series A",
                "one_liner": f"{company_name} is revolutionizing the {market_category} space.",
                "market_size": "$10B TAM",
                "current_cash": "$500k in cash",
                "burn_rate": "$50k/month",
                "revenue": "$200k ARR",
                "prev_raised": "$2M Seed",
                "round_size": "$5M Series A",
                "post_money_valuation": "$25M",
                "use_of_capital": "Expanding team, scaling operations, and developing new features.",
                "named_competitors": "Competitor A, Competitor B, Competitor C",
                "founder_1_name": "Founder One",
                "founder_1_bio": "Experienced entrepreneur with background in the industry.",
                "founder_2_name": "Founder Two",
                "founder_2_bio": "Technical expert with deep domain knowledge.",
                "founder_3_name": "",
                "founder_3_bio": "",
                "founder_4_name": "",
                "founder_4_bio": "",
                "misc_notes": "Promising early traction in the market.",
                "pros": "Strong team, good market timing, innovative approach",
                "cons": "Competitive market, early stage risks, execution challenges",
                "best_case": "Becomes market leader and achieves significant growth.",
                "worst_case": "Fails to gain traction and runs out of funding."
            }
    except Exception as e:
        st.error(f"Error categorizing company data: {e}")
        return None

# Function to generate random company data
def generate_test_company_data():
    test_prompt = """
    Generate a realistic startup company profile with the following information in JSON format:
    - company_name: A realistic startup name
    - company_overview: A detailed description of the company idea, target market, business model, and how the product/service works (3-4 sentences)
    - team_background: A description of the founding team, their backgrounds, experience, and qualifications (3-4 sentences)
    - website: A realistic website URL
    - launch_year: A year between 2020-2024
    - team_size: A number between 2-50
    - stage: One of: Pre-seed, Seed, Series A, Series B, Series C
    - market_size: A realistic market size (e.g., "$10B TAM")
    - current_cash: Current cash position (e.g., "$500k in cash")
    - burn_rate: Monthly burn rate (e.g., "$50k/month")
    - revenue: Current revenue (e.g., "$200k ARR")
    - prev_raised: Previously raised amount (e.g., "$2M Seed")
    - round_size: Current round size (e.g., "$5M Series A")
    - post_money_valuation: Post-money valuation (e.g., "$25M")
    - use_of_capital: What they need money for (2-3 sentences)
    
    Make it realistic and varied - could be any type of startup (SaaS, marketplace, hardware, etc.)
    """
    
    try:
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": test_prompt}],
            temperature=0.8,
            max_tokens=800
        )
        
        import json
        data_text = response.choices[0].message.content
        
        try:
            start_idx = data_text.find('{')
            end_idx = data_text.rfind('}') + 1
            json_str = data_text[start_idx:end_idx]
            return json.loads(json_str)
        except:
            return {
                "company_name": "TechFlow Solutions",
                "company_overview": "TechFlow Solutions is an AI-powered workflow automation platform that helps enterprise teams streamline their business processes. The company targets mid to large enterprises struggling with manual, time-consuming workflows across departments like HR, finance, and operations. Their SaaS platform uses machine learning to automatically identify, optimize, and execute repetitive tasks, reducing manual work by up to 80% while improving accuracy and compliance.",
                "team_background": "The founding team includes Sarah Chen, former engineering lead at Google with 10+ years in enterprise software who previously built automation tools at Slack, and Marcus Rodriguez, ex-McKinsey consultant with an MBA from Stanford who previously scaled sales at Salesforce and Box. The team brings deep expertise in workflow automation, enterprise sales, and AI/ML technologies.",
                "website": "https://techflow.io",
                "launch_year": "2023",
                "team_size": "12",
                "stage": "Series A",
                "market_size": "$15B TAM",
                "current_cash": "$800k in cash",
                "burn_rate": "$75k/month",
                "revenue": "$450k ARR",
                "prev_raised": "$2.5M Seed",
                "round_size": "$8M Series A",
                "post_money_valuation": "$35M",
                "use_of_capital": "Expanding engineering team, scaling sales operations, and developing new AI features for enterprise customers."
            }
    except Exception as e:
        st.error(f"Error generating test data: {e}")
        return None

# Welcome Page
if st.session_state.show_welcome:
    # Hide the main Streamlit elements
    st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="welcome-container">
        <h1 class="welcome-title">Investment Memo Generator</h1>
        <p class="welcome-subtitle">
            Transform company data into professional investment memos with AI-powered insights. 
            Just provide the basics and let AI handle the rest.
        </p>
        
        <div class="welcome-features">
            <div class="feature-card">
                <div class="feature-title">Simple Input</div>
                <div class="feature-desc">Just 3 key inputs - company name, description, and market</div>
            </div>
            <div class="feature-card">
                <div class="feature-title">AI Categorization</div>
                <div class="feature-desc">AI automatically populates all detailed fields</div>
            </div>
            <div class="feature-card">
                <div class="feature-title">Professional Output</div>
                <div class="feature-desc">Complete investment memo with market analysis</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Get started button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Get Started", use_container_width=True, type="primary"):
            st.session_state.show_welcome = False
            st.rerun()

# Main Application
else:
    # Sidebar for actions
    with st.sidebar:
        st.markdown("### Quick Actions")
        
        if st.button("Generate Test Data", use_container_width=True):
            with st.spinner("Creating test company..."):
                test_data = generate_test_company_data()
                if test_data:
                    st.success("Test data ready!")
                    st.session_state.test_data = test_data
                    st.rerun()
        
        st.markdown("---")
        st.markdown("### Process")
        st.markdown("1. Enter company details")
        st.markdown("2. AI categorizes data")
        st.markdown("3. Generate memo")

    # Main form
    with st.container():
        st.markdown('<h1 class="main-header fade-in">Investment Memo Generator</h1>', unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: center; color: #a0a0a0; margin-bottom: 2rem;'>
            Provide company details and let AI handle the rest
        </div>
        """, unsafe_allow_html=True)
        
        # Test data button at the top
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Generate Random Test Data", use_container_width=True, type="secondary"):
                with st.spinner("Creating random company data..."):
                    test_data = generate_test_company_data()
                    if test_data:
                        st.success("Random test data generated! Form has been populated.")
                        st.session_state.test_data = test_data
                        st.rerun()
        
        st.markdown("---")
        
        # Section 1: Company Idea, Market, How It Works
        st.markdown('<h2 class="section-header fade-in">Company Overview</h2>', unsafe_allow_html=True)
        st.markdown("""
        <div style='color: #a0a0a0; margin-bottom: 1rem;'>
            Describe the company idea, target market, and how the business works
        </div>
        """, unsafe_allow_html=True)
        
        company_overview = st.text_area("Company Idea, Market & How It Works", 
            value=st.session_state.get('test_data', {}).get('company_overview', ''),
            placeholder="Describe the company idea, target market, business model, and how the product/service works. Include the company name, what problem they solve, who their customers are, and how they make money.",
            height=150)

        # Section 2: Company Numbers (Structured Inputs)
        st.markdown('<h2 class="section-header fade-in">Financial & Company Metrics</h2>', unsafe_allow_html=True)
        st.markdown("""
        <div style='color: #a0a0a0; margin-bottom: 1rem;'>
            Key financial and company metrics
        </div>
        """, unsafe_allow_html=True)
        
        # Two columns for better organization
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            company_name = st.text_input("Company Name", 
                value=st.session_state.get('test_data', {}).get('company_name', ''),
                placeholder="Enter company name")
            
            website = st.text_input("Website", 
                value=st.session_state.get('test_data', {}).get('website', ''),
                placeholder="https://company.com")
            
            launch_year = st.text_input("Launch Year", 
                value=st.session_state.get('test_data', {}).get('launch_year', ''),
                placeholder="2023")
            
            team_size = st.text_input("Team Size", 
                value=st.session_state.get('test_data', {}).get('team_size', ''),
                placeholder="12")
            
            stage = st.selectbox("Stage", 
                ["Pre-seed", "Seed", "Series A", "Series B", "Series C", "Series D+"],
                index=2 if st.session_state.get('test_data', {}).get('stage', '') == 'Series A' else 0)
            
            market_size = st.text_input("Market Size (TAM)", 
                value=st.session_state.get('test_data', {}).get('market_size', ''),
                placeholder="$10B TAM")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            current_cash = st.text_input("Current Cash", 
                value=st.session_state.get('test_data', {}).get('current_cash', ''),
                placeholder="$500k in cash")
            
            burn_rate = st.text_input("Monthly Burn Rate", 
                value=st.session_state.get('test_data', {}).get('burn_rate', ''),
                placeholder="$50k/month")
            
            revenue = st.text_input("Revenue (ARR)", 
                value=st.session_state.get('test_data', {}).get('revenue', ''),
                placeholder="$200k ARR")
            
            prev_raised = st.text_input("Previously Raised", 
                value=st.session_state.get('test_data', {}).get('prev_raised', ''),
                placeholder="$2M Seed")
            
            round_size = st.text_input("Raising Round Size", 
                value=st.session_state.get('test_data', {}).get('round_size', ''),
                placeholder="$5M Series A")
            
            post_money_valuation = st.text_input("Post-Money Valuation", 
                value=st.session_state.get('test_data', {}).get('post_money_valuation', ''),
                placeholder="$25M")
            st.markdown('</div>', unsafe_allow_html=True)
        
        use_of_capital = st.text_area("Use of Capital", 
            value=st.session_state.get('test_data', {}).get('use_of_capital', ''),
            placeholder="What will they use the funding for?",
            height=80)

        # Section 3: Founder and Team Information
        st.markdown('<h2 class="section-header fade-in">Founding Team & Background</h2>', unsafe_allow_html=True)
        st.markdown("""
        <div style='color: #a0a0a0; margin-bottom: 1rem;'>
            Describe the founding team, their backgrounds, experience, and key team members
        </div>
        """, unsafe_allow_html=True)
        
        team_background = st.text_area("Founding Team & Background", 
            value=st.session_state.get('test_data', {}).get('team_background', ''),
            placeholder="Describe the founding team, their backgrounds, previous experience, education, achievements, and any other key team members. Include what makes them qualified to execute on this opportunity.",
            height=150)

        # Generate Memo Button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Generate Investment Memo", use_container_width=True, type="primary"):
                if not company_name or not company_overview or not team_background:
                    st.error("Please fill in all three main sections: Company Overview, Company Name, and Team Background.")
                else:
                    with st.spinner("Categorizing company data and generating memo..."):
                        # Extract market category from company overview using AI
                        market_extraction_prompt = f"""
                        Based on this company overview, extract the market category:
                        
                        Company Overview: {company_overview}
                        
                        Return only the market category (e.g., "Fintech", "Healthtech", "Edtech", "Enterprise SaaS", "Consumer", "Marketplace", "Hardware", etc.) in a single word or short phrase.
                        """
                        
                        try:
                            client = openai.OpenAI(api_key=openai.api_key)
                            market_response = client.chat.completions.create(
                                model="gpt-4",
                                messages=[{"role": "user", "content": market_extraction_prompt}],
                                temperature=0.3,
                                max_tokens=50
                            )
                            market_category = market_response.choices[0].message.content.strip()
                        except:
                            market_category = "Technology"
                        
                        # First, categorize and populate all the detailed fields
                        categorized_data = categorize_company_data(company_name, company_overview, market_category)
                        
                        if categorized_data:
                            # Build the complete company data dictionary
                            company_data = {
                                "company_name": company_name,
                                "website": website or categorized_data.get("website", ""),
                                "launch_year": launch_year or categorized_data.get("launch_year", ""),
                                "team_size": team_size or categorized_data.get("team_size", ""),
                                "stage": stage or categorized_data.get("stage", ""),
                                "one_liner": categorized_data.get("one_liner", ""),
                                "company_description": company_overview,
                                "market_size": market_size or categorized_data.get("market_size", ""),
                                "current_cash": current_cash or categorized_data.get("current_cash", ""),
                                "burn_rate": burn_rate or categorized_data.get("burn_rate", ""),
                                "revenue": revenue or categorized_data.get("revenue", ""),
                                "prev_raised": prev_raised or categorized_data.get("prev_raised", ""),
                                "round_size": round_size or categorized_data.get("round_size", ""),
                                "post_money_valuation": post_money_valuation or categorized_data.get("post_money_valuation", ""),
                                "use_of_capital": use_of_capital or categorized_data.get("use_of_capital", ""),
                                "market": market_category,
                                "named_competitors": categorized_data.get("named_competitors", ""),
                                "founder_1_name": categorized_data.get("founder_1_name", ""),
                                "founder_1_bio": categorized_data.get("founder_1_bio", ""),
                                "founder_2_name": categorized_data.get("founder_2_name", ""),
                                "founder_2_bio": categorized_data.get("founder_2_bio", ""),
                                "founder_3_name": categorized_data.get("founder_3_name", ""),
                                "founder_3_bio": categorized_data.get("founder_3_bio", ""),
                                "founder_4_name": categorized_data.get("founder_4_name", ""),
                                "founder_4_bio": categorized_data.get("founder_4_bio", ""),
                                "misc_notes": team_background,
                                "pros": categorized_data.get("pros", ""),
                                "cons": categorized_data.get("cons", ""),
                                "best_case": categorized_data.get("best_case", ""),
                                "worst_case": categorized_data.get("worst_case", "")
                            }
                            
                            # Use a simple formatter to replace placeholders in the base_prompt
                            def format_prompt(data, prompt):
                                formatted = prompt
                                for key, value in data.items():
                                    formatted = formatted.replace("{{" + key + "}}", str(value))
                                return formatted

                            # Load your base prompt
                            with open("base_prompt.txt", "r") as f:
                                base_prompt = f.read()
                            
                            final_prompt = format_prompt(company_data, base_prompt)
                            
                            # Call OpenAI's API
                            try:
                                client = openai.OpenAI(api_key=openai.api_key)
                                response = client.chat.completions.create(
                                    model="gpt-4",
                                    messages=[{"role": "user", "content": final_prompt}],
                                    temperature=0.7,
                                    max_tokens=1000
                                )
                                generated_memo = response.choices[0].message.content
                                
                                st.success("Investment memo generated successfully!")
                                st.markdown("---")
                                st.markdown("## Generated Investment Memo")
                                
                                # Display memo with proper styling
                                st.markdown(f"""
                                <div class="memo-container">
                                    {generated_memo}
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Market Analysis Section
                                st.markdown("---")
                                st.markdown("## Market Analysis")
                                
                                # Function to analyze market data
                                def analyze_market_data(market_category, market_size, revenue, stage):
                                    analysis_prompt = f"""
                                    Analyze this startup's market position:
                                    
                                    Market Category: {market_category}
                                    Market Size (TAM): {market_size}
                                    Current Revenue: {revenue}
                                    Stage: {stage}
                                    
                                    Provide analysis in JSON format with:
                                    - market_penetration_percentage: Calculate what percentage of TAM they've captured
                                    - typical_penetration_range: Typical range for companies at this stage in this market
                                    - market_opportunity: Remaining market opportunity
                                    - competitive_position: How they compare to typical companies
                                    - growth_potential: Assessment of growth potential
                                    - market_maturity: Is this market early, growing, or mature
                                    - stage_appropriateness: Is their penetration appropriate for their stage
                                    
                                    Return only valid JSON.
                                    """
                                    
                                    try:
                                        client = openai.OpenAI(api_key=openai.api_key)
                                        response = client.chat.completions.create(
                                            model="gpt-4",
                                            messages=[{"role": "user", "content": analysis_prompt}],
                                            temperature=0.3,
                                            max_tokens=800
                                        )
                                        
                                        import json
                                        data_text = response.choices[0].message.content
                                        
                                        # Extract JSON
                                        start_idx = data_text.find('{')
                                        end_idx = data_text.rfind('}') + 1
                                        json_str = data_text[start_idx:end_idx]
                                        return json.loads(json_str)
                                    except Exception as e:
                                        st.error(f"Error analyzing market data: {e}")
                                        return None
                                
                                # Perform market analysis
                                final_market_size = market_size or categorized_data.get("market_size")
                                final_revenue = revenue or categorized_data.get("revenue")
                                final_stage = stage or categorized_data.get("stage")
                                
                                if market_category and final_market_size and final_revenue:
                                    with st.spinner("Analyzing market position..."):
                                        market_analysis = analyze_market_data(market_category, final_market_size, final_revenue, final_stage)
                                        
                                        if market_analysis:
                                            # Display market analysis
                                            col1, col2 = st.columns(2)
                                            
                                            with col1:
                                                st.markdown("### Market Position Analysis")
                                                st.metric("Market Penetration", 
                                                         f"{market_analysis.get('market_penetration_percentage', 'N/A')}%")
                                                st.metric("Typical Range", 
                                                         market_analysis.get('typical_penetration_range', 'N/A'))
                                                st.metric("Market Maturity", 
                                                         market_analysis.get('market_maturity', 'N/A'))
                                            
                                            with col2:
                                                st.markdown("### Growth Assessment")
                                                st.metric("Remaining Opportunity", 
                                                         market_analysis.get('market_opportunity', 'N/A'))
                                                st.metric("Competitive Position", 
                                                         market_analysis.get('competitive_position', 'N/A'))
                                                st.metric("Stage Appropriateness", 
                                                         market_analysis.get('stage_appropriateness', 'N/A'))
                                            
                                            # Market penetration visualization
                                            st.markdown("### Market Penetration Visualization")
                                            
                                            try:
                                                import plotly.graph_objects as go
                                                import plotly.express as px
                                                
                                                # Extract percentage for visualization
                                                penetration_text = market_analysis.get('market_penetration_percentage', '0')
                                                if isinstance(penetration_text, str):
                                                    penetration = float(penetration_text.replace('%', '').replace(',', ''))
                                                else:
                                                    penetration = float(penetration_text)
                                                
                                                # Create gauge chart for market penetration
                                                fig = go.Figure(go.Indicator(
                                                    mode = "gauge+number+delta",
                                                    value = penetration,
                                                    domain = {'x': [0, 1], 'y': [0, 1]},
                                                    title = {'text': f"Market Penetration (%)"},
                                                    delta = {'reference': 5},  # Typical early stage
                                                    gauge = {
                                                        'axis': {'range': [None, 100]},
                                                        'bar': {'color': "#3b82f6"},
                                                        'steps': [
                                                            {'range': [0, 5], 'color': "lightgray"},
                                                            {'range': [5, 20], 'color': "yellow"},
                                                            {'range': [20, 100], 'color': "green"}
                                                        ],
                                                        'threshold': {
                                                            'line': {'color': "red", 'width': 4},
                                                            'thickness': 0.75,
                                                            'value': 90
                                                        }
                                                    }
                                                ))
                                                
                                                fig.update_layout(
                                                    title=f"{company_name} - Market Penetration Analysis",
                                                    font=dict(size=14),
                                                    height=400
                                                )
                                                
                                                st.plotly_chart(fig, use_container_width=True)
                                                
                                                # Market opportunity pie chart
                                                if penetration < 100:
                                                    remaining = 100 - penetration
                                                    
                                                    fig2 = go.Figure(data=[go.Pie(
                                                        labels=['Captured Market', 'Remaining Opportunity'],
                                                        values=[penetration, remaining],
                                                        hole=.3,
                                                        marker_colors=['#3b82f6', '#e5e7eb']
                                                    )])
                                                    
                                                    fig2.update_layout(
                                                        title=f"Market Opportunity Breakdown",
                                                        height=400
                                                    )
                                                    
                                                    st.plotly_chart(fig2, use_container_width=True)
                                                
                                                # Growth potential assessment
                                                st.markdown("### Growth Potential Assessment")
                                                growth_potential = market_analysis.get('growth_potential', 'N/A')
                                                st.info(f"**Growth Potential:** {growth_potential}")
                                                
                                            except ImportError:
                                                st.warning("Plotly not available. Install with: pip install plotly")
                                                st.json(market_analysis)
                                            
                                            # Market insights
                                            st.markdown("### Market Insights")
                                            insights = f"""
                                            **Market Category:** {market_category}
                                            **Total Addressable Market:** {final_market_size}
                                            **Current Revenue:** {final_revenue}
                                            **Company Stage:** {final_stage}
                                            
                                            **Key Insights:**
                                            - Market Penetration: {market_analysis.get('market_penetration_percentage', 'N/A')}%
                                            - Typical Range for {final_stage} companies: {market_analysis.get('typical_penetration_range', 'N/A')}
                                            - Market Maturity: {market_analysis.get('market_maturity', 'N/A')}
                                            - Competitive Position: {market_analysis.get('competitive_position', 'N/A')}
                                            """
                                            st.markdown(insights)
                                
                                # Download button
                                st.download_button(
                                    label="Download Memo as Markdown",
                                    data=generated_memo,
                                    file_name=f"{company_name}_investment_memo.md",
                                    mime="text/markdown"
                                )
                                
                            except Exception as e:
                                st.error(f"Error generating memo: {e}")
                        else:
                            st.error("Failed to categorize company data. Please try again.")
