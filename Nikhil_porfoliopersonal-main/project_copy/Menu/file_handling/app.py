import streamlit as st
import os
import shutil
from datetime import datetime
import tempfile

# Page configuration
st.set_page_config(
    page_title="File Manager",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .tab-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .file-item {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 0.8rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(79, 172, 254, 0.3);
    }
    
    .folder-item {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        color: #333;
        padding: 0.8rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(255, 154, 158, 0.3);
    }
    
    .success-message {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(67, 233, 123, 0.3);
    }
    
    .error-message {
        background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
    }
    
    .input-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
    }
    
    .sidebar-section {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
</style>
""", unsafe_allow_html=True)

def format_size(size_bytes):
    """Convert size in bytes to human readable format"""
    if size_bytes < 1024:
        return f"{size_bytes:,} bytes"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes/1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes/(1024*1024):.1f} MB"
    else:
        return f"{size_bytes/(1024*1024*1024):.1f} GB"

def get_directory_contents(directory):
    """Get formatted directory contents"""
    try:
        if not os.path.exists(directory):
            return "Directory does not exist"
        
        items = os.listdir(directory)
        if not items:
            return "Directory is empty"
        
        # Separate files and folders
        folders = []
        files = []
        
        for item in items:
            full_path = os.path.join(directory, item)
            if os.path.isdir(full_path):
                # Get folder size and item count
                folder_size = 0
                item_count = 0
                for root, dirs, filenames in os.walk(full_path):
                    for filename in filenames:
                        file_path = os.path.join(root, filename)
                        folder_size += os.path.getsize(file_path)
                        item_count += 1
                
                size_str = format_size(folder_size)
                folders.append(f"📁 {item}/ ({size_str}, {item_count} items)")
            else:
                # Get file size and last modified time
                size = os.path.getsize(full_path)
                modified_time = datetime.fromtimestamp(os.path.getmtime(full_path))
                size_str = format_size(size)
                time_str = modified_time.strftime("%Y-%m-%d %H:%M")
                files.append(f"📄 {item} ({size_str}, modified: {time_str})")
        
        # Sort folders and files alphabetically
        folders.sort()
        files.sort()
        
        # Combine results
        result = []
        if folders:
            result.append("📁 Folders:")
            result.extend(folders)
            result.append("")  # Empty line for separation
        
        if files:
            result.append("📄 Files:")
            result.extend(files)
        
        return "\n".join(result)
    except Exception as e:
        return f"Error: {str(e)}"

def rename_file(directory, old_name, new_name):
    """Rename a file"""
    try:
        if not os.path.exists(directory):
            return "Directory does not exist"
        
        old_path = os.path.join(directory, old_name)
        if not os.path.exists(old_path):
            return f"File '{old_name}' not found"
        
        new_path = os.path.join(directory, new_name)
        if os.path.exists(new_path):
            return f"File '{new_name}' already exists"
        
        os.rename(old_path, new_path)
        return f"Successfully renamed '{old_name}' to '{new_name}'"
    except Exception as e:
        return f"Error: {str(e)}"

def delete_file(directory, filename):
    """Delete a file"""
    try:
        if not os.path.exists(directory):
            return "Directory does not exist"
        
        file_path = os.path.join(directory, filename)
        if not os.path.exists(file_path):
            return f"File '{filename}' not found"
        
        os.remove(file_path)
        return f"File '{filename}' deleted successfully"
    except Exception as e:
        return f"Error: {str(e)}"

def create_dir(directory, folder_name):
    """Create a new directory"""
    try:
        if not os.path.exists(directory):
            return "Parent directory does not exist"
        
        path = os.path.join(directory, folder_name)
        if os.path.exists(path):
            return f"Directory '{folder_name}' already exists"
        
        os.makedirs(path)
        return f"Directory '{folder_name}' created successfully"
    except Exception as e:
        return f"Error: {str(e)}"

def read_file_content(directory, filename):
    """Read file content"""
    try:
        if not os.path.exists(directory):
            return "Directory does not exist"
        
        file_path = os.path.join(directory, filename)
        if not os.path.exists(file_path):
            return f"File '{filename}' not found"
        
        if not os.path.isfile(file_path):
            return f"'{filename}' is not a file"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                return f"Content of {filename}:\n\n{content}"
        except UnicodeDecodeError:
            return f"Cannot read '{filename}': File is not a text file"
    except Exception as e:
        return f"Error: {str(e)}"

def display_message(message, is_success=True):
    """Display a styled message"""
    if is_success:
        st.markdown(f"""
        <div class="success-message">
            ✅ {message}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="error-message">
            ❌ {message}
        </div>
        """, unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>📁 File Manager</h1>
    <p>Manage your files and directories with ease!</p>
    <p>Browse, rename, delete, create, and view file contents.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for quick actions
with st.sidebar:
    st.markdown("""
    <div class="sidebar-section">
        <h3 style="text-align: center; color: #333; margin-bottom: 1rem;">⚡ Quick Actions</h3>
    """, unsafe_allow_html=True)
    
    # Quick directory buttons
    common_dirs = [
        "Desktop", "Documents", "Downloads", "Pictures", "Music", "Videos"
    ]
    
    st.subheader("📂 Quick Access")
    for dir_name in common_dirs:
        if st.button(f"📁 {dir_name}", key=f"dir_{dir_name}", use_container_width=True):
            user_home = os.path.expanduser("~")
            dir_path = os.path.join(user_home, dir_name)
            if os.path.exists(dir_path):
                st.session_state.current_directory = dir_path
                st.success(f"📁 Switched to {dir_name}")
            else:
                st.error(f"❌ {dir_name} directory not found")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-section">
        <h3 style="text-align: center; color: #333; margin-bottom: 1rem;">🔧 Tools</h3>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Refresh", key="sidebar_refresh", use_container_width=True):
        st.rerun()
    
    if st.button("📊 System Info", key="sidebar_system_info", use_container_width=True):
        import platform
        st.info(f"""
        **System Information:**
        - OS: {platform.system()} {platform.release()}
        - Python: {platform.python_version()}
        - Current Directory: {os.getcwd()}
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Initialize session state
if 'current_directory' not in st.session_state:
    st.session_state.current_directory = os.getcwd()

# Main content with tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📂 Directory Viewer", 
    "✏️ Rename File", 
    "🗑️ Delete File", 
    "📁 Create Directory", 
    "📄 View File Content"
])

# Tab 1: Directory Viewer
with tab1:
    st.markdown("""
    <div class="tab-container">
        <h3 style="text-align: center; color: #333; margin-bottom: 1.5rem;">📂 Directory Viewer</h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        directory_input = st.text_input(
            "Enter Directory Path",
            value=st.session_state.current_directory,
            placeholder="e.g., C:/Users/YourName/Documents",
            key="directory_viewer_input"
        )
    
    with col2:
        st.write("")  # Spacer
        browse_btn = st.button("🔍 View Directory", type="primary", use_container_width=True, key="browse_btn")
    
    if browse_btn or directory_input != st.session_state.current_directory:
        st.session_state.current_directory = directory_input
        contents = get_directory_contents(directory_input)
        
        if "Error:" in contents or "does not exist" in contents:
            display_message(contents, is_success=False)
        else:
            st.markdown("### 📋 Directory Contents")
            st.text_area("Contents", value=contents, height=400, disabled=True)
            
            # Show file count
            if "Files:" in contents:
                file_count = contents.count("📄")
                folder_count = contents.count("📁") - 1  # Subtract the header
                st.info(f"📊 Found {file_count} files and {folder_count} folders")

# Tab 2: Rename File
with tab2:
    st.markdown("""
    <div class="tab-container">
        <h3 style="text-align: center; color: #333; margin-bottom: 1.5rem;">✏️ Rename File</h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        rename_dir = st.text_input(
            "Directory Path",
            value=st.session_state.current_directory,
            placeholder="e.g., C:/Users/YourName/Documents",
            key="rename_dir_input"
        )
        old_name = st.text_input(
            "Current File Name",
            placeholder="e.g., oldfile.txt",
            key="old_name_input"
        )
    
    with col2:
        new_name = st.text_input(
            "New File Name",
            placeholder="e.g., newfile.txt",
            key="new_name_input"
        )
        st.write("")  # Spacer
        rename_btn = st.button("✏️ Rename File", type="primary", use_container_width=True, key="rename_btn")
    
    if rename_btn:
        if old_name and new_name:
            result = rename_file(rename_dir, old_name, new_name)
            if "Successfully" in result:
                display_message(result, is_success=True)
            else:
                display_message(result, is_success=False)
        else:
            display_message("Please enter both old and new file names", is_success=False)

# Tab 3: Delete File
with tab3:
    st.markdown("""
    <div class="tab-container">
        <h3 style="text-align: center; color: #333; margin-bottom: 1.5rem;">🗑️ Delete File</h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        delete_dir = st.text_input(
            "Directory Path",
            value=st.session_state.current_directory,
            placeholder="e.g., C:/Users/YourName/Documents",
            key="delete_dir_input"
        )
        delete_filename = st.text_input(
            "File Name to Delete",
            placeholder="e.g., file.txt",
            key="delete_filename_input"
        )
    
    with col2:
        st.write("")  # Spacer
        st.write("")  # Spacer
        delete_btn = st.button("🗑️ Delete File", type="primary", use_container_width=True, key="delete_btn")
    
    if delete_btn:
        if delete_filename:
            # Add confirmation
            if st.checkbox("⚠️ I confirm I want to delete this file"):
                result = delete_file(delete_dir, delete_filename)
                if "deleted successfully" in result:
                    display_message(result, is_success=True)
                else:
                    display_message(result, is_success=False)
        else:
            display_message("Please enter a file name to delete", is_success=False)

# Tab 4: Create Directory
with tab4:
    st.markdown("""
    <div class="tab-container">
        <h3 style="text-align: center; color: #333; margin-bottom: 1.5rem;">📁 Create Directory</h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        create_dir_path = st.text_input(
            "Parent Directory Path",
            value=st.session_state.current_directory,
            placeholder="e.g., C:/Users/YourName/Documents",
            key="create_dir_path_input"
        )
        folder_name = st.text_input(
            "New Folder Name",
            placeholder="e.g., newfolder",
            key="folder_name_input"
        )
    
    with col2:
        st.write("")  # Spacer
        st.write("")  # Spacer
        create_btn = st.button("📁 Create Directory", type="primary", use_container_width=True, key="create_btn")
    
    if create_btn:
        if folder_name:
            result = create_dir(create_dir_path, folder_name)
            if "created successfully" in result:
                display_message(result, is_success=True)
            else:
                display_message(result, is_success=False)
        else:
            display_message("Please enter a folder name", is_success=False)

# Tab 5: View File Content
with tab5:
    st.markdown("""
    <div class="tab-container">
        <h3 style="text-align: center; color: #333; margin-bottom: 1.5rem;">📄 View File Content</h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        view_dir = st.text_input(
            "Directory Path",
            value=st.session_state.current_directory,
            placeholder="e.g., C:/Users/YourName/Documents",
            key="view_dir_input"
        )
        view_filename = st.text_input(
            "File Name",
            placeholder="e.g., file.txt",
            key="view_filename_input"
        )
    
    with col2:
        st.write("")  # Spacer
        st.write("")  # Spacer
        view_btn = st.button("📄 View File", type="primary", use_container_width=True, key="view_btn")
    
    if view_btn:
        if view_filename:
            result = read_file_content(view_dir, view_filename)
            if "Content of" in result:
                st.markdown("### 📄 File Content")
                # Extract content after the header
                content_start = result.find("\n\n") + 2
                file_content = result[content_start:]
                st.text_area("Content", value=file_content, height=400, disabled=True)
                
                # Show file info
                file_path = os.path.join(view_dir, view_filename)
                if os.path.exists(file_path):
                    size = format_size(os.path.getsize(file_path))
                    modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    st.info(f"📊 File Size: {size} | Modified: {modified_time.strftime('%Y-%m-%d %H:%M')}")
            else:
                display_message(result, is_success=False)
        else:
            display_message("Please enter a file name to view", is_success=False)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>File Manager - Powered by Streamlit</p>
</div>
""", unsafe_allow_html=True) 