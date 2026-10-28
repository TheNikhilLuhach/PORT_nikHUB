import streamlit as st
import tempfile
import os
import time
import subprocess
import threading
import queue
from voice_menu import VoiceMenu

# Page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="Voice Menu Assistant",
    page_icon="🎤",
    layout="wide"
)

# Initialize the VoiceMenu
@st.cache_resource(show_spinner=False)
def get_voice_menu():
    return VoiceMenu()

menu = get_voice_menu()

# Function to detect project type
def detect_project_type(project_path, entry_point):
    """Detect the type of project based on its entry point"""
    try:
        with open(os.path.join(project_path, entry_point), 'r', encoding='utf-8') as f:
            content = f.read().lower()
            
        if 'import streamlit' in content or 'st.' in content:
            return "streamlit"
        elif 'import flask' in content or 'from flask' in content:
            return "flask"
        elif 'import django' in content or 'from django' in content:
            return "django"
        elif 'import gradio' in content or 'gr.' in content:
            return "gradio"
        elif 'import cv2' in content or 'mediapipe' in content:
            return "opencv"
        elif 'import os' in content and 'shutil' in content and 'gradio' in content:
            return "gradio"
        else:
            return "python"
    except:
        return "python"

# Terminal class for real-time project execution
class Terminal:
    def __init__(self):
        self.process = None
        self.output_queue = queue.Queue()
        self.is_running = False
        
    def start_project(self, project_path, entry_point, project_type):
        """Start a project in the terminal"""
        try:
            if project_type == "streamlit":
                cmd = ['streamlit', 'run', entry_point]
            elif project_type == "gradio":
                cmd = ['python', entry_point]
            elif project_type == "flask":
                cmd = ['python', entry_point]
            elif project_type == "django":
                cmd = ['python', 'manage.py', 'runserver']
            elif project_type == "opencv":
                cmd = ['python', entry_point]
            else:
                cmd = ['python', entry_point]
            
            self.process = subprocess.Popen(
                cmd,
                cwd=project_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            self.is_running = True
            
            # Start output monitoring thread
            threading.Thread(target=self._monitor_output, daemon=True).start()
            
            return True, "Project started successfully!"
        except Exception as e:
            error_msg = str(e)
            if "Cannot find empty port" in error_msg or "port" in error_msg.lower():
                return False, f"Port conflict detected: {error_msg}\n\n💡 Try stopping other running projects first, or restart the application."
            else:
                return False, f"Error starting project: {error_msg}"
    
    def _monitor_output(self):
        """Monitor process output in a separate thread"""
        try:
            for line in iter(self.process.stdout.readline, ''):
                if line:
                    self.output_queue.put(line.strip())
        except:
            pass
        finally:
            self.is_running = False
    
    def get_output(self):
        """Get all available output"""
        output = []
        while not self.output_queue.empty():
            output.append(self.output_queue.get_nowait())
        return output
    
    def stop_project(self):
        """Stop the running project"""
        if self.process and self.is_running:
            self.process.terminate()
            self.is_running = False
            return True
        return False

# Global terminal instance
if 'terminal' not in st.session_state:
    st.session_state.terminal = Terminal()

def check_port_conflicts():
    """Check for common port conflicts"""
    import socket
    
    common_ports = {
        7860: "Gradio (default)",
        7861: "Gradio (alternative)",
        7862: "File Manager",
        7864: "New_genAI (Streamlit)",
        8501: "Streamlit (default)",
        8502: "Streamlit (alternative)"
    }
    
    conflicts = []
    for port, service in common_ports.items():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            if result == 0:
                conflicts.append(f"Port {port} ({service})")
        except:
            pass
    
    return conflicts

# Function to execute project and capture output
def execute_project(project_path, entry_point):
    """Execute a project and return its output"""
    try:
        import subprocess
        import sys
        
        # Detect project type
        project_type = detect_project_type(project_path, entry_point)
        
        if project_type == "streamlit":
            # For Streamlit apps, we'll provide instructions instead of running
            return [
                "🌐 This is a Streamlit web application!",
                "",
                "📋 To run this project:",
                f"1. Open terminal/command prompt",
                f"2. Navigate to: {project_path}",
                f"3. Run: streamlit run {entry_point}",
                "",
                "🚀 The app will open in your browser automatically!",
                "",
                "💡 Alternative: You can also run it from the project folder directly."
            ], 0
            
        elif project_type == "flask":
            # For Flask apps
            result = subprocess.run(
                [sys.executable, entry_point],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=30
            )
        elif project_type == "django":
            # For Django apps
            result = subprocess.run(
                [sys.executable, 'manage.py', 'runserver'],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=30
            )
        else:
            # Regular Python script
            result = subprocess.run(
                [sys.executable, entry_point],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=30
            )
        
        output_lines = []
        if result.stdout:
            output_lines.extend(result.stdout.strip().split('\n'))
        if result.stderr:
            output_lines.extend([f"ERROR: {line}" for line in result.stderr.strip().split('\n')])
        
        return output_lines, result.returncode
    except subprocess.TimeoutExpired:
        return ["⏰ Project execution timed out after 30 seconds"], 1
    except Exception as e:
        return [f"❌ Error executing project: {str(e)}"], 1

# Main title and description
st.title("🎤 Voice Menu Assistant")
st.markdown("---")

# Display available commands
st.subheader("🎯 Available Commands")
st.markdown("**Voice commands you can use:**")

# Create a grid layout for commands
command_cols = st.columns(2)

# Group commands by category
basic_commands = ["help", "exit", "log"]
project_commands = ["list_projects", "open_project", "run_project"]
system_commands = ["send_whatsapp", "ssh_login", "open_notepad", "open_jupyter", "open_calculator", "open_paint", "open_explorer", "open_cmd", "open_task_manager", "google_search"]
window_commands = ["minimize_all", "minimize", "maximize", "close_window"]

# Function to create command card
def create_command_card(name, description, category, col_index, cmd_index):
    with col_index:
        # Choose color based on category
        if category == "basic":
            gradient = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
        elif category == "project":
            gradient = "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
        elif category == "system":
            gradient = "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"
        else:  # window
            gradient = "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)"
        
        st.markdown(f"""
        <div style="
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            background: {gradient};
            color: white;
            text-align: center;
            cursor: pointer;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        ">
            <h4>🎤 {name.replace('_', ' ').title()}</h4>
            <p style="font-size: 12px; margin: 5px 0;">{description}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Add test button with unique key
        if st.button(f"🎯 Test '{name.replace('_', ' ')}'", key=f"test_{name}_{cmd_index}", use_container_width=True):
            st.session_state.text_input = name.replace('_', ' ')
            st.rerun()

# Display commands in categories
with command_cols[0]:
    st.markdown("**🔧 Basic Commands**")
    for i, cmd in enumerate(basic_commands):
        if cmd in menu.commands:
            create_command_card(cmd, menu.commands[cmd][1], "basic", command_cols[0], i)
    
    st.markdown("**🚀 Project Commands**")
    for i, cmd in enumerate(project_commands):
        if cmd in menu.commands:
            create_command_card(cmd, menu.commands[cmd][1], "project", command_cols[0], i + 100)

with command_cols[1]:
    st.markdown("**💻 System Commands**")
    for i, cmd in enumerate(system_commands):
        if cmd in menu.commands:
            create_command_card(cmd, menu.commands[cmd][1], "system", command_cols[1], i + 200)
    
    st.markdown("**🪟 Window Commands**")
    for i, cmd in enumerate(window_commands):
        if cmd in menu.commands:
            create_command_card(cmd, menu.commands[cmd][1], "window", command_cols[1], i + 300)

st.markdown("---")

# Quick Command Tester
st.subheader("⚡ Quick Command Tester")
st.markdown("**Test any command instantly:**")

# Create a row for quick testing
test_col1, test_col2, test_col3, test_col4 = st.columns(4)

with test_col1:
    if st.button("🎤 Test Voice Recognition", key="quick_test_voice", use_container_width=True):
        st.session_state.text_input = "help"
        st.rerun()

with test_col2:
    if st.button("📊 View Logs", key="quick_test_logs", use_container_width=True):
        st.session_state.text_input = "log"
        st.rerun()

with test_col3:
    if st.button("📋 List Projects", key="quick_test_projects", use_container_width=True):
        st.session_state.text_input = "list projects"
        st.rerun()

with test_col4:
    if st.button("🔍 Google Search", key="quick_test_search", use_container_width=True):
        st.session_state.text_input = "search for python tutorials"
        st.rerun()

st.markdown("---")

# Projects Section
st.subheader("🚀 Available Projects for Testing")
st.markdown("**Click on any project to run it:**")

# Get projects list
try:
    projects = menu.get_projects_list()
    st.success(f"✅ Projects loaded successfully! Found {len(projects)} projects")
    # Debug: Show projects info
    if st.checkbox("🐛 Show Debug Info", key="debug_projects"):
        st.write("Projects found:", list(projects.keys()))
        for name, info in projects.items():
            st.write(f"- {name}: {info}")
except AttributeError as e:
    st.error(f"❌ AttributeError: {e}")
    st.write("Available methods:", [method for method in dir(menu) if not method.startswith('_')])
    # Try to clear cache and reload
    if st.button("🔄 Clear Cache and Reload", key="clear_cache_reload"):
        st.cache_resource.clear()
        st.rerun()
    projects = {}
except Exception as e:
    st.error(f"❌ Unexpected error: {e}")
    projects = {}

if projects:
    # Display projects as clickable cards
    st.markdown("**Click any project to run it directly on this page:**")
    
    # Create a grid layout for projects
    cols = st.columns(2)
    
    for i, (name, info) in enumerate(projects.items()):
        with cols[i % 2]:
            with st.container():
                st.markdown(f"""
                <div style="
                    border: 2px solid #e0e0e0;
                    border-radius: 10px;
                    padding: 15px;
                    margin: 10px 0;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    text-align: center;
                    cursor: pointer;
                ">
                    <h3>🚀 {name}</h3>
                    <p>{info['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Run button for each project
                if st.button(f"▶️ Run {name}", key=f"run_{name}", use_container_width=True):
                    st.session_state.selected_project = name
                    st.session_state.run_project_directly = True
                    st.rerun()
    
    # Show project execution interface
    if 'selected_project' in st.session_state and st.session_state.get('run_project_directly', False):
        selected = st.session_state.selected_project
        if selected in projects:
            st.markdown("---")
            st.subheader(f"🚀 Running: {selected}")
            
            # Check for entry points first - including project-specific files
            entry_points = [
                'app.py', 'main.py', 'run.py', 'start.py',
                'file_manager.py', 'ui_gradio.py', 'hand_gesture_control.py',
                'gemini_api.py'
            ]
            
            # Add project-specific entry points based on project name
            if selected == "file_handling":
                entry_points.insert(0, 'app.py')
            elif selected == "New_genAI":
                entry_points.insert(0, 'app.py')
            elif selected == "Hand_power":
                entry_points.insert(0, 'hand_gesture_control.py')
            elif selected == "Resume maker":
                entry_points.insert(0, 'app.py')
            
            found_entries = []
            for entry in entry_points:
                entry_path = os.path.join(projects[selected]['path'], entry)
                if os.path.exists(entry_path):
                    found_entries.append(entry)
            
            # Project info
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**Project:** {selected}")
                st.write(f"**Description:** {projects[selected]['description']}")
                st.write(f"**Path:** `{projects[selected]['path']}`")
                
                # Show project type
                if found_entries:
                    project_type = detect_project_type(projects[selected]['path'], found_entries[0])
                    type_icons = {
                        "streamlit": "🌐",
                        "gradio": "🎨", 
                        "opencv": "📷",
                        "python": "🐍",
                        "flask": "🍃",
                        "django": "🐘"
                    }
                    icon = type_icons.get(project_type, "📁")
                    st.write(f"**Type:** {icon} {project_type.title()}")
            
            with col2:
                if found_entries:
                    st.success(f"✅ Entry point found: {', '.join(found_entries)}")
                    
                    # Check for requirements.txt
                    req_path = os.path.join(projects[selected]['path'], 'requirements.txt')
                    if os.path.exists(req_path):
                        st.info("📦 Requirements.txt found")
                else:
                    st.warning("⚠️ No entry point found")
            
            # Project execution section
            st.markdown("### 🎯 Project Execution")
            
            # Check if project is already running
            if 'project_running' not in st.session_state:
                st.session_state.project_running = False
            
            if not st.session_state.project_running:
                if st.button("🚀 Start Project", key="start_project", type="primary"):
                    st.session_state.project_running = True
                    st.session_state.project_output = []
                    
                    # Start project in terminal
                    if found_entries:
                        entry_point = found_entries[0]
                        project_type = detect_project_type(projects[selected]['path'], entry_point)
                        
                        # Add execution info
                        st.session_state.project_output = [
                            f"🚀 Starting {selected}...",
                            f"📁 Working directory: {projects[selected]['path']}",
                            f"🔍 Entry point: {entry_point}",
                            f"🎯 Project type: {project_type}",
                            f"⚡ Starting terminal execution...",
                            f"🕒 Started at: {time.strftime('%H:%M:%S')}",
                            "---"
                        ]
                        
                        # Start the project in terminal
                        success, message = st.session_state.terminal.start_project(
                            projects[selected]['path'], 
                            entry_point, 
                            project_type
                        )
                        
                        if success:
                            st.session_state.project_output.append(f"✅ {message}")
                        else:
                            st.session_state.project_output.append(f"❌ {message}")
                            # Add helpful guidance for port conflicts
                            if "port" in message.lower() or "conflict" in message.lower():
                                st.session_state.project_output.append("💡 **Port Conflict Solution:**")
                                st.session_state.project_output.append("1. Stop other running projects")
                                st.session_state.project_output.append("2. Check sidebar for port conflicts")
                                st.session_state.project_output.append("3. Restart the application if needed")
                                st.session_state.project_output.append("4. Try running the project again")
                    else:
                        # Try to find any Python file with main function
                        import glob
                        python_files = glob.glob(os.path.join(projects[selected]['path'], "*.py"))
                        main_files = []
                        
                        for py_file in python_files:
                            try:
                                with open(py_file, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                    if 'if __name__ == "__main__"' in content:
                                        main_files.append(os.path.basename(py_file))
                            except:
                                continue
                        
                        if main_files:
                            st.session_state.project_output = [
                                f"🔍 Found Python files with main functions: {', '.join(main_files)}",
                                f"📁 Project path: {projects[selected]['path']}",
                                f"💡 You can run any of these files manually"
                            ]
                        else:
                            st.session_state.project_output = [
                                f"❌ No entry point found for {selected}",
                                f"📁 Project path: {projects[selected]['path']}",
                                f"🔍 Looking for: app.py, main.py, run.py, start.py, file_manager.py, ui_gradio.py, hand_gesture_control.py"
                            ]
                    
                    st.rerun()
            else:
                # Show running status
                if st.session_state.terminal.is_running:
                    st.success("🟢 Project is running in terminal...")
                else:
                    st.info("ℹ️ Project execution completed")
                
                # Display project output
                if 'project_output' not in st.session_state:
                    st.session_state.project_output = []
                
                # Get real-time output from terminal
                if st.session_state.terminal.is_running:
                    new_output = st.session_state.terminal.get_output()
                    if new_output:
                        # Filter out common TensorFlow and AI library info messages
                        filtered_output = []
                        camera_error_count = 0
                        for line in new_output:
                            # Skip TensorFlow oneDNN messages
                            if "oneDNN custom operations" in line or "TF_ENABLE_ONEDNN_OPTS" in line:
                                continue
                            # Skip other common TensorFlow info messages
                            elif "tensorflow/core/util/port.cc" in line:
                                continue
                            # Skip MediaPipe info messages
                            elif "MediaPipe" in line and "INFO" in line:
                                continue
                            # Skip OpenCV info messages
                            elif "opencv" in line.lower() and "info" in line.lower():
                                continue
                            # Handle camera error messages
                            elif "Failed to read from webcam" in line:
                                camera_error_count += 1
                                if camera_error_count <= 3:  # Show first 3 errors only
                                    filtered_output.append("📷 Camera access error - check camera connection")
                                continue
                            elif "webcam" in line.lower() and "error" in line.lower():
                                camera_error_count += 1
                                if camera_error_count <= 3:  # Show first 3 errors only
                                    filtered_output.append("📷 Camera error detected")
                                continue
                            else:
                                filtered_output.append(line)
                        
                        st.session_state.project_output.extend(filtered_output)
                        
                        # Add info about filtered messages if any were filtered
                        if len(new_output) > len(filtered_output):
                            filtered_count = len(new_output) - len(filtered_output)
                            st.session_state.project_output.append(f"ℹ️ Filtered {filtered_count} TensorFlow/AI library info messages")
                        
                        # Check for camera errors with user authority
                        if project_type == "opencv" and camera_error_count > 10:
                            if 'camera_warning_shown' not in st.session_state:
                                st.session_state.camera_warning_shown = True
                                st.session_state.project_output.append("⚠️ Multiple camera errors detected")
                                st.session_state.project_output.append("💡 Use Camera Control dropdown to manage camera")
                                st.session_state.project_output.append("🔄 Camera will continue trying to connect...")
                            
                            # Check if auto-stop is enabled
                            auto_stop_enabled = st.session_state.get('auto_stop_camera', False)
                            if auto_stop_enabled:
                                error_threshold = st.session_state.get('error_threshold', 20)
                                if camera_error_count > error_threshold:
                                    st.session_state.terminal.stop_project()
                                    st.session_state.project_output.append(f"🛑 Auto-stopped after {error_threshold} camera errors")
                                    st.session_state.project_output.append("💡 You can restart the camera when ready")
                
                # Display output
                st.markdown("### 📄 Terminal Output:")
                output_container = st.container()
                with output_container:
                    for i, output_line in enumerate(st.session_state.project_output):
                        if output_line.startswith("ERROR:"):
                            st.error(output_line)
                        elif output_line.startswith("✅"):
                            st.success(output_line)
                        elif output_line.startswith("⚠️"):
                            st.warning(output_line)
                        elif output_line.startswith("❌"):
                            st.error(output_line)
                        elif output_line == "---":
                            st.markdown("---")
                        elif "streamlit" in output_line.lower():
                            st.info(f"🌐 {output_line}")
                        elif "gradio" in output_line.lower():
                            st.info(f"🎨 {output_line}")
                        elif "opencv" in output_line.lower() or "cv2" in output_line.lower():
                            st.info(f"📷 {output_line}")
                        elif "mediapipe" in output_line.lower():
                            st.info(f"🤚 {output_line}")
                        elif "gemini" in output_line.lower() or "google" in output_line.lower():
                            st.info(f"🤖 {output_line}")
                        elif "file" in output_line.lower() and "manager" in output_line.lower():
                            st.info(f"📁 {output_line}")
                        elif "tensorflow" in output_line.lower() or "onednn" in output_line.lower():
                            # Filter out TensorFlow info messages
                            if "oneDNN custom operations" in output_line or "TF_ENABLE_ONEDNN_OPTS" in output_line:
                                continue  # Skip these TensorFlow info messages
                            else:
                                st.info(f"🤖 {output_line}")
                        elif "running" in output_line.lower() or "server" in output_line.lower():
                            st.success(f"🚀 {output_line}")
                        elif "error" in output_line.lower() and not "tensorflow" in output_line.lower():
                            st.error(f"❌ {output_line}")
                        elif "warning" in output_line.lower() and not "tensorflow" in output_line.lower():
                            st.warning(f"⚠️ {output_line}")
                        elif "success" in output_line.lower() or "opened" in output_line.lower():
                            st.success(f"✅ {output_line}")
                        else:
                            st.text(f"[{i+1}] {output_line}")
                
                # Auto-refresh for running projects
                if st.session_state.terminal.is_running:
                    time.sleep(0.5)  # Small delay for real-time updates
                    st.rerun()
                
                # Action buttons based on project type
                project_type = detect_project_type(projects[selected]['path'], found_entries[0]) if found_entries else "unknown"
                
                if project_type == "opencv":
                    # Special controls for camera-based projects
                    col1, col2, col3, col4, col5 = st.columns(5)
                    
                    with col1:
                        if st.button("🔄 Run Again", key="run_again"):
                            # Stop current process if running
                            if st.session_state.terminal.is_running:
                                st.session_state.terminal.stop_project()
                            st.session_state.project_running = False
                            st.rerun()
                    
                    with col2:
                        if st.button("📁 Open Folder", key="open_folder"):
                            import subprocess
                            try:
                                subprocess.run(['explorer', projects[selected]['path']], shell=True)
                                st.success("📁 Project folder opened!")
                            except:
                                st.error("❌ Could not open folder")
                    
                    with col3:
                        # Camera control dropdown
                        camera_action = st.selectbox(
                            "📷 Camera Control:",
                            ["🔄 Keep Running", "⏸️ Pause Camera", "📷 Stop Camera", "🔄 Restart Camera"],
                            key="camera_control"
                        )
                        
                        if camera_action == "⏸️ Pause Camera":
                            st.info("⏸️ Camera paused - will resume automatically")
                        elif camera_action == "📷 Stop Camera":
                            if st.session_state.terminal.is_running:
                                st.session_state.terminal.stop_project()
                                st.success("📷 Camera stopped by user!")
                                st.rerun()
                        elif camera_action == "🔄 Restart Camera":
                            if st.session_state.terminal.is_running:
                                st.session_state.terminal.stop_project()
                            st.session_state.project_running = False
                            st.rerun()
                    
                    with col4:
                        if st.button("⏹️ Stop Project", key="stop_project", type="secondary"):
                            if st.session_state.terminal.is_running:
                                st.session_state.terminal.stop_project()
                                st.success("⏹️ Project stopped!")
                            st.rerun()
                    
                    with col5:
                        if st.button("🔙 Back to Projects", key="back_to_projects"):
                            # Stop current process if running
                            if st.session_state.terminal.is_running:
                                st.session_state.terminal.stop_project()
                            st.session_state.project_running = False
                            st.session_state.run_project_directly = False
                            if 'selected_project' in st.session_state:
                                del st.session_state.selected_project
                            if 'project_output' in st.session_state:
                                del st.session_state.project_output
                            st.rerun()
                else:
                    # Standard controls for non-camera projects
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        if st.button("🔄 Run Again", key="run_again"):
                            # Stop current process if running
                            if st.session_state.terminal.is_running:
                                st.session_state.terminal.stop_project()
                            st.session_state.project_running = False
                            st.rerun()
                    
                    with col2:
                        if st.button("📁 Open Folder", key="open_folder"):
                            import subprocess
                            try:
                                subprocess.run(['explorer', projects[selected]['path']], shell=True)
                                st.success("📁 Project folder opened!")
                            except:
                                st.error("❌ Could not open folder")
                    
                    with col3:
                        if st.button("⏹️ Stop Project", key="stop_project", type="secondary"):
                            if st.session_state.terminal.is_running:
                                st.session_state.terminal.stop_project()
                                st.success("⏹️ Project stopped!")
                            st.rerun()
                    
                    with col4:
                        if st.button("🔙 Back to Projects", key="back_to_projects"):
                            # Stop current process if running
                            if st.session_state.terminal.is_running:
                                st.session_state.terminal.stop_project()
                            st.session_state.project_running = False
                            st.session_state.run_project_directly = False
                            if 'selected_project' in st.session_state:
                                del st.session_state.selected_project
                            if 'project_output' in st.session_state:
                                del st.session_state.project_output
                            st.rerun()
                
                # Special instructions for different project types
                project_type = detect_project_type(projects[selected]['path'], found_entries[0]) if found_entries else "unknown"
                
                if project_type == "streamlit":
                    st.markdown("---")
                    st.info("""
                    **🌐 Streamlit Web Application!**
                    
                    This is a Streamlit web application. It will:
                    1. Start a local web server
                    2. Open automatically in your browser
                    3. Show the web interface
                    
                    💡 The app is now running and accessible in your browser!
                    """)
                
                elif project_type == "gradio":
                    st.markdown("---")
                    st.info("""
                    **🎨 Gradio Web Application!**
                    
                    This is a Gradio web application. It will:
                    1. Start a local web server
                    2. Open automatically in your browser
                    3. Show the interactive interface
                    
                    💡 The app is now running and accessible in your browser!
                    """)
                
                elif project_type == "opencv":
                    st.markdown("---")
                    
                    # Camera status and user authority panel
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Camera status indicator
                        if st.session_state.terminal.is_running:
                            st.success("🟢 Camera is running")
                        else:
                            st.info("⚪ Camera is stopped")
                        
                        # Camera error count
                        camera_errors = sum(1 for line in st.session_state.project_output if "camera" in line.lower() and "error" in line.lower())
                        if camera_errors > 0:
                            st.warning(f"⚠️ {camera_errors} camera errors detected")
                    
                    with col2:
                        # User authority controls
                        st.markdown("**🎮 User Authority Controls:**")
                        
                        # Auto-stop toggle
                        auto_stop = st.checkbox(
                            "🛑 Enable auto-stop on errors",
                            value=False,
                            key="auto_stop_camera",
                            help="Automatically stop camera if too many errors occur"
                        )
                        
                        # Error threshold
                        if auto_stop:
                            error_threshold = st.slider(
                                "Error threshold:",
                                min_value=5,
                                max_value=50,
                                value=20,
                                key="error_threshold",
                                help="Number of errors before auto-stop"
                            )
                    
                    # Camera status warning
                    if any("camera" in line.lower() and "error" in line.lower() for line in st.session_state.project_output):
                        st.error("""
                        **📷 Camera Access Issue Detected!**
                        
                        The application is having trouble accessing your camera:
                        1. **Check camera connection** - Make sure camera is connected
                        2. **Check permissions** - Allow camera access if prompted
                        3. **Close other apps** - Other apps might be using the camera
                        4. **Use Camera Control dropdown** - You have full control over camera
                        
                        💡 You can choose to keep trying or stop the camera manually
                        """)
                    else:
                        st.info("""
                        **📷 OpenCV Application!**
                        
                        This is a computer vision application. It will:
                        1. Access your camera
                        2. Process video in real-time
                        3. Detect hand gestures
                        
                        💡 Make sure your camera is connected and accessible!
                        """)
                
                elif project_type == "python":
                    st.markdown("---")
                    st.info("""
                    **🐍 Python Application!**
                    
                    This is a Python script. It will:
                    1. Execute the script
                    2. Show output in the terminal
                    3. Perform file operations
                    
                    💡 Check the terminal output for results!
                    """)
                

else:
    st.warning("No projects found in the current directory.")

st.markdown("---")

# Create two columns for input methods
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Text Input")
    text_command = st.text_input(
        "Type your command here",
        placeholder="e.g. 1, open notepad, log, help",
        key="text_input"
    )

with col2:
    st.subheader("🎙️ Voice Input")
    audio_file = st.file_uploader(
        "Upload an audio file with your command",
        type=['wav', 'mp3', 'm4a', 'ogg'],
        key="audio_upload"
    )

# Log password input
st.subheader("🔐 Log Access")
log_password = st.text_input(
    "Log Password (for 'log' command)",
    type="password",
    placeholder="Enter password to view logs",
    key="log_password"
)

# Submit button
if st.button("🚀 Submit Command", type="primary", use_container_width=True):
    # Determine which input to use
    if text_command and text_command.strip():
        command = text_command.strip()
        input_type = "text"
    elif audio_file is not None:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            tmp_file.write(audio_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # Transcribe the audio
        command = menu.transcribe_audio_file(tmp_file_path)
        
        # Clean up temporary file
        os.unlink(tmp_file_path)
        
        if not command:
            st.error("❌ Could not understand audio. Please try again.")
            st.stop()
        input_type = "voice"
    else:
        st.warning("⚠️ Please enter or speak a command.")
        st.stop()
    
    # Process the command
    st.subheader("🤖 Assistant Response")
    
    with st.spinner("Processing your command..."):
        if menu.match_command(command) == "help":
            result = '\n'.join([f"{i+1}. {k.replace('_',' ')}: {menu.commands[k][1]}" for i, k in enumerate(menu.command_keys)])
        else:
            result = menu.run_command(command, log_password=log_password)
    
    # Display result
    if input_type == "voice":
        st.info(f"🎙️ You said: '{command}'")
    
    # Check if it's a project launch
    if "🚀 Successfully launched" in result:
        st.success("✅ Project launched successfully!")
        st.balloons()
    elif "❌ Error" in result:
        st.error("❌ Error occurred!")
    else:
        st.success("✅ Command processed successfully!")
    
    st.text_area("📄 Output:", value=result, height=300, disabled=True)

# Sidebar with additional information
with st.sidebar:
    st.header("🎯 Voice Menu Assistant")
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    ">
        <h4>🎤 Voice Control</h4>
        <p>Control your system with voice commands!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("📋 How to Use")
    st.markdown("""
    **1. Text Input:** Type commands directly
    **2. Voice Input:** Upload audio files
    **3. Quick Test:** Use the test buttons
    **4. Projects:** Click to run any project
    
    **Note:** Some commands work only in terminal mode.
    """)
    
    st.header("⚡ Quick Actions")
    
    # Create styled buttons
    if st.button("🎤 Test Voice", key="sidebar_test_voice", use_container_width=True):
        st.session_state.text_input = "help"
        st.rerun()
    
    if st.button("📊 View Logs", key="sidebar_view_logs", use_container_width=True):
        st.session_state.text_input = "log"
        st.rerun()
    
    if st.button("📋 List Projects", key="sidebar_list_projects", use_container_width=True):
        st.session_state.text_input = "list projects"
        st.rerun()
    
    st.header("💻 System Commands")
    st.markdown("**Test system applications:**")
    
    if st.button("📝 Open Notepad", key="sidebar_notepad", use_container_width=True):
        st.session_state.text_input = "open notepad"
        st.rerun()
    
    if st.button("🧮 Open Calculator", key="sidebar_calculator", use_container_width=True):
        st.session_state.text_input = "open calculator"
        st.rerun()
    
    if st.button("🎨 Open Paint", key="sidebar_paint", use_container_width=True):
        st.session_state.text_input = "open paint"
        st.rerun()
    
    if st.button("📁 Open Explorer", key="sidebar_explorer", use_container_width=True):
        st.session_state.text_input = "open explorer"
        st.rerun()
    
    if st.button("🔍 Google Search", key="sidebar_search", use_container_width=True):
        st.session_state.text_input = "search for python tutorials"
        st.rerun()
    
    st.markdown("**Advanced Commands:**")
    
    if st.button("🔐 SSH Login", key="sidebar_ssh", use_container_width=True):
        st.session_state.text_input = "ssh to 192.168.1.1"
        st.rerun()
    
    if st.button("📱 Send WhatsApp", key="sidebar_whatsapp", use_container_width=True):
        st.session_state.text_input = "send whatsapp to +1234567890"
        st.rerun()
    
    st.header("🎨 Command Categories")
    st.markdown("""
    **🔧 Basic:** Help, Exit, Logs
    **🚀 Projects:** List, Open, Run
    **💻 System:** Apps, SSH, WhatsApp
    **🪟 Windows:** Minimize, Maximize, Close
    """)
    
    st.header("🔧 Debug")
    if st.button("🔄 Clear All Cache", key="debug_clear_cache"):
        st.cache_resource.clear()
        st.rerun()
    
    if st.button("🐛 Show Menu Methods", key="debug_show_methods"):
        methods = [method for method in dir(menu) if not method.startswith('_')]
        st.write("Available methods:", methods)
    
    # Check for port conflicts
    port_conflicts = check_port_conflicts()
    if port_conflicts:
        st.header("⚠️ Port Conflicts")
        st.warning("Ports in use:")
        for conflict in port_conflicts:
            st.write(f"• {conflict}")
        st.info("💡 Stop other projects or restart app.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Voice Menu Assistant - Powered by Streamlit</p>
</div>
""", unsafe_allow_html=True) 