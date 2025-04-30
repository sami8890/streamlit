import streamlit as st
import string
import random
import re
import pyperclip
from math import log2
import time

# Set page configuration with dark theme
st.set_page_config(
    page_title="SecurePass Generator",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS for dark theme and enhanced styling
st.markdown("""
<style>
    /* Dark theme base colors */
    :root {
        --background-color: #121212;
        --card-background: #1e1e1e;
        --input-background: #2d2d2d;
        --border-color: #333333;
        --text-color: #e0e0e0;
        --text-secondary: #a0a0a0;
        --primary-color: #4361ee;
        --primary-hover: #3a56d4;
        --success-color: #4CAF50;
        --warning-color: #FFC107;
        --danger-color: #FF5252;
        --info-color: #2196F3;
    }

    /* Override Streamlit's default white background */
    .main .block-container {
        background-color: var(--background-color);
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
        color: var(--text-color);
    }
    
    /* Make the main content area dark */
    .main {
        background-color: var(--background-color);
        color: var(--text-color);
    }
    
    /* Style for tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        border-radius: 8px;
        background-color: var(--card-background);
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 10px 16px;
        border-radius: 6px 6px 0 0;
        font-weight: 500;
        color: var(--text-color);
        background-color: var(--card-background);
    }
    
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: var(--primary-color);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: white;
    }
    
    /* Password meter styling */
    .password-meter {
        height: 10px;
        border-radius: 6px;
        margin-top: 5px;
        margin-bottom: 15px;
        transition: all 0.3s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.3);
    }
    
    /* Button styling */
    .copy-btn {
        border: none;
        background-color: var(--primary-color);
        color: white;
        padding: 10px 16px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 14px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 6px;
        transition: 0.3s;
        width: 100%;
    }
    
    .copy-btn:hover {
        background-color: var(--primary-hover);
    }
    
    .stButton>button {
        width: 100%;
        background-color: var(--primary-color);
        color: white;
        font-weight: 500;
        padding: 0.5em 1em;
        border-radius: 6px;
        border: none;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    
    .stButton>button:hover {
        background-color: var(--primary-hover);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    /* Password display styling */
    .password-display {
        padding: 16px;
        background-color: var(--input-background);
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        margin-bottom: 20px;
        border: 1px solid var(--border-color);
        font-size: 16px;
        letter-spacing: 1px;
        text-align: center;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        color: var(--text-color);
    }
    
    .password-display:hover {
        background-color: #353535;
    }
    
    /* Card styling */
    .feature-card {
        background-color: var(--card-background);
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        border: 1px solid var(--border-color);
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        transform: translateY(-2px);
    }
    
    /* Strength label styling */
    .strength-label {
        font-weight: bold;
        font-size: 1.2em;
        margin-bottom: 5px;
        color: var(--text-color);
    }
    
    /* Feedback items styling */
    .feedback-item {
        margin-bottom: 6px;
        padding: 8px 12px;
        border-radius: 6px;
        background-color: var(--card-background);
    }
    
    .feedback-item-positive {
        background-color: rgba(76, 175, 80, 0.2);
        border-left: 4px solid var(--success-color);
    }
    
    .feedback-item-warning {
        background-color: rgba(255, 193, 7, 0.2);
        border-left: 4px solid var(--warning-color);
    }
    
    .feedback-item-negative {
        background-color: rgba(255, 82, 82, 0.2);
        border-left: 4px solid var(--danger-color);
    }
    
    /* Headings styling */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-color);
    }
    
    h1 {
        margin-bottom: 1.5rem;
    }
    
    h2, h3 {
        margin-top: 1.5rem;
    }
    
    hr {
        margin: 2rem 0;
        border-color: var(--border-color);
    }
    
    /* Slider styling */
    .stSlider>div>div>div {
        background-color: var(--primary-color);
    }
    
    /* Input fields styling */
    .stTextInput>div>div>input {
        background-color: var(--input-background);
        color: var(--text-color);
        border-color: var(--border-color);
    }
    
    /* Checkbox styling */
    .stCheckbox>div>div>label {
        color: var(--text-color);
    }
    
    /* Code blocks styling */
    .stCodeBlock {
        background-color: var(--input-background);
        border-color: var(--border-color);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: var(--card-background);
        color: var(--text-color);
        border-color: var(--border-color);
    }
    
    .streamlit-expanderContent {
        background-color: var(--card-background);
        color: var(--text-color);
        border-color: var(--border-color);
    }
    
    /* Success message styling */
    .element-container .stAlert {
        background-color: rgba(76, 175, 80, 0.2);
        color: var(--text-color);
    }
    
    /* Remove white background from all containers */
    div.css-1r6slb0.e1tzin5v2 {
        background-color: var(--background-color);
        border: 1px solid var(--border-color);
        padding: 5px;
        border-radius: 5px;
    }
    
    div.css-keje6w.e1tzin5v2 {
        background-color: var(--background-color);
        border: 1px solid var(--border-color);
        padding: 5px;
        border-radius: 5px;
    }
    
    div.stTabs [data-baseweb="tab-panel"] {
        background-color: var(--background-color);
    }
    
    /* Style for the spinner */
    div.stSpinner > div {
        border-top-color: var(--primary-color) !important;
    }
    
    /* Style for selectbox */
    div.stSelectbox > div {
        background-color: var(--input-background);
        color: var(--text-color);
    }
    
    /* Style for multiselect */
    div.stMultiSelect > div {
        background-color: var(--input-background);
        color: var(--text-color);
    }
    
    /* Style for dataframe */
    .dataframe {
        background-color: var(--card-background);
        color: var(--text-color);
    }
    
    .dataframe th {
        background-color: var(--input-background);
        color: var(--text-color);
    }
    
    /* Override any remaining white backgrounds */
    .css-1kyxreq, .css-12oz5g7 {
        background-color: var(--background-color) !important;
        color: var(--text-color) !important;
    }
    
    /* Make sure text is visible */
    .css-1aehpvj, .css-1v3fvcr, .css-qrbaxs {
        color: var(--text-color) !important;
    }
    
    /* Fix for code display */
    code {
        background-color: var(--input-background);
        color: var(--text-color);
        padding: 0.2em 0.4em;
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)

# App header with animation
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1>🔒 SecurePass Generator</h1>
    <p style="font-size: 1.2rem; color: #a0a0a0; max-width: 600px; margin: 0 auto;">
        Create unbreakable passwords and analyze their strength against modern security standards
    </p>
</div>
""", unsafe_allow_html=True)

# Password strength calculation function
def calculate_password_strength(password):
    """Calculate password strength score from 0-100"""
    if not password:
        return 0, []
    
    strength = 0
    feedback = []
    
    # Length check
    if len(password) < 8:
        feedback.append(("❌ Password is too short (should be at least 8 characters)", "negative"))
        length_score = len(password) * 2.5  # Max 20 points for length
    elif len(password) < 12:
        feedback.append(("⚠️ Good length, but 12+ characters is recommended", "warning"))
        length_score = 20 + (len(password) - 8) * 2.5  # Max 30 points for length
    else:
        feedback.append(("✅ Excellent length", "positive"))
        length_score = min(40, 20 + (len(password) - 8) * 2)  # Max 40 points for length
    
    strength += length_score
    
    # Character variety checks
    has_lowercase = bool(re.search(r'[a-z]', password))
    has_uppercase = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[^a-zA-Z0-9\s]', password))
    
    variety_score = 0
    if has_lowercase:
        variety_score += 10
        feedback.append(("✅ Contains lowercase letters", "positive"))
    else:
        feedback.append(("❌ Missing lowercase letters", "negative"))
    
    if has_uppercase:
        variety_score += 10
        feedback.append(("✅ Contains uppercase letters", "positive"))
    else:
        feedback.append(("❌ Missing uppercase letters", "negative"))
    
    if has_digit:
        variety_score += 10
        feedback.append(("✅ Contains numbers", "positive"))
    else:
        feedback.append(("❌ Missing numbers", "negative"))
    
    if has_special:
        variety_score += 10
        feedback.append(("✅ Contains special characters", "positive"))
    else:
        feedback.append(("❌ Missing special characters", "negative"))
    
    strength += variety_score
    
    # Common patterns check
    common_patterns = [
        r'12345', r'qwerty', r'password', r'admin', r'welcome',
        r'123123', r'abcdef', r'abc123', r'111111', r'monkey'
    ]
    
    for pattern in common_patterns:
        if re.search(pattern, password.lower()):
            strength -= 15
            feedback.append((f"❌ Contains common pattern: '{pattern}'", "negative"))
            break
    
    # Repeating characters check
    if re.search(r'(.)\1{2,}', password):  # Same character 3+ times in a row
        strength -= 10
        feedback.append(("❌ Contains repeating characters", "negative"))
    
    # Sequential characters check
    sequential_patterns = [
        r'abcd', r'wxyz', r'1234', r'7890'
    ]
    
    for pattern in sequential_patterns:
        if re.search(pattern, password.lower()):
            strength -= 10
            feedback.append(("❌ Contains sequential characters", "negative"))
            break
    
    # Calculate entropy
    charset_size = 0
    if has_lowercase:
        charset_size += 26
    if has_uppercase:
        charset_size += 26
    if has_digit:
        charset_size += 10
    if has_special:
        charset_size += 33  # Approximation of special characters
    
    if charset_size > 0:
        entropy = log2(charset_size ** len(password))
        entropy_score = min(20, entropy / 5)  # Max 20 points for entropy
        strength += entropy_score
        
        if entropy > 60:
            feedback.append((f"✅ High entropy ({entropy:.1f} bits)", "positive"))
        elif entropy > 35:
            feedback.append((f"⚠️ Moderate entropy ({entropy:.1f} bits)", "warning"))
        else:
            feedback.append((f"❌ Low entropy ({entropy:.1f} bits)", "negative"))
    
    # Make sure strength is between 0 and 100
    strength = max(0, min(100, strength))
    
    # Add any positive feedback if the score is good
    if strength > 80 and not any(f[0].startswith("❌") for f in feedback):
        feedback.append(("✅ Excellent password strength overall", "positive"))
    
    return strength, feedback

# Generate a password
def generate_password(length=12, use_lowercase=True, use_uppercase=True, use_digits=True, use_special=True, avoid_ambiguous=False):
    """Generate a random password based on user preferences"""
    chars = ""
    
    if use_lowercase:
        chars += string.ascii_lowercase
    if use_uppercase:
        chars += string.ascii_uppercase
    if use_digits:
        chars += string.digits
    if use_special:
        chars += string.punctuation
    
    # Remove ambiguous characters if requested
    if avoid_ambiguous:
        for c in 'Il1O0':
            chars = chars.replace(c, '')
    
    if not chars:
        return "Please select at least one character type"
    
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

# Create two tabs with enhanced styling
tabs = st.tabs(["🏗️ Password Generator", "🔍 Password Strength Checker"])

# Password Generator Tab
with tabs[0]:
    st.markdown("""
    <h2 style="margin-top: 0;">Generate a Strong Password</h2>
    <p style="color: #a0a0a0;">Customize your password settings using the options below</p>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            password_length = st.slider(
                "Password Length", 
                min_value=8, 
                max_value=32, 
                value=16, 
                step=1,
                help="Longer passwords are generally more secure. 16+ characters is recommended."
            )
        
        with col2:
            avoid_ambiguous = st.checkbox(
                "Avoid Ambiguous Characters", 
                value=True,
                help="Exclude characters that can be confused with each other (I, l, 1, O, 0)"
            )
        
        st.markdown('<div style="margin-top: 15px;">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<strong>Include Characters:</strong>", unsafe_allow_html=True)
            use_lowercase = st.checkbox("Lowercase (a-z)", value=True)
            use_uppercase = st.checkbox("Uppercase (A-Z)", value=True)
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            use_digits = st.checkbox("Numbers (0-9)", value=True)
            use_special = st.checkbox("Special Characters (!@#$...)", value=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    generate_btn = st.button("🔄 Generate Secure Password", use_container_width=True)
    
    if generate_btn:
        with st.spinner("Generating secure password..."):
            time.sleep(0.5)  # Small delay for better UX
            generated_password = generate_password(
                length=password_length,
                use_lowercase=use_lowercase,
                use_uppercase=use_uppercase,
                use_digits=use_digits,
                use_special=use_special,
                avoid_ambiguous=avoid_ambiguous
            )
            
            st.session_state.current_password = generated_password
            strength, feedback = calculate_password_strength(generated_password)
            st.session_state.current_strength = strength
            st.session_state.current_feedback = feedback
    
    # Display password and strength if available
    if 'current_password' in st.session_state:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("<h3>Your Generated Password:</h3>", unsafe_allow_html=True)
        
        # Create a container with the password and copy button
        st.markdown(f"""
        <div class="password-display">{st.session_state.current_password}</div>
        """, unsafe_allow_html=True)
        
        if st.button("📋 Copy to Clipboard", key="copy_btn"):
            pyperclip.copy(st.session_state.current_password)
            st.success("Password copied to clipboard!")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Show strength meter
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("<h3>Password Strength Analysis:</h3>", unsafe_allow_html=True)
        strength = st.session_state.current_strength
        
        # Determine color based on strength
        if strength < 40:
            meter_color = "#FF5252"  # Red
            strength_text = "Weak"
            strength_emoji = "⚠️"
        elif strength < 70:
            meter_color = "#FFC107"  # Yellow/Orange
            strength_text = "Moderate"
            strength_emoji = "🔔"
        else:
            meter_color = "#4CAF50"  # Green
            strength_text = "Strong"
            strength_emoji = "✅"
        
        # Display the meter
        st.markdown(f"""
        <div class="strength-label">{strength_emoji} {strength_text} ({strength:.0f}/100)</div>
        <div style="width: 100%; background-color: #333333; border-radius: 6px; box-shadow: inset 0 1px 3px rgba(0,0,0,0.2);">
            <div class="password-meter" style="width: {strength}%; background-color: {meter_color};"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display feedback
        st.markdown("<h4>Detailed Analysis:</h4>", unsafe_allow_html=True)
        for item, item_type in st.session_state.current_feedback:
            st.markdown(f"""
            <div class="feedback-item feedback-item-{item_type}">
                {item}
            </div>
            """, unsafe_allow_html=True)
        
        # Time to crack estimate
        char_complexity = 0
        if use_lowercase: char_complexity += 26
        if use_uppercase: char_complexity += 26
        if use_digits: char_complexity += 10
        if use_special: char_complexity += 33
        
        if char_complexity > 0 and len(st.session_state.current_password) > 0:
            entropy = log2(char_complexity ** len(st.session_state.current_password))
            
            # Very rough estimate of time to crack
            if entropy < 28:
                crack_time = "Seconds to Minutes"
                crack_desc = "Extremely vulnerable"
            elif entropy < 36:
                crack_time = "Hours to Days"
                crack_desc = "Very weak"
            elif entropy < 60:
                crack_time = "Weeks to Months"
                crack_desc = "Moderate but vulnerable to targeted attacks"
            elif entropy < 80:
                crack_time = "Years"
                crack_desc = "Strong against most attacks"
            else:
                crack_time = "Centuries"
                crack_desc = "Virtually unbreakable with current technology"
            
            st.markdown(f"""
            <h4>Estimated Time to Crack:</h4>
            <div class="feedback-item">
                <strong>{crack_time}</strong> - {crack_desc}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Password Strength Checker Tab
with tabs[1]:
    st.markdown("""
    <h2 style="margin-top: 0;">Check Your Password Strength</h2>
    <p style="color: #a0a0a0;">Enter your existing password to evaluate its security level</p>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        password_to_check = st.text_input("Enter a password to check:", type="password")
        st.markdown("""
        <div style="font-size: 0.8rem; color: #a0a0a0; margin-top: -10px;">
            Your password is not stored or transmitted - analysis happens locally in your browser
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    if password_to_check:
        with st.spinner("Analyzing password strength..."):
            time.sleep(0.3)  # Small delay for better UX
            strength, feedback = calculate_password_strength(password_to_check)
        
        # Determine color based on strength
        if strength < 40:
            meter_color = "#FF5252"  # Red
            strength_text = "Weak"
            strength_emoji = "⚠️"
        elif strength < 70:
            meter_color = "#FFC107"  # Yellow/Orange
            strength_text = "Moderate"
            strength_emoji = "🔔"
        else:
            meter_color = "#4CAF50"  # Green
            strength_text = "Strong"
            strength_emoji = "✅"
        
        # Display the meter
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("<h3>Password Strength Analysis:</h3>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="strength-label">{strength_emoji} {strength_text} ({strength:.0f}/100)</div>
        <div style="width: 100%; background-color: #333333; border-radius: 6px; box-shadow: inset 0 1px 3px rgba(0,0,0,0.2);">
            <div class="password-meter" style="width: {strength}%; background-color: {meter_color};"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display feedback
        st.markdown("<h4>Detailed Analysis:</h4>", unsafe_allow_html=True)
        for item, item_type in feedback:
            st.markdown(f"""
            <div class="feedback-item feedback-item-{item_type}">
                {item}
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Security tips in a card
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("""
    <h3>Password Security Best Practices</h3>
    <ul style="padding-left: 20px; color: #e0e0e0;">
        <li><strong>Length Matters:</strong> Use at least 12 characters, preferably 16+</li>
        <li><strong>Mix It Up:</strong> Include uppercase, lowercase, numbers, and special characters</li>
        <li><strong>Avoid Personal Info:</strong> Don't use birthdates, names, or common words</li>
        <li><strong>Use Unique Passwords:</strong> Never reuse passwords across different sites</li>
        <li><strong>Password Manager:</strong> Consider using a reputable password manager</li>
        <li><strong>Enable 2FA:</strong> Where available, enable two-factor authentication</li>
        <li><strong>Regular Updates:</strong> Change sensitive passwords every 3-6 months</li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Password History (if in session state)
if 'password_history' not in st.session_state:
    st.session_state.password_history = []

# Add current password to history if it exists and is new
if 'current_password' in st.session_state and st.session_state.current_password not in st.session_state.password_history and tabs[0].selectbox:
    # Keep only the last 5 passwords
    if len(st.session_state.password_history) >= 5:
        st.session_state.password_history.pop(0)
    st.session_state.password_history.append(st.session_state.current_password)

# Show history in expandable section
if st.session_state.password_history:
    with st.expander("Password History (Last 5)"):
        for i, pwd in enumerate(reversed(st.session_state.password_history)):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.code(pwd, language=None)
            with col2:
                if st.button(f"Copy", key=f"hist_{i}"):
                    pyperclip.copy(pwd)
                    st.success("Copied!")

# Footer
st.markdown("""
<hr style="border-color: #333333;">
<div style="text-align: center; color: #a0a0a0; padding: 1rem 0;">
    <p>🔐 <strong>SecurePass Generator</strong> - Created with Streamlit</p>
    <p style="font-size: 0.8rem; margin-top: -10px;">For educational purposes only • Not storing any data</p>
</div>
""", unsafe_allow_html=True)