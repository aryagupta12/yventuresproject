import streamlit as st
import openai
import random
import tempfile
import os
import io
import json
try:
    from PIL import Image
    import pytesseract
    IMAGE_PROCESSING_AVAILABLE = True
except ImportError:
    IMAGE_PROCESSING_AVAILABLE = False

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
    - tam: Total Addressable Market (e.g., "$50B")
    - sam: Serviceable Addressable Market (e.g., "$5B")
    - som: Serviceable Obtainable Market (e.g., "$500M")
    - current_cash: Current cash position (e.g., "$500k in cash")
    - burn_rate: Monthly burn rate (e.g., "$50k/month")
    - revenue: Current revenue (e.g., "$200k ARR")
    - prev_raised: Previously raised amount (e.g., "$2M Seed")
    - round_size: Current round size (e.g., "$5M Series A")
    - post_money_valuation: Post-money valuation (e.g., "$25M")
    - use_of_capital: What they need money for (2-3 sentences)
    
    Make it realistic and varied - could be any type of startup (SaaS, marketplace, hardware, etc.)
    Make SAM about 10-20% of TAM and SOM about 10-20% of SAM.
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
                "tam": "$50B",
                "sam": "$5B",
                "som": "$500M",
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

# Function to generate market size hierarchy visualization
def create_market_size_hierarchy(tam, sam, som, company_name):
    """
    Create a Plotly visualization showing TAM > SAM > SOM hierarchy
    If any values are missing, use AI to estimate them
    """
    try:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        
        # If any values are missing, use AI to estimate them
        if not tam or not sam or not som:
            estimation_prompt = f"""
            Estimate realistic market size numbers for this company:
            
            Company: {company_name}
            Current TAM: {tam or 'Not provided'}
            Current SAM: {sam or 'Not provided'} 
            Current SOM: {som or 'Not provided'}
            
            Return only a JSON object with:
            - tam: Total Addressable Market (e.g., "$50B")
            - sam: Serviceable Addressable Market (e.g., "$5B") 
            - som: Serviceable Obtainable Market (e.g., "$500M")
            
            Make SAM about 10-20% of TAM and SOM about 10-20% of SAM.
            Return only valid JSON.
            """
            
            try:
                client = openai.OpenAI(api_key=openai.api_key)
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": estimation_prompt}],
                    temperature=0.3,
                    max_tokens=200
                )
                
                import json
                data_text = response.choices[0].message.content
                start_idx = data_text.find('{')
                end_idx = data_text.rfind('}') + 1
                json_str = data_text[start_idx:end_idx]
                estimated_data = json.loads(json_str)
                
                tam = tam or estimated_data.get('tam', '$50B')
                sam = sam or estimated_data.get('sam', '$5B')
                som = som or estimated_data.get('som', '$500M')
                
            except:
                # Fallback values
                tam = tam or '$50B'
                sam = sam or '$5B' 
                som = som or '$500M'
        
        # Extract numeric values for visualization
        def extract_number(value_str):
            if not value_str:
                return 1
            # Remove common prefixes and convert to number
            value_str = str(value_str).upper().replace('$', '').replace('B', '000000000').replace('M', '000000').replace('K', '000')
            try:
                return float(value_str)
            except:
                return 1
        
        tam_num = extract_number(tam)
        sam_num = extract_number(sam)
        som_num = extract_number(som)
        
        # Create the visualization
        fig = go.Figure()
        
        # TAM (outer circle)
        fig.add_trace(go.Scatter(
            x=[0], y=[0],
            mode='markers+text',
            marker=dict(
                size=300,
                color='lightblue',
                line=dict(color='blue', width=3)
            ),
            text=[f'TAM<br>{tam}'],
            textposition='middle center',
            textfont=dict(size=16, color='darkblue'),
            name='TAM',
            showlegend=False
        ))
        
        # SAM (middle circle)
        fig.add_trace(go.Scatter(
            x=[0], y=[0],
            mode='markers+text',
            marker=dict(
                size=200,
                color='lightgreen',
                line=dict(color='green', width=3)
            ),
            text=[f'SAM<br>{sam}'],
            textposition='middle center',
            textfont=dict(size=14, color='darkgreen'),
            name='SAM',
            showlegend=False
        ))
        
        # SOM (inner circle)
        fig.add_trace(go.Scatter(
            x=[0], y=[0],
            mode='markers+text',
            marker=dict(
                size=100,
                color='lightcoral',
                line=dict(color='red', width=3)
            ),
            text=[f'SOM<br>{som}'],
            textposition='middle center',
            textfont=dict(size=12, color='darkred'),
            name='SOM',
            showlegend=False
        ))
        
        # Add legend
        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode='markers',
            marker=dict(size=10, color='lightblue'),
            name=f'TAM: {tam}',
            showlegend=True
        ))
        
        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode='markers',
            marker=dict(size=10, color='lightgreen'),
            name=f'SAM: {sam}',
            showlegend=True
        ))
        
        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode='markers',
            marker=dict(size=10, color='lightcoral'),
            name=f'SOM: {som}',
            showlegend=True
        ))
        
        fig.update_layout(
            title=f'{company_name} - Market Size Hierarchy',
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1, 1]),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1, 1]),
            plot_bgcolor='white',
            height=500,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
        
    except ImportError:
        st.warning("Plotly not available. Install with: pip install plotly")
        return None
    except Exception as e:
        st.error(f"Error creating market size visualization: {e}")
        return None

# Function to create investment stage visualization
def create_investment_stage_visualization(stage, company_name, revenue, burn_rate, team_size, prev_raised, round_size):
    """
    Create a Plotly visualization showing the startup's investment stage and typical metrics
    """
    try:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        
        # Define typical metrics for each stage
        stage_metrics = {
            "Pre-seed": {
                "typical_revenue": "$0-50k",
                "typical_burn": "$10-30k/month",
                "typical_team": "2-5 people",
                "typical_valuation": "$1-5M",
                "typical_round": "$100k-500k",
                "color": "#FF6B6B",
                "description": "Idea validation, MVP development"
            },
            "Seed": {
                "typical_revenue": "$50k-500k",
                "typical_burn": "$30-100k/month",
                "typical_team": "5-15 people",
                "typical_valuation": "$5-15M",
                "typical_round": "$500k-2M",
                "color": "#4ECDC4",
                "description": "Product-market fit, early customers"
            },
            "Series A": {
                "typical_revenue": "$500k-5M",
                "typical_burn": "$100-500k/month",
                "typical_team": "15-50 people",
                "typical_valuation": "$15-50M",
                "typical_round": "$2-15M",
                "color": "#45B7D1",
                "description": "Scaling, market expansion"
            },
            "Series B": {
                "typical_revenue": "$5-50M",
                "typical_burn": "$500k-2M/month",
                "typical_team": "50-200 people",
                "typical_valuation": "$50-200M",
                "typical_round": "$15-50M",
                "color": "#96CEB4",
                "description": "Rapid growth, market leadership"
            },
            "Series C": {
                "typical_revenue": "$50M+",
                "typical_burn": "$2M+/month",
                "typical_team": "200+ people",
                "typical_valuation": "$200M+",
                "typical_round": "$50M+",
                "color": "#FFEAA7",
                "description": "Market dominance, IPO preparation"
            },
            "Series D+": {
                "typical_revenue": "$100M+",
                "typical_burn": "$5M+/month",
                "typical_team": "500+ people",
                "typical_valuation": "$500M+",
                "typical_round": "$100M+",
                "color": "#DDA0DD",
                "description": "Late-stage, exit preparation"
            }
        }
        
        # Get current stage metrics
        current_stage = stage or "Series A"
        stage_data = stage_metrics.get(current_stage, stage_metrics["Series A"])
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Investment Stage Timeline', 'Current vs Typical Metrics', 'Team Size Comparison', 'Financial Health'),
            specs=[[{"type": "bar"}, {"type": "indicator"}],
                   [{"type": "bar"}, {"type": "indicator"}]],
            vertical_spacing=0.1,
            horizontal_spacing=0.1
        )
        
        # 1. Investment Stage Timeline
        stages = list(stage_metrics.keys())
        stage_colors = [stage_metrics[s]["color"] for s in stages]
        current_index = stages.index(current_stage) if current_stage in stages else 2
        
        # Create timeline bars
        for i, stage_name in enumerate(stages):
            color = stage_colors[i]
            opacity = 1.0 if i <= current_index else 0.3
            fig.add_trace(
                go.Bar(
                    x=[stage_name],
                    y=[1],
                    name=stage_name,
                    marker_color=color,
                    opacity=opacity,
                    showlegend=False
                ),
                row=1, col=1
            )
        
        # 2. Current vs Typical Revenue
        try:
            # Extract numeric revenue value
            revenue_str = str(revenue or "0").upper()
            revenue_num = 0
            if "M" in revenue_str:
                revenue_num = float(revenue_str.replace("M", "").replace("$", "").replace(" ", "")) * 1000000
            elif "K" in revenue_str:
                revenue_num = float(revenue_str.replace("K", "").replace("$", "").replace(" ", "")) * 1000
            else:
                revenue_num = float(revenue_str.replace("$", "").replace(" ", ""))
        except:
            revenue_num = 0
        
        # Estimate typical revenue for comparison
        typical_revenue_str = stage_data["typical_revenue"]
        typical_revenue_num = 0
        
        try:
            # Handle range values like "$0-50k" or "$500k-5M"
            if "-" in typical_revenue_str:
                # Split the range and take the higher end
                range_parts = typical_revenue_str.split("-")
                if len(range_parts) == 2:
                    higher_end = range_parts[1].strip()
                    if "M" in higher_end:
                        typical_revenue_num = float(higher_end.replace("M", "").replace("$", "").replace(" ", "")) * 1000000
                    elif "K" in higher_end:
                        typical_revenue_num = float(higher_end.replace("K", "").replace("$", "").replace(" ", "")) * 1000
                    else:
                        typical_revenue_num = float(higher_end.replace("$", "").replace(" ", ""))
                else:
                    # Fallback to simple conversion
                    if "M" in typical_revenue_str:
                        typical_revenue_num = float(typical_revenue_str.replace("M", "").replace("$", "").replace(" ", "")) * 1000000
                    elif "K" in typical_revenue_str:
                        typical_revenue_num = float(typical_revenue_str.replace("K", "").replace("$", "").replace(" ", "")) * 1000
                    else:
                        typical_revenue_num = float(typical_revenue_str.replace("$", "").replace(" ", ""))
            else:
                # Handle single values
                if "M" in typical_revenue_str:
                    typical_revenue_num = float(typical_revenue_str.replace("M", "").replace("$", "").replace(" ", "")) * 1000000
                elif "K" in typical_revenue_str:
                    typical_revenue_num = float(typical_revenue_str.replace("K", "").replace("$", "").replace(" ", "")) * 1000
                else:
                    typical_revenue_num = float(typical_revenue_str.replace("$", "").replace(" ", ""))
        except:
            # Fallback values based on stage
            fallback_values = {
                "Pre-seed": 25000,  # $25k (middle of $0-50k)
                "Seed": 275000,     # $275k (middle of $50k-500k)
                "Series A": 2750000, # $2.75M (middle of $500k-5M)
                "Series B": 27500000, # $27.5M (middle of $5M-50M)
                "Series C": 100000000, # $100M+ (minimum)
                "Series D+": 200000000  # $200M+ (minimum)
            }
            typical_revenue_num = fallback_values.get(current_stage, 2750000)
        
        # Revenue comparison gauge
        revenue_percentage = min(100, (revenue_num / typical_revenue_num) * 100) if typical_revenue_num > 0 else 0
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=revenue_percentage,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Revenue vs Typical"},
                delta={'reference': 100},
                gauge={
                    'axis': {'range': [None, 200]},
                    'bar': {'color': stage_data["color"]},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 100], 'color': "yellow"},
                        {'range': [100, 200], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 150
                    }
                }
            ),
            row=1, col=2
        )
        
        # 3. Team Size Comparison
        try:
            team_size_num = int(str(team_size or "0").replace(" ", ""))
        except:
            team_size_num = 0
        
        # Estimate typical team size
        typical_team_str = stage_data["typical_team"]
        typical_team_num = 0
        
        try:
            # Handle range values like "2-5 people" or "50-200 people"
            if "-" in typical_team_str:
                # Split the range and take the higher end
                range_parts = typical_team_str.split("-")
                if len(range_parts) == 2:
                    higher_end = range_parts[1].strip()
                    # Remove "people" and "+" if present
                    higher_end = higher_end.replace(" people", "").replace("+", "").strip()
                    typical_team_num = int(higher_end)
                else:
                    # Fallback to simple conversion
                    typical_team_str = typical_team_str.replace(" people", "").replace("+", "").strip()
                    typical_team_num = int(typical_team_str)
            else:
                # Handle single values
                typical_team_str = typical_team_str.replace(" people", "").replace("+", "").strip()
                typical_team_num = int(typical_team_str)
        except:
            # Fallback values based on stage
            fallback_values = {
                "Pre-seed": 4,    # Middle of 2-5
                "Seed": 10,       # Middle of 5-15
                "Series A": 32,   # Middle of 15-50
                "Series B": 125,  # Middle of 50-200
                "Series C": 250,  # 200+ (minimum)
                "Series D+": 500  # 500+ (minimum)
            }
            typical_team_num = fallback_values.get(current_stage, 32)
        
        # Team size comparison
        fig.add_trace(
            go.Bar(
                x=['Current Team', 'Typical for Stage'],
                y=[team_size_num, typical_team_num],
                marker_color=[stage_data["color"], "lightgray"],
                name="Team Size",
                showlegend=False
            ),
            row=2, col=1
        )
        
        # 4. Burn Rate Health
        try:
            # Extract burn rate
            burn_str = str(burn_rate or "0").upper()
            burn_num = 0
            if "M" in burn_str:
                burn_num = float(burn_str.replace("M", "").replace("$", "").replace(" ", "").replace("/month", "")) * 1000000
            elif "K" in burn_str:
                burn_num = float(burn_str.replace("K", "").replace("$", "").replace(" ", "").replace("/month", "")) * 1000
            else:
                burn_num = float(burn_str.replace("$", "").replace(" ", "").replace("/month", ""))
        except:
            burn_num = 0
        
        # Calculate runway (assuming current cash from previous data)
        try:
            cash_str = str(prev_raised or "0").upper()
            cash_num = 0
            if "M" in cash_str:
                cash_num = float(cash_str.replace("M", "").replace("$", "").replace(" ", "")) * 1000000
            elif "K" in cash_str:
                cash_num = float(cash_str.replace("K", "").replace("$", "").replace(" ", "")) * 1000
            else:
                cash_num = float(cash_str.replace("$", "").replace(" ", ""))
        except:
            cash_num = 0
        
        runway_months = (cash_num / burn_num) if burn_num > 0 else 0
        runway_percentage = min(100, (runway_months / 18) * 100)  # 18 months is healthy runway
        
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=runway_percentage,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Runway Health (months)"},
                delta={'reference': 100},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': stage_data["color"]},
                    'steps': [
                        {'range': [0, 6], 'color': "red"},
                        {'range': [6, 12], 'color': "yellow"},
                        {'range': [12, 100], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 18
                    }
                }
            ),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title=f'{company_name} - Investment Stage Analysis',
            height=800,
            showlegend=False,
            plot_bgcolor='white'
        )
        
        # Update axes
        fig.update_xaxes(showgrid=False, zeroline=False)
        fig.update_yaxes(showgrid=False, zeroline=False)
        
        return fig
        
    except ImportError:
        st.warning("Plotly not available. Install with: pip install plotly")
        return None
    except Exception as e:
        st.error(f"Error creating investment stage visualization: {e}")
        return None

# Function to convert memo to PDF
def convert_memo_to_pdf(final_memo, company_name, market_hierarchy_fig=None, stage_analysis_fig=None):
    """
    Convert the investment memo and analysis to PDF format
    """
    try:
        # Create HTML content with proper styling
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{company_name} - Investment Memo</title>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                h1 {{
                    color: #2c3e50;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                    page-break-after: avoid;
                }}
                h2 {{
                    color: #34495e;
                    border-bottom: 2px solid #3498db;
                    padding-bottom: 5px;
                    margin-top: 30px;
                    page-break-before: always;
                }}
                h3 {{
                    color: #7f8c8d;
                    margin-top: 20px;
                }}
                p {{
                    margin-bottom: 15px;
                    text-align: justify;
                }}
                ul, ol {{
                    margin-bottom: 15px;
                    padding-left: 20px;
                }}
                li {{
                    margin-bottom: 5px;
                }}
                strong {{
                    color: #2c3e50;
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                    border-bottom: 2px solid #3498db;
                    padding-bottom: 20px;
                }}
                .company-name {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #2c3e50;
                    margin-bottom: 10px;
                }}
                .date {{
                    color: #7f8c8d;
                    font-style: italic;
                }}
                .section {{
                    margin-bottom: 30px;
                }}
                .page-break {{
                    page-break-before: always;
                }}
                @media print {{
                    h2 {{
                        page-break-before: always;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="company-name">{company_name}</div>
                <div class="date">Investment Memo & Analysis</div>
                <div class="date">{random.choice(['Generated on', 'Prepared on', 'Analysis Date'])}: {random.choice(['2024', '2025'])}</div>
            </div>
            
            {final_memo.replace('# ', '<h1>').replace('## ', '<h2>').replace('### ', '<h3>').replace('**', '<strong>').replace('**', '</strong>')}
            
            <div class="page-break">
                <h2>Market Analysis Summary</h2>
                <p>This investment memo includes comprehensive market analysis, investment stage assessment, and venture capital evaluation.</p>
                <p>The analysis is based on the provided company information and industry benchmarks for companies at similar stages.</p>
            </div>
            
            <div class="page-break">
                <h2>Key Investment Considerations</h2>
                <ul>
                    <li><strong>Market Opportunity:</strong> Evaluate the TAM, SAM, and SOM analysis provided</li>
                    <li><strong>Team Assessment:</strong> Review the founding team's background and capabilities</li>
                    <li><strong>Financial Health:</strong> Consider the current financial metrics and runway</li>
                    <li><strong>Competitive Position:</strong> Assess the company's competitive advantages</li>
                    <li><strong>Risk Factors:</strong> Review the identified risks and mitigation strategies</li>
                </ul>
            </div>
        </body>
        </html>
        """
        
        # Try to use weasyprint first (more reliable)
        try:
            from weasyprint import HTML
            # Create PDF using weasyprint
            pdf_bytes = HTML(string=html_content).write_pdf()
            return pdf_bytes
        except ImportError:
            # Fallback to pdfkit if weasyprint is not available
            try:
                import pdfkit
                # Configure pdfkit options
                options = {
                    'page-size': 'A4',
                    'margin-top': '0.75in',
                    'margin-right': '0.75in',
                    'margin-bottom': '0.75in',
                    'margin-left': '0.75in',
                    'encoding': "UTF-8",
                    'no-outline': None
                }
                
                # Create PDF using pdfkit
                pdf_bytes = pdfkit.from_string(html_content, False, options=options)
                return pdf_bytes
            except ImportError:
                st.error("PDF generation libraries not available. Install with: pip install weasyprint or pip install pdfkit")
                return None
                
    except Exception as e:
        st.error(f"Error generating PDF: {e}")
        return None

# Google Drive API and file processing functions
def setup_google_drive_api():
    """
    Setup Google Drive API client
    Note: This requires credentials.json file for authentication
    """
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import Flow
        from googleapiclient.discovery import build
        from google.auth.transport.requests import Request
        import pickle
        
        SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
        
        creds = None
        # Check if token.pickle exists (stored credentials)
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # This requires credentials.json from Google Cloud Console
                if os.path.exists('credentials.json'):
                    flow = Flow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                    flow.redirect_uri = 'http://localhost:8080'
                    
                    auth_url, _ = flow.authorization_url(prompt='consent')
                    st.warning(f"Please visit this URL to authorize the application: {auth_url}")
                    return None
                else:
                    st.error("Google Drive API credentials not found. Please add credentials.json file.")
                    return None
            
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        service = build('drive', 'v3', credentials=creds)
        return service
    
    except ImportError:
        st.error("Google Drive API libraries not installed. Run: pip install -r requirements.txt")
        return None
    except Exception as e:
        st.error(f"Error setting up Google Drive API: {e}")
        return None

def extract_text_from_pdf(file_bytes):
    """Extract text from PDF file"""
    try:
        import PyPDF2
        
        pdf_file = io.BytesIO(file_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
    
    except ImportError:
        st.error("PDF processing library not available. Install with: pip install PyPDF2")
        return None
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return None

def extract_text_from_docx(file_bytes):
    """Extract text from Word document"""
    try:
        from docx import Document
        
        doc_file = io.BytesIO(file_bytes)
        doc = Document(doc_file)
        
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        
        return text.strip()
    
    except ImportError:
        st.error("Word document processing library not available. Install with: pip install python-docx")
        return None
    except Exception as e:
        st.error(f"Error extracting text from Word document: {e}")
        return None

def extract_text_from_excel(file_bytes):
    """Extract text from Excel file"""
    try:
        import pandas as pd
        
        excel_file = io.BytesIO(file_bytes)
        
        # Read all sheets
        excel_data = pd.read_excel(excel_file, sheet_name=None)
        
        text = ""
        for sheet_name, df in excel_data.items():
            text += f"Sheet: {sheet_name}\n"
            text += df.to_string(index=False) + "\n\n"
        
        return text.strip()
    
    except ImportError:
        st.error("Excel processing library not available. Install with: pip install openpyxl pandas")
        return None
    except Exception as e:
        st.error(f"Error extracting text from Excel file: {e}")
        return None

def extract_text_from_image(file_bytes):
    """Extract text from image using OCR"""
    if not IMAGE_PROCESSING_AVAILABLE:
        st.error("Image processing libraries not available. Install with: pip install pillow pytesseract")
        st.info("Also ensure Tesseract OCR is installed on your system")
        return None
    
    try:
        # Open image from bytes
        image = Image.open(io.BytesIO(file_bytes))
        
        # Use OCR to extract text
        text = pytesseract.image_to_string(image)
        
        return text.strip()
    
    except Exception as e:
        st.error(f"Error extracting text from image: {e}")
        st.info("Make sure Tesseract OCR is installed on your system")
        return None

def process_uploaded_file(uploaded_file):
    """Process uploaded file and extract text content"""
    if uploaded_file is None:
        return None
    
    file_bytes = uploaded_file.read()
    file_name = uploaded_file.name.lower()
    
    # Reset file pointer
    uploaded_file.seek(0)
    
    text_content = None
    
    if file_name.endswith('.pdf'):
        text_content = extract_text_from_pdf(file_bytes)
    elif file_name.endswith('.docx'):
        text_content = extract_text_from_docx(file_bytes)
    elif file_name.endswith(('.xlsx', '.xls')):
        text_content = extract_text_from_excel(file_bytes)
    elif file_name.endswith('.txt'):
        text_content = file_bytes.decode('utf-8')
    elif file_name.endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
        text_content = extract_text_from_image(file_bytes)
    else:
        st.error(f"Unsupported file type: {file_name}")
        return None
    
    return text_content

def extract_company_info_from_text(text_content):
    """Use AI to extract company information from document text"""
    if not text_content:
        return None
    
    extraction_prompt = f"""
    Analyze the following document text and extract company information for an investment memo.
    
    Document Content:
    {text_content[:4000]}  # Limit to first 4000 characters to avoid token limits
    
    Extract and return the following information in JSON format:
    - company_name: Company name if mentioned
    - company_overview: Business description, what they do, target market, business model (3-4 sentences)
    - team_background: Information about founders, team members, their backgrounds (if available)
    - financials: Any financial information mentioned (revenue, funding, burn rate, etc.)
    - market_info: Market size, competitors, market opportunity (if mentioned)
    - stage: Investment stage if mentioned (Pre-seed, Seed, Series A, etc.)
    - key_metrics: Important numbers or KPIs mentioned
    - additional_notes: Any other relevant information for investment analysis
    
    If information is not available in the document, set the field to empty string.
    Return only valid JSON.
    """
    
    try:
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": extraction_prompt}],
            temperature=0.3,
            max_tokens=1500
        )
        
        data_text = response.choices[0].message.content
        
        # Extract JSON from response
        start_idx = data_text.find('{')
        end_idx = data_text.rfind('}') + 1
        json_str = data_text[start_idx:end_idx]
        
        return json.loads(json_str)
    
    except Exception as e:
        st.error(f"Error extracting company information: {e}")
        return None

def download_from_google_drive(file_id, service):
    """Download file from Google Drive using file ID"""
    try:
        from googleapiclient.http import MediaIoBaseDownload
        
        request = service.files().get_media(fileId=file_id)
        file_io = io.BytesIO()
        downloader = MediaIoBaseDownload(file_io, request)
        
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        
        file_io.seek(0)
        return file_io.getvalue()
    
    except Exception as e:
        st.error(f"Error downloading from Google Drive: {e}")
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
                    st.session_state.test_data = test_data
                    st.rerun()
        
        st.markdown("---")
        st.markdown("### Supported Files")
        st.markdown("📄 PDF • 📝 Word • 📊 Excel • 📋 Text • 🖼️ Images")

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
                        st.session_state.test_data = test_data
                        st.rerun()
        
        st.markdown("---")
        
        # File Upload Section
        st.markdown('<h2 class="section-header fade-in">📁 Document Upload & Analysis</h2>', unsafe_allow_html=True)
        
        # Create tabs for different upload methods
        upload_tab1, upload_tab2 = st.tabs(["📤 Upload Files", "🔗 Google Drive"])
        
        with upload_tab1:
            uploaded_files = st.file_uploader(
                "Choose files",
                type=['pdf', 'docx', 'xlsx', 'xls', 'txt', 'png', 'jpg', 'jpeg', 'tiff', 'bmp'],
                accept_multiple_files=True,
                help="Upload documents, images, or files"
            )
            
            if uploaded_files:
                # Process uploaded files
                if st.button("🔍 Extract Information from Files", use_container_width=True, type="primary"):
                    extracted_data = {}
                    all_text_content = ""
                    
                    with st.spinner("Processing uploaded files..."):
                        for uploaded_file in uploaded_files:
                            # Extract text from file
                            text_content = process_uploaded_file(uploaded_file)
                            
                            if text_content:
                                all_text_content += f"\n\n=== {uploaded_file.name} ===\n{text_content}"
                    
                    if all_text_content:
                        # Use AI to extract company information
                        with st.spinner("Analyzing documents with AI..."):
                            extracted_info = extract_company_info_from_text(all_text_content)
                            
                            if extracted_info:
                                # Store extracted data in session state
                                st.session_state.extracted_data = extracted_info
                                
                                # Display extracted information
                                with st.expander("📋 Extracted Information", expanded=True):
                                    col1, col2 = st.columns(2)
                                    
                                    with col1:
                                        if extracted_info.get('company_name'):
                                            st.metric("Company Name", extracted_info['company_name'])
                                        if extracted_info.get('stage'):
                                            st.metric("Stage", extracted_info['stage'])
                                        if extracted_info.get('financials'):
                                            st.text_area("Financial Info", extracted_info['financials'], height=100, disabled=True)
                                    
                                    with col2:
                                        if extracted_info.get('market_info'):
                                            st.text_area("Market Info", extracted_info['market_info'], height=100, disabled=True)
                                        if extracted_info.get('key_metrics'):
                                            st.text_area("Key Metrics", extracted_info['key_metrics'], height=100, disabled=True)
                                    
                                    if extracted_info.get('company_overview'):
                                        st.text_area("Company Overview", extracted_info['company_overview'], height=150, disabled=True)
                                    
                                    if extracted_info.get('team_background'):
                                        st.text_area("Team Background", extracted_info['team_background'], height=100, disabled=True)
                                    
                                    if extracted_info.get('additional_notes'):
                                        st.text_area("Additional Notes", extracted_info['additional_notes'], height=100, disabled=True)
                                
                                # Auto-populate form button
                                if st.button("✨ Auto-populate Form with Extracted Data", use_container_width=True, type="secondary"):
                                    # Create a combined data structure
                                    auto_data = {
                                        'company_name': extracted_info.get('company_name', ''),
                                        'company_overview': extracted_info.get('company_overview', ''),
                                        'team_background': extracted_info.get('team_background', ''),
                                        'stage': extracted_info.get('stage', 'Series A'),
                                        # You can add more mappings here
                                    }
                                    st.session_state.extracted_form_data = auto_data
                                    st.rerun()
                            else:
                                st.error("❌ Failed to extract company information from documents.")
        
        with upload_tab2:
            # Google Drive setup
            drive_service = None
            if st.button("🔗 Connect to Google Drive", use_container_width=True):
                with st.spinner("Connecting..."):
                    drive_service = setup_google_drive_api()
                    if drive_service:
                        st.session_state.drive_service = drive_service
                    else:
                        st.error("Failed to connect. Check credentials.")
            
            # Google Drive file input
            gdrive_input = st.text_area(
                "Google Drive File IDs or Links",
                placeholder="Enter file IDs or links, one per line",
                height=100
            )
            
            if gdrive_input and st.session_state.get('drive_service'):
                if st.button("📥 Download and Process Google Drive Files", use_container_width=True, type="primary"):
                    lines = gdrive_input.strip().split('\n')
                    file_ids = []
                    
                    # Extract file IDs from various formats
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        
                        # Extract file ID from different URL formats
                        if 'drive.google.com/file/d/' in line:
                            file_id = line.split('/file/d/')[1].split('/')[0]
                            file_ids.append(file_id)
                        elif 'docs.google.com/document/d/' in line:
                            file_id = line.split('/document/d/')[1].split('/')[0]
                            file_ids.append(file_id)
                        elif 'docs.google.com/spreadsheets/d/' in line:
                            file_id = line.split('/spreadsheets/d/')[1].split('/')[0]
                            file_ids.append(file_id)
                        else:
                            # Assume it's a direct file ID
                            file_ids.append(line)
                    
                    if file_ids:
                        all_gdrive_content = ""
                        
                        with st.spinner(f"Downloading {len(file_ids)} file(s) from Google Drive..."):
                            for i, file_id in enumerate(file_ids):
                                try:
                                    st.info(f"Downloading file {i+1}/{len(file_ids)}: {file_id}")
                                    
                                    # Download file content
                                    file_bytes = download_from_google_drive(file_id, st.session_state.drive_service)
                                    
                                    if file_bytes:
                                        # Try to determine file type and extract text
                                        # This is a simplified approach - in practice, you'd want to get the file metadata
                                        try:
                                            # Try as text first
                                            text_content = file_bytes.decode('utf-8')
                                            all_gdrive_content += f"\n\n=== Google Drive File {i+1} ===\n{text_content}"
                                            st.success(f"✅ Processed file {i+1}")
                                        except:
                                            # Try as PDF
                                            try:
                                                text_content = extract_text_from_pdf(file_bytes)
                                                if text_content:
                                                    all_gdrive_content += f"\n\n=== Google Drive File {i+1} ===\n{text_content}"
                                                    st.success(f"✅ Processed PDF file {i+1}")
                                                else:
                                                    st.warning(f"⚠️ Could not extract text from file {i+1}")
                                            except:
                                                st.error(f"❌ Unsupported file format for file {i+1}")
                                    else:
                                        st.error(f"❌ Failed to download file {i+1}")
                                        
                                except Exception as e:
                                    st.error(f"❌ Error processing file {i+1}: {e}")
                        
                        # Process extracted content
                        if all_gdrive_content:
                            with st.spinner("Analyzing Google Drive documents with AI..."):
                                extracted_info = extract_company_info_from_text(all_gdrive_content)
                                
                                if extracted_info:
                                    st.success("🎉 Successfully extracted information from Google Drive files!")
                                    st.session_state.extracted_data = extracted_info
                                    
                                    # Display extracted information (similar to local files)
                                    with st.expander("📋 Extracted Information from Google Drive", expanded=True):
                                        st.json(extracted_info)
                                else:
                                    st.error("❌ Failed to extract company information from Google Drive documents.")
                    else:
                        st.error("❌ No valid file IDs found. Please check your input.")
            
            elif gdrive_input and not st.session_state.get('drive_service'):
                st.warning("⚠️ Please connect to Google Drive first before processing files.")
        
        st.markdown("---")
        
        # Section 1: Company Idea, Market, How It Works
        st.markdown('<h2 class="section-header fade-in">Company Overview</h2>', unsafe_allow_html=True)
        
        # Use extracted data if available
        default_overview = st.session_state.get('extracted_form_data', {}).get('company_overview', 
                                                st.session_state.get('test_data', {}).get('company_overview', ''))
        
        company_overview = st.text_area("Company Idea, Market & How It Works", 
            value=default_overview,
            placeholder="Describe the company idea, target market, business model, and how the product/service works. Include the company name, what problem they solve, who their customers are, and how they make money.",
            height=150)

        # Section 2: Company Numbers (Structured Inputs)
        st.markdown('<h2 class="section-header fade-in">Financial & Company Metrics</h2>', unsafe_allow_html=True)
        
        # Two columns for better organization
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            
            # Helper function to get default values (extracted data > test data > empty)
            def get_default_value(field_name, test_field=None):
                if test_field is None:
                    test_field = field_name
                return (st.session_state.get('extracted_form_data', {}).get(field_name, '') or 
                       st.session_state.get('test_data', {}).get(test_field, ''))
            
            company_name = st.text_input("Company Name", 
                value=get_default_value('company_name'),
                placeholder="Enter company name")
            
            website = st.text_input("Website", 
                value=get_default_value('website'),
                placeholder="https://company.com")
            
            launch_year = st.text_input("Launch Year", 
                value=get_default_value('launch_year'),
                placeholder="2023")
            
            team_size = st.text_input("Team Size", 
                value=get_default_value('team_size'),
                placeholder="12")
            
            # Handle stage selection with extracted data
            extracted_stage = st.session_state.get('extracted_form_data', {}).get('stage', '')
            test_stage = st.session_state.get('test_data', {}).get('stage', '')
            default_stage = extracted_stage or test_stage or 'Series A'
            
            stage_options = ["Pre-seed", "Seed", "Series A", "Series B", "Series C", "Series D+"]
            stage_index = stage_options.index(default_stage) if default_stage in stage_options else 2
            
            stage = st.selectbox("Stage", 
                stage_options,
                index=stage_index)
            
            market_size = st.text_input("Market Size (TAM)", 
                value=get_default_value('market_size'),
                placeholder="$10B TAM")
            
            # Add TAM, SAM, SOM fields
            tam = st.text_input("TAM (Total Addressable Market)", 
                value=get_default_value('tam'),
                placeholder="$50B")
            
            sam = st.text_input("SAM (Serviceable Addressable Market)", 
                value=get_default_value('sam'),
                placeholder="$5B")
            
            som = st.text_input("SOM (Serviceable Obtainable Market)", 
                value=get_default_value('som'),
                placeholder="$500M")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            current_cash = st.text_input("Current Cash", 
                value=get_default_value('current_cash'),
                placeholder="$500k in cash")
            
            burn_rate = st.text_input("Monthly Burn Rate", 
                value=get_default_value('burn_rate'),
                placeholder="$50k/month")
            
            revenue = st.text_input("Revenue (ARR)", 
                value=get_default_value('revenue'),
                placeholder="$200k ARR")
            
            prev_raised = st.text_input("Previously Raised", 
                value=get_default_value('prev_raised'),
                placeholder="$2M Seed")
            
            round_size = st.text_input("Raising Round Size", 
                value=get_default_value('round_size'),
                placeholder="$5M Series A")
            
            post_money_valuation = st.text_input("Post-Money Valuation", 
                value=get_default_value('post_money_valuation'),
                placeholder="$25M")
            st.markdown('</div>', unsafe_allow_html=True)
        
        use_of_capital = st.text_area("Use of Capital", 
            value=get_default_value('use_of_capital'),
            placeholder="What will they use the funding for?",
            height=80)

        # Section 3: Founder and Team Information
        st.markdown('<h2 class="section-header fade-in">Founding Team & Background</h2>', unsafe_allow_html=True)
        
        team_background = st.text_area("Founding Team & Background", 
            value=get_default_value('team_background'),
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
                                "tam": tam or categorized_data.get("tam", ""),
                                "sam": sam or categorized_data.get("sam", ""),
                                "som": som or categorized_data.get("som", ""),
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
                            
                            # Stage 1: Generate initial memo
                            try:
                                client = openai.OpenAI(api_key=openai.api_key)
                                response = client.chat.completions.create(
                                    model="gpt-4",
                                    messages=[{"role": "user", "content": final_prompt}],
                                    temperature=0.7,
                                    max_tokens=2000
                                )
                                initial_memo = response.choices[0].message.content
                                
                                # Stage 2: VC Critical Review
                                vc_review_prompt = f"""
                                Answer the following question based solely on the provided context. If the context is insufficient, say 'I don't know.' Do not make up facts.

                                Now overlook this memo with a critical eye. You are a venture capitalist, and your savings are being invested into this endeavor, you only want to put your money into the best ideas. However, you want to cast a wide net, because if you invest in even one idea that becomes big, you've struck gold.

                                Here is the investment memo to review:

                                {initial_memo}

                                Please provide a comprehensive VC analysis that includes:
                                1. **Investment Thesis**: Why this could be a winning investment
                                2. **Key Strengths**: What makes this company compelling
                                3. **Major Risks**: What could go wrong
                                4. **Market Opportunity**: Assessment of the market size and timing
                                5. **Team Assessment**: Evaluation of the founding team
                                6. **Competitive Analysis**: How they stack up against competitors
                                7. **Financial Health**: Assessment of current financials and runway
                                8. **Investment Recommendation**: Pass, Consider, or Invest with reasoning
                                9. **Due Diligence Items**: What you'd want to investigate further
                                10. **Exit Potential**: Realistic exit scenarios and timelines

                                Format this as a professional VC analysis report with clear sections and actionable insights.
                                Base all analysis solely on the information provided in the memo. If any information is missing or unclear, explicitly state what additional information would be needed for a complete assessment.
                                """
                                
                                vc_response = client.chat.completions.create(
                                    model="gpt-4",
                                    messages=[{"role": "user", "content": vc_review_prompt}],
                                    temperature=0.6,
                                    max_tokens=2500
                                )
                                vc_analysis = vc_response.choices[0].message.content
                                
                                # Combine the memo and VC analysis
                                final_memo = f"""
                                # Investment Memo
                                
                                {initial_memo}
                                
                                ---
                                
                                # Venture Capital Analysis
                                
                                {vc_analysis}
                                """
                                st.markdown("---")
                                st.markdown("## Generated Investment Memo & VC Analysis")
                                
                                # Display memo with proper styling
                                st.markdown(f"""
                                <div class="memo-container">
                                    {final_memo}
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Market Size Hierarchy Visualization
                                st.markdown("---")
                                st.markdown("## Market Size Hierarchy")
                                
                                # Create and display the TAM > SAM > SOM visualization
                                market_hierarchy_fig = create_market_size_hierarchy(tam, sam, som, company_name)
                                if market_hierarchy_fig:
                                    st.plotly_chart(market_hierarchy_fig, use_container_width=True)
                                    
                                    # Add explanation
                                    st.markdown("""
                                    **Market Size Definitions:**
                                    - **TAM (Total Addressable Market):** The total market demand for a product or service
                                    - **SAM (Serviceable Addressable Market):** The portion of TAM that your product can realistically serve
                                    - **SOM (Serviceable Obtainable Market):** The portion of SAM that you can realistically capture in 3-5 years
                                    """)
                                else:
                                    pass
                                
                                # Investment Stage Analysis
                                st.markdown("---")
                                st.markdown("## Investment Stage Analysis")
                                
                                # Create and display the investment stage visualization
                                stage_analysis_fig = create_investment_stage_visualization(
                                    stage, company_name, revenue, burn_rate, team_size, prev_raised, round_size
                                )
                                if stage_analysis_fig:
                                    st.plotly_chart(stage_analysis_fig, use_container_width=True)
                                    
                                    # Add stage-specific insights
                                    stage_insights = {
                                        "Pre-seed": "**Pre-seed Stage:** Focus on idea validation and MVP development. Key metrics: product-market fit signals, early user feedback, technical feasibility.",
                                        "Seed": "**Seed Stage:** Building product-market fit and acquiring early customers. Key metrics: customer acquisition cost, retention rates, revenue growth.",
                                        "Series A": "**Series A Stage:** Scaling operations and expanding market reach. Key metrics: unit economics, market penetration, team scaling.",
                                        "Series B": "**Series B Stage:** Rapid growth and market leadership. Key metrics: market share, competitive positioning, operational efficiency.",
                                        "Series C": "**Series C Stage:** Market dominance and IPO preparation. Key metrics: market leadership, profitability, international expansion.",
                                        "Series D+": "**Series D+ Stage:** Late-stage growth and exit preparation. Key metrics: exit readiness, market consolidation, strategic partnerships."
                                    }
                                    
                                    current_stage = stage or "Series A"
                                    insight = stage_insights.get(current_stage, stage_insights["Series A"])
                                    st.info(insight)
                                else:
                                    pass
                                
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
                                                    # Clean the text and extract number
                                                    penetration_text = penetration_text.replace('%', '').replace(',', '').strip()
                                                    try:
                                                        penetration = float(penetration_text)
                                                    except:
                                                        penetration = 0.0
                                                else:
                                                    penetration = float(penetration_text)
                                                
                                                # Ensure penetration is reasonable
                                                penetration = max(0, min(100, penetration))
                                                
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
                                            except Exception as e:
                                                st.error(f"Error creating market penetration visualization: {e}")
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
                                
                                # Download buttons
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.download_button(
                                        label="Download Memo as Markdown",
                                        data=final_memo,
                                        file_name=f"{company_name}_investment_memo.md",
                                        mime="text/markdown",
                                        use_container_width=True
                                    )
                                
                                with col2:
                                    # Generate PDF
                                    pdf_bytes = convert_memo_to_pdf(final_memo, company_name)
                                    if pdf_bytes:
                                        st.download_button(
                                            label="Download Memo as PDF",
                                            data=pdf_bytes,
                                            file_name=f"{company_name}_investment_memo.pdf",
                                            mime="application/pdf",
                                            use_container_width=True
                                        )
                                    else:
                                        st.info("PDF download requires additional libraries. Install with: pip install weasyprint")
                                
                                # Alternative PDF generation method
                                st.markdown("---")
                                st.markdown("### Alternative PDF Generation")
                                st.markdown("""
                                If the PDF download doesn't work, you can:
                                1. **Copy the memo text** from above
                                2. **Paste into a word processor** (Google Docs, Microsoft Word, etc.)
                                3. **Export as PDF** from there
                                4. **Or use online converters** like markdown-to-pdf.com
                                """)
                                
                            except Exception as e:
                                st.error(f"Error generating memo: {e}")
                        else:
                            st.error("Failed to categorize company data. Please try again.") 