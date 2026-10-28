# 📁 File Manager - Streamlit Version

A modern, user-friendly file management application built with Streamlit that allows you to browse, manage, and manipulate files and directories on your system.

## 🚀 Features

- **📂 Directory Viewer**: Browse and view directory contents with file/folder details
- **✏️ File Renaming**: Rename files with ease
- **🗑️ File Deletion**: Delete files with confirmation
- **📁 Directory Creation**: Create new directories
- **📄 File Content Viewer**: View text file contents
- **⚡ Quick Access**: Quick navigation to common directories
- **🎨 Modern UI**: Beautiful gradient styling and responsive design

## 🛠️ Installation

1. **Navigate to the project directory:**
   ```bash
   cd file_handling
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Features Overview

#### 📂 Directory Viewer
- Enter a directory path to view its contents
- Shows files and folders with size and modification time
- Displays file/folder counts
- Quick access buttons for common directories

#### ✏️ Rename File
- Specify directory path and file names
- Rename files safely with error handling
- Instant feedback on success/failure

#### 🗑️ Delete File
- Delete files with confirmation checkbox
- Safety measures to prevent accidental deletion
- Clear success/error messages

#### 📁 Create Directory
- Create new directories in any location
- Automatic path validation
- Error handling for existing directories

#### 📄 View File Content
- View text file contents
- File information display (size, modification time)
- Support for UTF-8 encoded files

#### ⚡ Quick Actions
- **Quick Access**: Buttons for Desktop, Documents, Downloads, etc.
- **Refresh**: Reload the current view
- **System Info**: Display system information

## 📁 Project Structure

```
file_handling/
├── app.py              # Main Streamlit application
├── file_manager.py     # Original Gradio version (for reference)
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🎨 UI Features

### Modern Design
- **Gradient Backgrounds**: Beautiful color transitions
- **Responsive Layout**: Works on all screen sizes
- **Tabbed Interface**: Organized functionality
- **Styled Messages**: Success/error messages with colors
- **Interactive Elements**: Hover effects and animations

### Color Scheme
- **Main Header**: Blue-purple gradient
- **Success Messages**: Green gradient
- **Error Messages**: Red-orange gradient
- **Tab Containers**: Light blue gradient
- **Sidebar**: Light gradient with borders

## 🔧 Configuration

### Port Configuration
The app runs on the default Streamlit port (8501). To change the port:

```bash
streamlit run app.py --server.port 8502
```

### Custom Styling
The app includes custom CSS for enhanced styling. You can modify the styles in the `app.py` file.

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

1. **Permission Errors**: Make sure you have read/write permissions for the directories you're accessing
2. **File Not Found**: Double-check file paths and names
3. **Port Conflicts**: If port 8501 is busy, use a different port
4. **Unicode Errors**: Some files may not be readable as text

### Debug Mode
Run with debug information:
```bash
streamlit run app.py --logger.level debug
```

## 📊 Requirements

- Python 3.7+
- Streamlit 1.28.0+
- File system access permissions

## 🤝 Contributing

Feel free to contribute to this project by:
- Adding new file operations
- Improving the UI/UX
- Adding file upload/download features
- Enhancing error handling

## 📄 License

This project is open source and available under the MIT License.

## 🔗 Links

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Python os Module](https://docs.python.org/3/library/os.html)
- [File System Operations](https://docs.python.org/3/library/shutil.html)

---

**Made with ❤️ using Streamlit** 