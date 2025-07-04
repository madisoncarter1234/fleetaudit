import streamlit as st

st.set_page_config(
    page_title="FleetAudit.io - Fleet Fraud Detection",
    page_icon="🚛",
    layout="wide", 
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    /* Obliterate sidebar */
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
        width: 0 !important;
        visibility: hidden !important;
    }

    /* Remove left margin */
    .css-1d391kg {
        margin-left: 0 !important;
    }

    /* Remove Streamlit's auto padding */
    section.main > div:first-child {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

import pandas as pd
import json
from datetime import datetime, timedelta
import random

# Check Streamlit version for multipage compatibility
try:
    import streamlit as st
    st_version = st.__version__
    major, minor = map(int, st_version.split('.')[:2])
    if major < 1 or (major == 1 and minor < 10):
        st.error(f"⚠️ Streamlit {st_version} detected. Multipage requires 1.10+")
except:
    pass

# Science.io-inspired CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .main {
        background: linear-gradient(to bottom, #f9fafb, #ffffff);
        padding: 0;
        max-width: none;
    }
    
    
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }
    
    /* Section padding for scroll offset */
    .scroll-section {
        scroll-margin-top: 80px;
        padding-top: 2rem;
    }
    
    /* JavaScript for smooth scrolling */
</style>
<script>
    // Enhanced smooth scrolling with easing
    function smoothScrollTo(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            const yOffset = -80; // Offset for fixed navbar
            const y = element.getBoundingClientRect().top + window.pageYOffset + yOffset;
            
            window.scrollTo({
                top: y,
                behavior: 'smooth'
            });
        }
    }
    
    // Wait for Streamlit to load
    setTimeout(function() {
        // Override anchor link clicks
        const links = document.querySelectorAll('a[href^="#"]');
        links.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const targetId = this.getAttribute('href').substring(1);
                smoothScrollTo(targetId);
            });
        });
    }, 100);
</script>
<style>
    
    /* Content container */
    .content-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem;
    }
    
    /* Hero section - Enhanced design */
    .hero-section {
        text-align: center;
        padding: 6rem 3rem;
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #f0f9ff 100%);
        border-radius: 1.5rem;
        margin: 2rem auto 4rem;
        max-width: 900px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 40px rgba(37, 99, 235, 0.08);
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(37, 99, 235, 0.03) 0%, transparent 70%);
        animation: pulse 15s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(0.8); opacity: 0.5; }
        50% { transform: scale(1.2); opacity: 0.8; }
    }
    
    .hero-section h1 {
        color: #111827 !important;
        font-size: 3.75rem !important;
        font-weight: 800 !important;
        margin-bottom: 1.5rem !important;
        line-height: 1.1 !important;
        letter-spacing: -0.02em;
        position: relative;
        z-index: 1;
    }
    
    .hero-section h2 {
        color: #4b5563 !important;
        font-size: 1.375rem !important;
        font-weight: 400 !important;
        margin-bottom: 2.5rem !important;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.6 !important;
        position: relative;
        z-index: 1;
    }
    
    .hero-cta {
        background: #2563eb;
        color: white;
        padding: 1rem 2rem;
        border-radius: 0.75rem;
        border: none;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-block;
        text-decoration: none;
        margin-top: 1rem;
    }
    
    .hero-cta:hover {
        background: #1d4ed8;
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.3);
    }
    
    /* Feature cards - Clean minimal style */
    .features-section {
        margin-bottom: 5rem;
    }
    
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin-top: 2rem;
    }
    
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 1rem;
        border: 1px solid #e5e7eb;
        transition: all 0.3s ease;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    .feature-card:hover {
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    .feature-card h3 {
        color: #111827 !important;
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
    }
    
    .feature-card p {
        color: #6b7280 !important;
        line-height: 1.6 !important;
    }
    
    /* Demo section */
    .demo-section {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 1rem;
        padding: 3rem;
        margin: 3rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    .demo-header h2 {
        color: #111827 !important;
        font-size: 2rem !important;
        font-weight: 600 !important;
        text-align: center;
        margin-bottom: 1rem !important;
    }
    
    /* Pricing */
    .pricing-section {
        text-align: center;
        margin: 4rem 0;
    }
    
    .pricing-card {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 1rem;
        padding: 2rem;
        max-width: 400px;
        margin: 0 auto;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    .price {
        font-size: 3rem;
        font-weight: 700;
        color: #111827;
        margin: 1rem 0;
    }
    
    /* Section headings */
    .section-heading {
        color: #111827 !important;
        font-size: 2.25rem !important;
        font-weight: 600 !important;
        text-align: center;
        margin-bottom: 3rem !important;
    }
    
    /* Hide Streamlit elements */
    .stDeployButton {display: none;}
    footer {visibility: hidden;}
    .stMainBlockContainer {padding-top: 0;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    .stSidebar {display: none;}
    section[data-testid="stSidebar"] {display: none;}
    
    /* Navigation button styling */
    div[data-testid="column"]:nth-child(2) .stButton > button,
    div[data-testid="column"]:nth-child(3) .stButton > button,
    div[data-testid="column"]:nth-child(4) .stButton > button {
        background: transparent !important;
        color: #6b7280 !important;
        border: none !important;
        border-radius: 0.375rem !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        font-size: 0.9rem !important;
    }
    
    div[data-testid="column"]:nth-child(2) .stButton > button:hover,
    div[data-testid="column"]:nth-child(3) .stButton > button:hover,
    div[data-testid="column"]:nth-child(4) .stButton > button:hover {
        background: #f3f4f6 !important;
        color: #2563eb !important;
        transform: none !important;
    }
    
    /* Primary CTA button styling */
    div[data-testid="column"]:nth-child(5) .stButton > button {
        background: #2563eb !important;
        color: white !important;
        border: none !important;
        border-radius: 0.5rem !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="column"]:nth-child(5) .stButton > button:hover {
        background: #1d4ed8 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
    }
    
    /* Regular button styling for other buttons */
    .stButton > button {
        background: #2563eb !important;
        color: white !important;
        border: none !important;
        border-radius: 0.5rem !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        position: static !important;
    }
    
    .stButton > button:hover {
        background: #1d4ed8 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
    }
    
    /* Force all buttons to stay in normal flow */
    .stButton {
        position: static !important;
    }
</style>
""", unsafe_allow_html=True)

def get_demo_data():
    """Generate realistic demo data for the fleet audit"""
    
    # Sample scenarios
    scenarios = {
        "ABC Logistics": {
            "description": "12-vehicle delivery fleet with multiple policy violations",
            "vehicles": 12,
            "violations": [
                {
                    "type": "shared_card_use",
                    "card_last_4": "4455",
                    "vehicles_involved": ["VAN-003", "TRUCK-007"],
                    "drivers_involved": ["Mike Chen", "Sarah Wilson"],
                    "time_span_minutes": 25,
                    "description": "Same fuel card (****4455) used by different drivers within 25 minutes",
                    "severity": "high",
                    "estimated_loss": 187.50
                },
                {
                    "type": "after_hours",
                    "vehicle_id": "VAN-005",
                    "driver_name": "Carlos Rodriguez", 
                    "timestamp": "2024-08-15 02:47:00",
                    "location": "Shell Station - Interstate 85",
                    "card_last_4": "4455",
                    "description": "Fuel purchase at 2:47 AM on weekend outside business hours",
                    "severity": "high",
                    "estimated_loss": 89.25
                },
                {
                    "type": "excessive_amount",
                    "vehicle_id": "TRUCK-003",
                    "driver_name": "David Kim",
                    "timestamp": "2024-08-12 14:22:00", 
                    "location": "BP Station - Highway 75",
                    "card_last_4": "7891",
                    "description": "Purchased 67 gallons (normal capacity: 35 gallons)",
                    "severity": "medium",
                    "estimated_loss": 125.00
                },
                {
                    "type": "ghost_job",
                    "job_id": "ATL-2024-0815",
                    "driver_name": "Mike Chen",
                    "vehicle_id": "VAN-003",
                    "scheduled_time": "2024-08-15 14:00:00",
                    "address": "Buford, GA",
                    "description": "Scheduled delivery with no GPS activity at job location",
                    "severity": "high", 
                    "estimated_loss": 150.00
                }
            ],
            "summary": {
                "total_violations": 4,
                "total_estimated_loss": 551.75,
                "high_risk_vehicles": ["VAN-003", "VAN-005", "TRUCK-003"]
            }
        },
        "Metro Delivery": {
            "description": "6-vehicle urban delivery service with moderate violations",
            "vehicles": 6,
            "violations": [
                {
                    "type": "rapid_purchases",
                    "vehicle_id": "VAN-002",
                    "driver_name": "Lisa Johnson",
                    "timestamp": "2024-08-10 16:45:00",
                    "location": "Exxon Station - Downtown",
                    "card_last_4": "3344", 
                    "description": "Two fuel purchases within 45 minutes at different locations",
                    "severity": "medium",
                    "estimated_loss": 95.50
                },
                {
                    "type": "personal_use",
                    "vehicle_id": "TRUCK-001", 
                    "driver_name": "James Wilson",
                    "timestamp": "2024-08-11 19:30:00",
                    "location": "Shell Station - Residential Area",
                    "card_last_4": "2233",
                    "description": "Weekend fuel purchase in residential area during off-hours",
                    "severity": "medium",
                    "estimated_loss": 67.25
                }
            ],
            "summary": {
                "total_violations": 2,
                "total_estimated_loss": 162.75,
                "high_risk_vehicles": ["VAN-002", "TRUCK-001"]
            }
        },
        "Clean Fleet Co": {
            "description": "8-vehicle service fleet with excellent compliance record",
            "vehicles": 8,
            "violations": [
                {
                    "type": "minor_deviation",
                    "vehicle_id": "VAN-001",
                    "driver_name": "Jennifer Adams",
                    "timestamp": "2024-08-09 18:15:00",
                    "location": "BP Station - Route 285",
                    "card_last_4": "5566",
                    "description": "Fuel purchase 15 minutes after official end of shift",
                    "severity": "low",
                    "estimated_loss": 12.50
                }
            ],
            "summary": {
                "total_violations": 1,
                "total_estimated_loss": 12.50,
                "high_risk_vehicles": []
            }
        }
    }
    
    return scenarios

def display_demo_results(scenario_name, scenario_data):
    """Display demo results that look like real fraud detection output"""
    
    violations = scenario_data["violations"]
    summary = scenario_data["summary"]
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🚨 Violations Found", len(violations), delta=f"{len(violations)} issues")
    with col2:
        total_loss = summary.get('total_estimated_loss', 0)
        st.metric("💰 Estimated Loss", f"${total_loss:.2f}", delta=f"-${total_loss:.2f}")
    with col3:
        high_risk = len([v for v in violations if v.get('severity') == 'high'])
        st.metric("⚠️ High Risk", high_risk, delta=f"{high_risk} critical")
    
    st.markdown("---")
    
    # Display violations
    for violation in violations:
        if violation.get('type') == 'shared_card_use':
            card_info = f"Card ****{violation.get('card_last_4', 'Unknown')}"
            vehicles = ', '.join(violation.get('vehicles_involved', []))
            with st.expander(f"**Shared Card Use** - {card_info} ({vehicles})"):
                st.write(f"**Card Last 4:** ****{violation.get('card_last_4', 'Unknown')}")
                st.write(f"**Vehicles Involved:** {', '.join(violation.get('vehicles_involved', []))}")
                st.write(f"**Drivers Involved:** {', '.join(violation.get('drivers_involved', []))}")
                st.write(f"**Time Span:** {violation.get('time_span_minutes', 'Unknown')} minutes")
                st.write(f"**Description:** {violation.get('description', 'No description')}")
                st.write(f"**Severity:** {violation.get('severity', 'Unknown').upper()}")
                if violation.get('estimated_loss'):
                    st.write(f"**Estimated Loss:** ${violation['estimated_loss']:.2f}")
        else:
            # Handle regular violations
            driver_info = f"{violation.get('driver_name', 'Unknown Driver')} ({violation.get('vehicle_id', 'Unknown Vehicle')})"
            violation_title = violation.get('type', 'Unknown').replace('_', ' ').title()
            with st.expander(f"**{violation_title}** - {driver_info}"):
                st.write(f"**Driver:** {violation.get('driver_name', 'Unknown')}")
                st.write(f"**Vehicle:** {violation.get('vehicle_id', 'Unknown')}")
                st.write(f"**Time:** {violation.get('timestamp', 'Unknown')}")
                if violation.get('location'):
                    st.write(f"**Location:** {violation.get('location', 'Unknown')}")
                if violation.get('address'):
                    st.write(f"**Job Address:** {violation.get('address', 'Unknown')}")
                if violation.get('card_last_4'):
                    st.write(f"**Card Used:** ****{violation['card_last_4']}")
                st.write(f"**Description:** {violation.get('description', 'No description')}")
                st.write(f"**Severity:** {violation.get('severity', 'Unknown').upper()}")
                if violation.get('estimated_loss'):
                    st.write(f"**Estimated Loss:** ${violation['estimated_loss']:.2f}")

def init_global_session_state():
    """Initialize session state variables that should persist across all pages"""
    if 'navigation_initialized' not in st.session_state:
        st.session_state.navigation_initialized = True
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'landing'

def navbar():
    st.markdown("##", unsafe_allow_html=True)  # spacer
    cols = st.columns([1, 4, 1, 1, 1, 1])  # Added space for CTA

    with cols[0]:
        st.markdown("### 🚚 FleetAudit", unsafe_allow_html=True)
    with cols[1]:
        pass
    with cols[2]:
        if st.button("Features"):
            st.session_state.scroll_to = "features"
    with cols[3]:
        if st.button("Demo"):
            st.session_state.scroll_to = "demo"
    with cols[4]:
        if st.button("Pricing"):
            st.session_state.scroll_to = "pricing"
    with cols[5]:
        st.markdown(
            """
            <style>
            .blue-button > button {
                background-color: #2563eb;
                color: white;
                font-weight: 600;
                border-radius: 6px;
                padding: 0.5rem 1.25rem;
            }
            .blue-button > button:hover {
                background-color: #1d4ed8;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        with st.container():
            cta = st.container()
            with cta:
                if st.button("Try FleetAudit", key="cta"):
                    st.switch_page("pages/1_Product.py")
        st.markdown('<div class="blue-button"></div>', unsafe_allow_html=True)

def main():
    # Initialize session state first
    init_global_session_state()
    
    # Call the navbar function
    navbar()
    
    # Handle scrolling if navigation was clicked
    if st.session_state.get('scroll_to'):
        target = st.session_state.scroll_to
        st.markdown(f"""
        <script>
            setTimeout(function() {{
                const element = document.getElementById('{target}');
                if (element) {{
                    element.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                }}
            }}, 100);
        </script>
        """, unsafe_allow_html=True)
        # Clear the scroll target
        del st.session_state.scroll_to
    
    st.markdown("---")
    
    # Hero Section - Science.io style
    st.markdown("""
    <div class="content-container">
        <div class="hero-section">
            <h1>Stop Fleet Fraud Before It Costs You Thousands</h1>
            <h2>AI-powered fraud detection that analyzes your fuel, GPS, and job data to uncover theft, misuse, and policy violations in minutes.</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA Button with navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Try FleetAudit Free", type="primary", use_container_width=True, key="hero_cta"):
            st.switch_page("pages/1_Product.py")
    
    # Features Section with Science.io styling
    st.markdown("""
    <div class="content-container">
        <div class="features-section scroll-section" id="features">
            <h2 class="section-heading">Why FleetAudit.io?</h2>
            <div class="features-grid">
                <div class="feature-card">
                    <h3>🔍 AI-Powered Detection</h3>
                    <p>Advanced algorithms detect fraud patterns humans miss - shared cards, ghost jobs, after-hours abuse, and more.</p>
                </div>
                <div class="feature-card">
                    <h3>💰 Immediate ROI</h3>
                    <p>Customers typically recover 10x their subscription cost in the first month by stopping ongoing fraud.</p>
                </div>
                <div class="feature-card">
                    <h3>📊 Professional Reports</h3>
                    <p>Generate detailed PDF reports with evidence for HR, management, and legal proceedings.</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Demo Section with new styling
    st.markdown("""
    <div class="content-container">
        <div class="demo-section scroll-section" id="demo">
            <div class="demo-header">
                <h2>🎯 See FleetAudit.io in Action</h2>
                <p style="color: #6b7280; font-size: 1.1rem; margin-bottom: 2rem; text-align: center;">Select a sample fleet below to see how our AI detects fraud and policy violations:</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Demo selector
    demo_data = get_demo_data()
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        scenario_names = list(demo_data.keys())
        selected_scenario = st.selectbox(
            "Choose Sample Fleet:",
            scenario_names,
            help="Select different fleet examples to see various types of fraud detection"
        )
        
        scenario_info = demo_data[selected_scenario]
        st.info(f"**{selected_scenario}**\n\n{scenario_info['description']}")
        
        if st.button("🔍 Run Fraud Analysis", type="primary", use_container_width=True):
            st.session_state.show_demo = True
    
    with col2:
        if st.session_state.get('show_demo', False):
            st.markdown(f"### 🚨 Fraud Detection Results: {selected_scenario}")
            display_demo_results(selected_scenario, demo_data[selected_scenario])
    
    # Pricing Section with Science.io styling
    st.markdown("""
    <div class="content-container">
        <div class="pricing-section scroll-section" id="pricing">
            <h2 class="section-heading">💳 Simple, Transparent Pricing</h2>
            <div class="pricing-card">
                <h3 style="color: #111827; font-size: 1.5rem; margin-bottom: 1rem;">Professional Plan</h3>
                <div class="price">$99<span style="font-size: 1rem; color: #6b7280; font-weight: 400;">/month</span></div>
                <div style="text-align: left; color: #374151; line-height: 1.8;">
                    ✅ Unlimited fleet data analysis<br>
                    ✅ All fraud detection features<br>
                    ✅ PDF report generation<br>
                    ✅ Email alerts & notifications<br>
                    ✅ Priority support
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Start trial button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Start Free Trial", type="primary", use_container_width=True):
            st.balloons()
            st.success("🎉 Ready to start your free trial! Subscription system coming soon.")
    
    # Call to Action with Science.io styling
    st.markdown("""
    <div class="content-container">
        <div style="text-align: center; padding: 4rem 2rem; background: #f9fafb; border-radius: 1rem; margin: 3rem 0;">
            <h2 style="color: #111827; font-size: 2rem; font-weight: 600; margin-bottom: 1rem;">Ready to Stop Fleet Fraud?</h2>
            <p style="color: #6b7280; font-size: 1.2rem; margin-bottom: 0;">Join hundreds of fleet managers who've recovered thousands in stolen fuel and time.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Clean Footer
    st.markdown("""
    <div class="content-container">
        <div style="border-top: 1px solid #e5e7eb; padding: 3rem 0; margin-top: 4rem;">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; color: #6b7280;">
                <div>
                    <h4 style="color: #111827; font-weight: 600; margin-bottom: 1rem;">FleetAudit.io</h4>
                    <p>AI-powered fleet fraud detection</p>
                </div>
                <div>
                    <h4 style="color: #111827; font-weight: 600; margin-bottom: 1rem;">Features</h4>
                    <p>• Shared card detection<br>• Ghost job analysis<br>• After-hours monitoring<br>• GPS cross-referencing</p>
                </div>
                <div>
                    <h4 style="color: #111827; font-weight: 600; margin-bottom: 1rem;">Support</h4>
                    <p>• 24/7 customer support<br>• Implementation assistance<br>• Training & onboarding</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()