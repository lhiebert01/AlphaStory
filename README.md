# 📚 Jack and Jill's Alphabet Adventure

An interactive children's alphabet book application built with Streamlit, featuring narration in multiple voices, beautiful illustrations, and an AI-powered chatbot.

![App Screenshot](Jack_and_Jill_Alphabet_Adventures_Streamlit_app_screen.png)

## 🌟 Features

### Story Experience
- **26 Unique Stories**: From A to Z, each with its own theme and learning goals
- **Dual Illustration Styles**: Choose between realistic 3D illustrations and watercolor art
- **Multiple Voice Options**: Listen to the stories in different male and female voices
- **Flexible Navigation**: Browse sequentially or jump to specific letters

### Interactive Learning
- **AI Chatbot**: Ask questions about any story and get child-friendly answers
- **Educational Content**: Each story teaches about the featured letter with relevant vocabulary
- **Discussion Questions**: Every story includes questions for parents and educators to use

### Cross-Platform Support
- **Desktop Compatibility**: Works seamlessly on Chrome, Firefox, Safari, and Edge
- **Mobile Support**: Full iOS support including audio playback on iPhone and iPad
- **Tablet Optimization**: Responsive design for various screen sizes

## 📱 Getting Started

### Prerequisites
- Python 3.8+
- OpenAI API key (for chatbot functionality)

### Installation

1. Clone this repository
```bash
git clone https://github.com/lhiebert01/AlphaStory.git
cd AlphaStory
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API keys
```
OPENAI_API_KEY=your-openai-api-key-here
```

5. Run the app
```bash
streamlit run app.py
```

## 📂 Project Structure

```
AlphaStory/
├── app.py                           # Main Streamlit application
├── alphabet_stories_new/            # Story text files (A_story.txt through Z_story.txt)
├── alphabet_images_new/             # Realistic illustrations (A.png through Z.png)
├── alphabet_images_new_illustrations/ # Watercolor illustrations (A.png through Z.png)
├── alphabet_audio_files/            # Base audio directory
│   ├── female1/                     # Female voice 1 audio files
│   ├── female2/                     # Female voice 2 audio files
│   ├── male1/                       # Male voice 1 audio files
│   └── male2/                       # Male voice 2 audio files
├── requirements.txt                 # Required dependencies
├── render.yaml                      # Render deployment configuration
└── README.md                        # Project documentation
```

## 🔧 Voice Features

The application includes:

- **Pre-recorded audio narration** for all 26 stories
- **Multiple voice options**: Choose between Female 1, Female 2, Male 1 and Male 2 voices
- **Cross-platform audio playback**: Compatible with desktop browsers and iOS mobile devices

## 🚀 Deployment

This application is deployed at [https://alphastory.onrender.com/](https://alphastory.onrender.com/)

For detailed deployment instructions, please see [DEPLOYMENT-GUIDE.md](DEPLOYMENT-GUIDE.md).

## 📄 License & Copyright

**© 2024 Lindsay Hiebert. All Rights Reserved.**

This is proprietary software. The code, documentation, stories, illustrations, and audio content are protected by copyright law.

**Usage Restrictions:**
- No use, copying, modification, merging, publication, distribution, sublicensing, or selling of this software is permitted without explicit written permission from the copyright owner.
- Commercial use of any part of this project requires prior written approval.
- For inquiries regarding licensing or usage, please contact the copyright owner.

## 👤 Contact

Developed by [Lindsay Hiebert](https://www.linkedin.com/in/lindsayhiebert/)
- GitHub: [lhiebert01](https://github.com/lhiebert01)
- LinkedIn: [lindsayhiebert](https://www.linkedin.com/in/lindsayhiebert/)



