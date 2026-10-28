# Voice-Controlled Menu System

This is a Python-based voice-controlled menu system that can perform various tasks through voice commands. It provides both a terminal interface and a modern web interface using Streamlit.

## Features

- SSH login to remote machines
- Send WhatsApp messages
- Open applications (Notepad, Jupyter Notebook)
- Voice recognition and text-to-speech feedback
- Modern web interface with Streamlit
- Google search functionality
- Window management (minimize, maximize, close)
- Log viewing with password protection

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root and add your SSH password:
```
SSH_PASSWORD=your_password_here
```

3. Make sure you have a working microphone connected to your system.

## Usage

### Terminal Mode
Run the program in terminal mode:
```bash
python voice_menu.py
```

### Web Interface (Streamlit)
Run the Streamlit web interface:
```bash
streamlit run streamlit_voice_menu.py
```

### Available Commands

1. **send whatsapp** - Send WhatsApp messages
2. **ssh login** - Start SSH login process
3. **open notepad** - Open Notepad
4. **open jupyter** - Open Jupyter Notebook
5. **google search** - Perform Google searches
6. **minimize all** - Minimize all windows
7. **minimize** - Minimize current window
8. **maximize** - Maximize current window
9. **close window** - Close current window
10. **help** - Show available commands
11. **exit** - Exit the program
12. **log** - View application logs (password: "password")

### Project Management Commands

13. **list projects** - Show all available projects
14. **open project** - Open a project folder in file explorer
15. **run project** - Run a project (if it has an entry point like app.py, main.py, etc.)

### Supported Projects

The system automatically detects projects in:
- `projects/` folder (nested projects)
- `Resume maker/` directory
- `file_handling/` directory
- Any other project directories in the root folder

## Notes

- For SSH login, you'll need to speak the IP address and username clearly
- For WhatsApp messages, speak the phone number with country code
- The program uses Google's speech recognition service, so an internet connection is required
- WhatsApp Web should be logged in for sending WhatsApp messages
- Some commands (SSH, WhatsApp, window management) are only available in terminal mode
- The web interface supports both text input and audio file uploads 