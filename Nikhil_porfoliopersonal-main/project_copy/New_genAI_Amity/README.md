# 🤖 Tech2Idea Chatbot - Streamlit Version

A conversational AI assistant that helps you transform your technical skills into unique project ideas using Google's Gemini AI.

## 🚀 Features

- **Interactive Chat Interface**: Natural conversation with the AI assistant
- **Project Idea Generation**: Get personalized project suggestions based on your skills
- **Technology Recommendations**: Receive guidance on tools and technologies
- **User-Friendly Interface**: Clean, modern Streamlit web interface
- **Session Management**: Remembers your name and conversation context

## 🛠️ Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd projects/New_genAI
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Gemini API key:**
   - Create a `.env` file in the project directory
   - Add your API key: `GEMINI_API_KEY=your_api_key_here`
   - Or use the demo key (limited functionality)

## 🎯 Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### How to Use

1. **Introduce yourself**: "My name is [Your Name]"
2. **Share your skills**: "I know Python, JavaScript, and React"
3. **Get project ideas**: The AI will generate personalized suggestions
4. **Ask for help**: Type "help" for more information

### Example Conversations

```
User: "My name is Alex and I know Python, JavaScript, and React"
Bot: "Nice to meet you, Alex! I'm your Tech2Idea assistant..."

User: "I want to build a web application"
Bot: "Here are some project ideas for you, Alex:
     1. Project Name: Task Management Dashboard
     2. Required Tools: React, Node.js, MongoDB
     3. Description: A full-stack web app for managing tasks..."
```

## 📁 Project Structure

```
New_genAI/
├── app.py              # Main Streamlit application
├── gemini_api.py       # Google Gemini AI integration
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── .env               # Environment variables (create this)
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:
```
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### API Key Setup

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

## 🎨 Features

### Chat Interface
- Real-time conversation with AI
- Message history preservation
- User-friendly input/output

### Quick Actions
- Popular skill buttons for quick access
- Clear chat functionality
- Statistics tracking

### Project Suggestions
- Personalized project ideas
- Technology recommendations
- Difficulty levels
- Time estimates

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Production Deployment
The app can be deployed to:
- Streamlit Cloud
- Heroku
- AWS/GCP/Azure
- Any platform supporting Streamlit

## 🔍 Troubleshooting

### Common Issues

1. **API Key Error**: Make sure your `.env` file contains the correct API key
2. **Import Errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
3. **Port Conflicts**: If port 8501 is busy, Streamlit will automatically use the next available port

### Debug Mode
Run with debug information:
```bash
streamlit run app.py --logger.level debug
```

## 📊 Requirements

- Python 3.7+
- Google Gemini API key
- Internet connection for AI responses

## 🤝 Contributing

Feel free to contribute to this project by:
- Adding new features
- Improving the UI/UX
- Enhancing the AI prompts
- Adding more project templates

## 📄 License

This project is open source and available under the MIT License.

## 🔗 Links

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google Gemini AI](https://ai.google.dev/)
- [Python Documentation](https://docs.python.org/)

---

**Made with ❤️ using Streamlit and Google Gemini AI** 