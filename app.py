import streamlit as st
import os
import base64
from gtts import gTTS
import io
from openai import OpenAI
from dotenv import load_dotenv
import textwrap

# Load environment variables
load_dotenv()

# Configure page settings
st.set_page_config(
    page_title="Jack and Jill's Alphabet Adventure",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"  # Start with sidebar expanded
)

# Define paths to content directories
STORIES_DIR = "alphabet_stories_new"
REALISTIC_IMAGES_DIR = "alphabet_images_new"
WATERCOLOR_IMAGES_DIR = "alphabet_images_new_illustrations"
AUDIO_DIR = "alphabet_audio_files"  # Base audio directory

# Voice directories
FEMALE1_AUDIO_DIR = os.path.join(AUDIO_DIR, "female1")
FEMALE2_AUDIO_DIR = os.path.join(AUDIO_DIR, "female2")
MALE1_AUDIO_DIR = os.path.join(AUDIO_DIR, "male1")
MALE2_AUDIO_DIR = os.path.join(AUDIO_DIR, "male2")

# OpenAI API key (for the chatbot)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Set default user state
if 'is_registered' not in st.session_state:
    st.session_state.is_registered = False

if 'has_purchased' not in st.session_state:
    st.session_state.has_purchased = False

# Set default voice options if not existing
if 'selected_voice' not in st.session_state:
    st.session_state.selected_voice = "Female 1"

# Function to read a story from file
def read_story(letter):
    story_path = os.path.join(STORIES_DIR, f"{letter}_story.txt")
    if os.path.exists(story_path):
        with open(story_path, 'r', encoding='utf-8') as file:
            return file.read()
    return f"Story for letter {letter} not found."

# Function to get image as base64 for background styling
def get_image_as_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# Function to convert text to speech
def text_to_speech(text):
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp
    except Exception as e:
        st.error(f"Error generating audio: {e}")
        return None

# Function to get the appropriate audio directory based on voice selection
def get_voice_directory():
    selected_voice = st.session_state.selected_voice
    
    if selected_voice == "Female 1":
        return FEMALE1_AUDIO_DIR
    elif selected_voice == "Female 2":
        return FEMALE2_AUDIO_DIR
    elif selected_voice == "Male 1":
        return MALE1_AUDIO_DIR
    elif selected_voice == "Male 2":
        return MALE2_AUDIO_DIR
    else:
        # Default fallback to root audio directory
        return AUDIO_DIR

# Function to check for pre-recorded audio file
def get_audio(letter, story_for_tts=None):
    # Get the appropriate voice directory
    voice_dir = get_voice_directory()
    
    # Check if pre-recorded audio file exists in voice directory
    audio_file_path = os.path.join(voice_dir, f"{letter}_story.mp3")
    
    if os.path.exists(audio_file_path):
        # Return the pre-recorded audio file
        with open(audio_file_path, "rb") as file:
            return file.read()
    else:
        # Fall back to root audio directory
        fallback_audio_path = os.path.join(AUDIO_DIR, f"{letter}_story.mp3")
        if os.path.exists(fallback_audio_path):
            with open(fallback_audio_path, "rb") as file:
                return file.read()
        elif story_for_tts:
            # Generate audio on the fly if no pre-recorded file exists
            return text_to_speech(story_for_tts)
    
    return None

# Function to ask questions about the story
def ask_about_story(question, letter, story_content):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"You are a helpful assistant for a children's alphabet book. You're answering questions about the letter {letter} story. Keep your answers child-friendly, educational, and engaging. Limit your responses to 3-4 sentences."},
                {"role": "user", "content": f"Here's the story about letter {letter}:\n\n{story_content}\n\nQuestion: {question}"}
            ],
            max_tokens=250,  # Increased from 150 to allow longer responses
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"I couldn't get an answer right now. Please try again later. Error: {str(e)}"

# Custom CSS to make the app more child-friendly and compact
def apply_custom_css():
    st.markdown("""
    <style>
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Reduce top padding to bring title closer to top */
    .main .block-container {
        padding-top: 1rem !important;
    }
    
    /* Overall styling */
    .main {
        background-color: #f5f7ff;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    
    /* Title area styling */
    h1, h2, h3 {
        color: #4b6cb7;
        margin-top: 0;
    }
    .stTitle {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Title with attribution */
    .title-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    .attribution {
        font-size: 0.85rem;
        color: #666;
    }
    .attribution a {
        color: #4285F4;
        text-decoration: none;
    }
    .attribution a:hover {
        text-decoration: underline;
    }
    
    /* Buttons with consistent blue theme */
    .stButton>button {
        background-color: #4285F4;
        color: white;
        border-radius: 20px;
        font-size: 16px;
        padding: 6px 14px;
        border: none;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        background-color: #3367D6;
    }
    
    /* Question button */
    .ask-button button {
        background-color: #EA4335;
        color: white;
        font-weight: bold;
    }
    .ask-button button:hover {
        background-color: #D62516;
    }
    
    /* Sidebar styling */
    .sidebar-buttons {
        margin-bottom: 20px;
    }
    .sidebar-section {
        margin-bottom: 12px;
        padding-bottom: 12px;
        border-bottom: 1px solid #e0e0e0;
    }
    .sidebar-title {
        font-weight: bold;
        margin-bottom: 5px;
        color: #4b6cb7;
    }
    
    /* Voice options styling */
    .voice-options {
        display: flex;
        flex-wrap: wrap;
        gap: 5px;
    }
    .voice-option label {
        font-size: 0.9rem;
    }
    
    /* Compact chatbot */
    .compact-chatbot {
        padding: 8px !important;
        margin-bottom: 12px !important;
    }
    .compact-chatbot input {
        padding: 4px 8px !important;
        font-size: 14px !important;
        min-height: 80px !important; /* Taller input area */
    }
    .compact-chatbot button {
        padding: 4px 8px !important;
        font-size: 14px !important;
        height: auto !important;
    }
    
    .story-container {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
        height: 650px;
        overflow-y: auto;
    }
    .image-container {
        text-align: center;
        margin-bottom: 15px;
        width: 100%;
    }
    .image-caption {
        font-style: italic;
        margin-top: 8px;
        font-size: 14px;
        color: #666;
    }
    .story-text {
        font-size: 17px;
        line-height: 1.5;
        color: #333;
    }
    
    /* Audio player styling */
    audio {
        width: 100%;
        margin-top: 5px;
        margin-bottom: 5px;
    }
    
    /* Image display enhancements */
    .larger-image img {
        width: 100%;
        height: auto;
        object-fit: contain;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Image controls */
    .image-controls {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-bottom: 12px;
    }
    
    /* Audio controls */
    .audio-controls {
        margin-top: 8px;
        margin-bottom: 8px;
        background-color: #f0f5ff;
        padding: 8px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Chatbot area */
    .chatbot-area {
        background-color: #f0f8ff;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .chatbot-response {
        background-color: #e8f4f8;
        padding: 12px;
        border-radius: 10px;
        margin-top: 8px;
        max-height: 200px;  /* Taller response area */
        overflow-y: auto;
    }
    
    /* Letter selector */
    .letter-selector {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 5px;
        margin-top: 8px;
        margin-bottom: 15px;
    }
    
    /* Google-inspired color scheme for letter buttons */
    .letter-button-A, .letter-button-E, .letter-button-I, .letter-button-M, .letter-button-Q, .letter-button-U, .letter-button-Y {
        background-color: #4285F4 !important; /* Google Blue */
    }
    
    .letter-button-B, .letter-button-F, .letter-button-J, .letter-button-N, .letter-button-R, .letter-button-V, .letter-button-Z {
        background-color: #EA4335 !important; /* Google Red */
    }
    
    .letter-button-C, .letter-button-G, .letter-button-K, .letter-button-O, .letter-button-S, .letter-button-W {
        background-color: #FBBC05 !important; /* Google Yellow */
    }
    
    .letter-button-D, .letter-button-H, .letter-button-L, .letter-button-P, .letter-button-T, .letter-button-X {
        background-color: #34A853 !important; /* Google Green */
    }
    
    .stButton>button.letter-button:hover {
        opacity: 0.9;
        transform: translateY(-2px);
    }
    
    /* Current letter button */
    .current-letter button {
        transform: scale(1.1);
        box-shadow: 0 0 10px rgba(0,0,0,0.3);
    }
    
    /* Premium feature message */
    .premium-message {
        background-color: #fff3cd;
        color: #856404;
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
        border-left: 5px solid #ffeeba;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to display premium feature message
def show_premium_message(feature_name):
    st.warning(f"**{feature_name}** is a premium feature. Please sign in and purchase the book to unlock this feature.")

# Main application
def main():
    apply_custom_css()
    
    # Set session state for current letter if not existing
    if 'current_letter' not in st.session_state:
        st.session_state.current_letter = 'A'
    
    # Set session state for image style if not existing
    if 'image_style' not in st.session_state:
        st.session_state.image_style = "Realistic"
    
    # Set default UI controls if not existing
    if 'show_prev_next' not in st.session_state:
        st.session_state.show_prev_next = True
        
    if 'show_alphabet' not in st.session_state:
        st.session_state.show_alphabet = True
        
    if 'show_chatbot' not in st.session_state:
        st.session_state.show_chatbot = True
        
    if 'show_read_button' not in st.session_state:
        st.session_state.show_read_button = True
        
    if 'show_realistic' not in st.session_state:
        st.session_state.show_realistic = True
        
    if 'show_watercolor' not in st.session_state:
        st.session_state.show_watercolor = True
    
    # Current letter
    letter = st.session_state.current_letter
    story_content = read_story(letter)
    
    # Check if user can access this letter
    can_access_letter = True
    if ord(letter) - ord('A') > 2 and not st.session_state.has_purchased:
        can_access_letter = False
    
    # Sidebar
    with st.sidebar:
        st.title("Book Options")
        
        # User Account section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">User Account</div>', unsafe_allow_html=True)
        
        if not st.session_state.is_registered:
            if st.button("📝 Register", use_container_width=True):
                st.session_state.is_registered = True
                st.success("You're now registered!")
                st.rerun()
                
            if st.button("🔑 Sign In", use_container_width=True):
                st.session_state.is_registered = True
                st.success("You're now signed in!")
                st.rerun()
        else:
            st.success("✅ Signed in as Guest User")
            if st.button("Sign Out", use_container_width=True):
                st.session_state.is_registered = False
                st.session_state.has_purchased = False
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Purchase Options section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">Purchase Options</div>', unsafe_allow_html=True)
        
        if not st.session_state.has_purchased:
            if st.button("🛒 Buy This Book ($15)", use_container_width=True):
                st.session_state.has_purchased = True
                st.success("Thank you for your purchase!")
                st.rerun()
        else:
            st.success("✅ You own this book")
        
        gift_button = st.button("🎁 Send As Gift", use_container_width=True)
        if gift_button:
            show_premium_message("Send As Gift")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Simplified Voice Options section - just radio buttons, no extra buttons
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">Voice Options</div>', unsafe_allow_html=True)
        
        # Simple voice selection with a single radio button group
        selected_voice = st.radio(
            "Select voice:",
            options=["Female 1", "Female 2", "Male 1", "Male 2"],
            horizontal=True,
            index=["Female 1", "Female 2", "Male 1", "Male 2"].index(st.session_state.selected_voice)
        )
        
        # Update session state if voice changed
        if selected_voice != st.session_state.selected_voice:
            st.session_state.selected_voice = selected_voice
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display Controls section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">Display Controls</div>', unsafe_allow_html=True)
        
        st.session_state.show_prev_next = st.checkbox("Show Previous/Next Buttons", value=st.session_state.show_prev_next)
        st.session_state.show_alphabet = st.checkbox("Show A-Z Buttons", value=st.session_state.show_alphabet)
        st.session_state.show_chatbot = st.checkbox("Show AI Chatbot", value=st.session_state.show_chatbot)
        st.session_state.show_read_button = st.checkbox("Show Read Story Button", value=st.session_state.show_read_button)
        st.session_state.show_realistic = st.checkbox("Show Realistic Style Option", value=st.session_state.show_realistic)
        st.session_state.show_watercolor = st.checkbox("Show Watercolor Style Option", value=st.session_state.show_watercolor)
        
        # Ensure at least one navigation method is enabled
        if not st.session_state.show_prev_next and not st.session_state.show_alphabet:
            st.warning("At least one navigation method must be enabled")
            st.session_state.show_prev_next = True
        
        # Ensure at least one image style is enabled
        if not st.session_state.show_realistic and not st.session_state.show_watercolor:
            st.warning("At least one image style must be enabled")
            st.session_state.show_realistic = True
            
        # Update image style if the selected style is disabled
        if not st.session_state.show_realistic and st.session_state.image_style == "Realistic":
            st.session_state.image_style = "Watercolor"
        elif not st.session_state.show_watercolor and st.session_state.image_style == "Watercolor":
            st.session_state.image_style = "Realistic"
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Additional features section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">Additional Features</div>', unsafe_allow_html=True)
        
        share_button = st.button("📤 Share This Book", use_container_width=True)
        if share_button:
            show_premium_message("Share This Book")
            
        like_button = st.button("👍 Like This Book", use_container_width=True)
        if like_button:
            show_premium_message("Like This Book")
            
        personalize_button = st.button("👤 Become Part Of The Story", use_container_width=True)
        if personalize_button:
            show_premium_message("Become Part Of The Story")
            
        create_button = st.button("✏️ Create Your Own Book", use_container_width=True)
        if create_button:
            show_premium_message("Create Your Own Book")
            
        earn_button = st.button("💰 Earn Money From This Book", use_container_width=True)
        if earn_button:
            show_premium_message("Earn Money From This Book")
            
        limited_button = st.button("🌟 Get Limited Edition", use_container_width=True)
        if limited_button:
            show_premium_message("Get Limited Edition")
            
        surprise_button = st.button("🎁 Surprise Me", use_container_width=True)
        if surprise_button:
            show_premium_message("Surprise Me")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content area with title and attribution
    st.markdown(
        '<div class="title-container">'
        '<h1>Jack and Jill\'s Alphabet Adventure</h1>'
        '<div class="attribution">Designed by <a href="https://www.linkedin.com/in/lindsayhiebert/" target="_blank">Lindsay Hiebert</a></div>'
        '</div>',
        unsafe_allow_html=True
    )
    
    # Extract title from story content if available
    title = "Alphabet Adventure"
    title_line = next((line for line in story_content.split('\n') if f"Title: {letter} -" in line), None)
    if title_line:
        title = title_line.replace(f"Title: {letter} -", "").strip()
    
    # Premium content warning for letters beyond C
    if not can_access_letter:
        st.warning(f"💎 **Premium Content** - Letters beyond 'C' are available after purchase. See the first 3 letters for free!")
    
    # Top navigation and controls
    if st.session_state.show_prev_next:
        col_prev, col_letter, col_next = st.columns([1, 3, 1])
        
        with col_prev:
            if letter != 'A':
                prev_letter = chr(ord(letter) - 1)
                if st.button(f"← Previous ({prev_letter})", key="prev_top", use_container_width=True):
                    st.session_state.current_letter = prev_letter
                    st.rerun()
        
        with col_letter:
            st.subheader(f"Letter {letter}")
        
        with col_next:
            if letter != 'Z':
                next_letter = chr(ord(letter) + 1)
                if st.button(f"Next ({next_letter}) →", key="next_top", use_container_width=True):
                    st.session_state.current_letter = next_letter
                    st.rerun()
    else:
        st.subheader(f"Letter {letter}")
    
    # A-Z alphabet buttons
    if st.session_state.show_alphabet:
        # First row of letters (A-M)
        cols1 = st.columns(13)
        for i, col in enumerate(cols1):
            if i < 13:  # A through M
                current_letter = chr(65 + i)  # ASCII: A=65, B=66, etc.
                is_current = current_letter == letter
                with col:
                    # Add Google-inspired color class based on letter
                    button_class = f"letter-button-{current_letter}"
                    if is_current:
                        button_class += " current-letter"
                    
                    st.markdown(f'<div class="{button_class}">', unsafe_allow_html=True)
                    if st.button(current_letter, key=f"letter_{current_letter}"):
                        new_letter = current_letter
                        # Check if user can access this letter
                        if ord(new_letter) - ord('A') > 2 and not st.session_state.has_purchased:
                            st.warning("Please purchase the book to access letters beyond C")
                        else:
                            st.session_state.current_letter = new_letter
                            st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
        
        # Second row of letters (N-Z)
        cols2 = st.columns(13)
        for i, col in enumerate(cols2):
            if i < 13:  # N through Z
                if i + 13 < 26:  # Ensure we don't go beyond Z
                    current_letter = chr(78 + i)  # ASCII: N=78, O=79, etc.
                    is_current = current_letter == letter
                    with col:
                        # Add Google-inspired color class based on letter
                        button_class = f"letter-button-{current_letter}"
                        if is_current:
                            button_class += " current-letter"
                        
                        st.markdown(f'<div class="{button_class}">', unsafe_allow_html=True)
                        if st.button(current_letter, key=f"letter_{current_letter}_2"):
                            new_letter = current_letter
                            # Check if user can access this letter
                            if ord(new_letter) - ord('A') > 2 and not st.session_state.has_purchased:
                                st.warning("Please purchase the book to access letters beyond C")
                            else:
                                st.session_state.current_letter = new_letter
                                st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)
    
    # Chatbot input - now with taller input box and response area
    if st.session_state.show_chatbot:
        st.markdown('<div class="chatbot-area compact-chatbot">', unsafe_allow_html=True)
        
        chat_col1, chat_col2 = st.columns([3, 1])
        
        with chat_col1:
            user_question = st.text_area("Ask a question about this story:", 
                                      placeholder="Example: What are the main characters in this story?", 
                                      label_visibility="collapsed",
                                      height=80)  # Taller input area
        
        with chat_col2:
            st.markdown('<div class="ask-button">', unsafe_allow_html=True)
            ask_button = st.button("Ask Question", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Initialize container for chat response
        chat_response = st.empty()
        
        if user_question and ask_button:
            with st.spinner("Getting answer..."):
                # Check if premium content
                if not can_access_letter:
                    chat_response.warning("Purchase the book to ask questions about this letter!")
                else:
                    answer = ask_about_story(user_question, letter, story_content)
                    chat_response.markdown(f"<div class='chatbot-response'><strong>Answer:</strong> {answer}</div>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content layout - story and image
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Display the story in a nice container
        if can_access_letter:
            st.markdown(f"<div class='story-container'><h2>{title}</h2><div class='story-text'>{story_content.replace(title_line, '').strip() if title_line else story_content}</div></div>", unsafe_allow_html=True)
        else:
            # Show preview with purchase message
            preview = story_content.split('\n\n')[0:2]
            preview_text = '\n\n'.join(preview) + "\n\n[... Purchase to read the full story ...]"
            st.markdown(f"<div class='story-container'><h2>{title}</h2><div class='story-text'>{preview_text}</div></div>", unsafe_allow_html=True)
        
        # Read story button
        if st.session_state.show_read_button:
            read_button = st.button("🔊 Read the Story", key="read_main", use_container_width=True)
            
            # Audio player container
            audio_container = st.container()
            
            if read_button:
                with audio_container:
                    st.markdown('<div class="audio-controls">', unsafe_allow_html=True)
                    
                    # Check if premium content
                    if not can_access_letter:
                        st.warning("Purchase the book to hear the full story!")
                    else:
                        with st.spinner(f"Loading {st.session_state.selected_voice} voice..."):
                            # Prepare text for TTS by removing title and questions
                            story_for_tts = story_content
                            if title_line:
                                story_for_tts = story_for_tts.replace(title_line, '')
                            
                            # Remove questions section if it exists
                            questions_idx = story_for_tts.find("Questions:")
                            if questions_idx != -1:
                                story_for_tts = story_for_tts[:questions_idx]
                            
                            # Clean up and prepare for TTS
                            story_for_tts = story_for_tts.strip()
                            
                            # Check for pre-recorded audio file first, or generate on the fly
                            audio_data = get_audio(letter, story_for_tts)
                            
                            if audio_data:
                                # Display audio player
                                st.audio(audio_data, format="audio/mp3")
                                
                                # Display which voice is being used
                                st.info(f"Playing with {st.session_state.selected_voice} voice")
                                
                                # Add download button for the audio
                                st.download_button(
                                    label="Download Audio",
                                    data=audio_data,
                                    file_name=f"letter_{letter}_story_{st.session_state.selected_voice.replace(' ', '_').lower()}.mp3",
                                    mime="audio/mp3",
                                    use_container_width=True
                                )
                            else:
                                st.error("Failed to load or generate audio. Please try again.")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Display image based on selected style
        realistic_img_path = os.path.join(REALISTIC_IMAGES_DIR, f"{letter}.png")
        watercolor_img_path = os.path.join(WATERCOLOR_IMAGES_DIR, f"{letter}.png")
        
        # Image style toggle at the top
        if st.session_state.show_realistic and st.session_state.show_watercolor:
            st.markdown('<div class="image-controls">', unsafe_allow_html=True)
            style_col1, style_col2 = st.columns(2)
            
            with style_col1:
                if st.button("Realistic", use_container_width=True, 
                            disabled=st.session_state.image_style == "Realistic"):
                    st.session_state.image_style = "Realistic"
                    st.rerun()
            
            with style_col2:
                if st.button("Watercolor", use_container_width=True, 
                            disabled=st.session_state.image_style == "Watercolor"):
                    st.session_state.image_style = "Watercolor"
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Image container with enhanced size
        image_container = st.container()
        
        with image_container:
            st.markdown('<div class="larger-image">', unsafe_allow_html=True)
            
            if st.session_state.image_style == "Realistic" and st.session_state.show_realistic:
                if os.path.exists(realistic_img_path):
                    st.image(realistic_img_path, caption=f"Realistic illustration for letter {letter}", use_container_width=True)
                else:
                    st.warning(f"Realistic image for letter {letter} not found.")
            elif st.session_state.image_style == "Watercolor" and st.session_state.show_watercolor:
                if os.path.exists(watercolor_img_path):
                    st.image(watercolor_img_path, caption=f"Watercolor illustration for letter {letter}", use_container_width=True)
                else:
                    st.warning(f"Watercolor image for letter {letter} not found.")
            elif st.session_state.show_realistic:
                if os.path.exists(realistic_img_path):
                    st.image(realistic_img_path, caption=f"Realistic illustration for letter {letter}", use_container_width=True)
                else:
                    st.warning(f"Realistic image for letter {letter} not found.")
            elif st.session_state.show_watercolor:
                if os.path.exists(watercolor_img_path):
                    st.image(watercolor_img_path, caption=f"Watercolor illustration for letter {letter}", use_container_width=True)
                else:
                    st.warning(f"Watercolor image for letter {letter} not found.")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Image download button
        if st.session_state.image_style == "Realistic" and st.session_state.show_realistic and os.path.exists(realistic_img_path):
            if can_access_letter:
                with open(realistic_img_path, "rb") as file:
                    btn = st.download_button(
                        label="Download Image",
                        data=file,
                        file_name=f"letter_{letter}_realistic.png",
                        mime="image/png",
                        use_container_width=True
                    )
            else:
                if st.button("Download Image (Premium)", use_container_width=True):
                    show_premium_message("Download Image")
        
        elif st.session_state.image_style == "Watercolor" and st.session_state.show_watercolor and os.path.exists(watercolor_img_path):
            if can_access_letter:
                with open(watercolor_img_path, "rb") as file:
                    btn = st.download_button(
                        label="Download Image",
                        data=file,
                        file_name=f"letter_{letter}_watercolor.png",
                        mime="image/png",
                        use_container_width=True
                    )
            else:
                if st.button("Download Image (Premium)", use_container_width=True):
                    show_premium_message("Download Image")

# Run the app
if __name__ == "__main__":
    main()