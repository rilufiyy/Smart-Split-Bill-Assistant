
def get_css(theme: str) -> str:
    """Get the CSS based on the selected theme.
    
    Args:
        theme (str): 'light' or 'dark'
        
    Returns:
        str: CSS string
    """
    
    # Color Palettes
    if theme == 'dark':
        bg_color = "#0e1117"
        text_color = "#fafafa"
        secondary_bg = "#262730"
        card_bg = "rgba(255, 255, 255, 0.05)"
        accent_color = "#FF4B4B"
        gradient_start = "#2e004a"
        gradient_end = "#660066"
        button_text = "#ffffff"
        border_color = "rgba(255, 255, 255, 0.6)" # Increased contrast
    else:
        bg_color = "#ffffff"
        text_color = "#000000"
        secondary_bg = "#f0f2f6"
        card_bg = "rgba(0, 0, 0, 0.02)"
        accent_color = "#FF4B4B"
        gradient_start = "#e0c3fc"
        gradient_end = "#8ec5fc"
        button_text = "#000000"
        border_color = "rgba(0, 0, 0, 0.1)"

    css = f"""
    <style>
    /* Global Settings */
    [data-testid="stAppViewContainer"] {{
        background-color: {bg_color};
        color: {text_color};
    }}
    
    [data-testid="stSidebar"] {{
        background-color: {secondary_bg};
    }}
    
    [data-testid="stHeader"] {{
        background-color: transparent;
    }}

    /* Typography */
    h1, h2, h3, h4, h5, h6 {{
        color: {text_color} !important;
        font-family: 'Inter', sans-serif;
    }}
    
    p, div, label, span {{
        color: {text_color};
        font-family: 'Inter', sans-serif;
    }}

    /* Buttons */
    .stButton > button {{
        background: linear-gradient(90deg, {gradient_start} 0%, {gradient_end} 100%);
        color: {button_text};
        border: none;
        border-radius: 12px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
    }}
    
    .stButton > button:active {{
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }}
    
    /* Tertiary Buttons (Ghost) */
    button[kind="tertiary"] {{
        background-color: transparent !important;
        border: 1px solid {border_color} !important;
        color: {text_color} !important;
        box_shadow: none !important;
    }}
    
    /* Ensure icon buttons are visible */
    button[kind="tertiary"] p {{
        color: {text_color} !important;
        fill: {text_color} !important;
    }}
    
    /* File Uploader Button Override */
    [data-testid="stFileUploader"] button {{
        background: {secondary_bg} !important;
        color: {text_color} !important;
        border: 1px solid {border_color} !important;
    }}

    /* Cards / Containers */
    [data-testid="stVerticalBlock"] > div > div {{
        /* This targets containers vaguely, Streamlit DOM is tricky */
    }}
    
    .element-container {{
        /* Generic element container */
    }}
    
    /* Custom Card Style Class (to be used with st.markdown) */
    .premium-card {{
        background-color: {card_bg};
        border-radius: 16px;
        padding: 20px;
        border: 1px solid {border_color};
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }}

    /* Inputs */
    .stTextInput > div > div > input {{
        background-color: {secondary_bg};
        color: {text_color};
        border-radius: 8px;
        border: 1px solid {border_color};
    }}
    
    /* Tables */
    [data-testid="stDataFrame"] {{
        border: 1px solid {border_color};
        border-radius: 10px;
        overflow: hidden;
    }}
    
    /* Modals / Dialogs */
    div[role="dialog"] {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
    }}
    
    div[role="dialog"] h1, div[role="dialog"] h2, div[role="dialog"] h3, div[role="dialog"] h4, div[role="dialog"] h5, div[role="dialog"] h6, div[role="dialog"] p, div[role="dialog"] label, div[role="dialog"] span {{
        color: {text_color} !important;
    }}
    
    /* Close button in modal */
    div[role="dialog"] button[kind="secondary"] {{
        color: {text_color} !important;
    }}
    
    /* Selectbox / Dropdown overrides */
    /* Selectbox / Dropdown overrides */
    div[data-baseweb="select"] > div {{
        background-color: {secondary_bg} !important;
        color: {text_color} !important;
        border-color: {border_color} !important;
    }}
    
    /* Target the text content specifically */
    div[data-baseweb="select"] div, 
    div[data-baseweb="select"] span, 
    div[data-baseweb="select"] li {{
        color: {text_color} !important;
    }}
    
    /* Dropdown alignment and background */
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul[data-baseweb="menu"], ul[role="listbox"] {{
        background-color: {bg_color} !important;
        border: 1px solid {border_color} !important;
    }}
    
    /* Options in the dropdown */
    li[data-baseweb="option"], li[role="option"] {{
         color: {text_color} !important;
         background-color: {bg_color} !important;
    }}
    
    /* Text inside options */
    li[data-baseweb="option"] *, li[role="option"] * {{
        color: {text_color} !important;
    }}
    
    /* Highlighted option */
    li[data-baseweb="option"]:hover, li[aria-selected="true"], li[role="option"][aria-selected="true"] {{
        background-color: {secondary_bg} !important;
    }}
    
    </style>
    """
    return css
