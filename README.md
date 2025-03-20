# 📚 Jack and Jill's Alphabet Adventure

An interactive children's alphabet book application built with Streamlit, featuring narration in multiple voices, beautiful illustrations, and an AI-powered chatbot.

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

## 📱 Getting Started

### Prerequisites
- Python 3.8+
- Google Cloud account (for Text-to-Speech API)
- OpenAI API key (for chatbot functionality)

### Installation

1. Clone this repository
```bash
git clone https://github.com/lhiebert01/alphabet-book-app.git
cd alphabet-book-app
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
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/google-credentials.json
```

5. Run the app
```bash
streamlit run alphabet_book_streamlit_app11.py
```

## 📂 Project Structure

```
alphabet-book-app/
├── alphabet_book_streamlit_app11.py  # Main Streamlit application
├── alphabet_stories_new/             # Story text files (A_story.txt through Z_story.txt)
├── alphabet_images_new/              # Realistic illustrations (A.png through Z.png)
├── alphabet_images_new_illustrations/ # Watercolor illustrations (A.png through Z.png)
├── alphabet_audio_files/             # Base audio directory
│   ├── female1/                      # Female voice 1 audio files
│   ├── female2/                      # Female voice 2 audio files
│   ├── male1/                        # Male voice 1 audio files
│   └── male2/                        # Male voice 2 audio files
├── requirements.txt                  # Required dependencies
└── README.md                         # Project documentation
```

## 🔧 Voice Generation Tools

The project includes tools for generating audio files in different voices:

- **dual_voice_generator.py**: Generate audio files with both male and female voices
- **google_tts_audio_generator.py**: Generate audio files using Google Cloud Text-to-Speech

## 🚀 Deployment

### Render

This app can be deployed to Render following these steps:

1. Push your code to GitHub
2. Log in to [Render](https://render.com)
3. Create a new Web Service, select your GitHub repo
4. Configure as follows:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run alphabet_book_streamlit_app11.py`
5. Add environment variables for your API keys
6. Deploy

### Future Integrations

The project roadmap includes:
- Database authentication
- User registration and management
- Payment processing via Stripe
- Subscription tracking
- Gumroad integration for digital distribution

## 👥 Contributing

Contributions are welcome! Please feel free to submit a pull request.

## 📄 License

This project is licensed under the MIT License.

## 👤 Contact

Developed by [Lindsay Hiebert](https://www.linkedin.com/in/lindsayhiebert/)
- LinkedIn: [lindsayhiebert](https://www.linkedin.com/in/lindsayhiebert/)

## Contact

Developed by [Lindsay Hiebert](https://www.linkedin.com/in/lindsayhiebert/)
- GitHub: [lhiebert01](https://github.com/lhiebert01)
- LinkedIn: [lindsayhiebert](https://www.linkedin.com/in/lindsayhiebert/)