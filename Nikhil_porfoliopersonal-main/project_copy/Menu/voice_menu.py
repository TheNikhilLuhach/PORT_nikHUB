import speech_recognition as sr
import pyttsx3
import pywhatkit
import paramiko
import os
import subprocess
import sys
import time
import webbrowser
import pyautogui
import win32gui
import win32con
from colorama import init, Fore, Style
import msvcrt
import logging
from functools import wraps
from dotenv import load_dotenv

init()
load_dotenv()
logging.basicConfig(filename='voice_menu.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_and_time(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        start = time.time()
        try:
            result = func(self, *args, **kwargs)
            logging.info(f"{func.__name__} | Args: {args} | Time: {time.time()-start:.2f}s")
            return result
        except Exception as e:
            logging.error(f"{func.__name__} | Error: {e}")
            print(f"Error: {e}")
    return wrapper

class VoiceMenu:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.assistant_name = "Alexa"
        self.command_keys = [
            "send_whatsapp", "ssh_login", "open_notepad", "open_jupyter", "google_search",
            "open_calculator", "open_paint", "open_explorer", "open_cmd", "open_task_manager",
            "minimize_all", "minimize", "maximize", "close_window", "help", "exit", "log",
            "list_projects", "open_project", "run_project"
        ]
        # Assign numbers to commands in the dictionary
        self.commands = {}
        for idx, key in enumerate(self.command_keys, 1):
            if key == "send_whatsapp":
                variations = ["send whatsapp", "send message", "whatsapp message", "send a message", "whatsapp", "send msg", "message bhejo", "message send", "whatsapp bhejo", "whatsapp to", "send to"]
            elif key == "ssh_login":
                variations = ["ssh login", "login ssh", "connect ssh", "remote login", "ssh connect", "remote connect", "connect system", "ssh", "ssh to", "connect to", "remote access"]
            elif key == "open_notepad":
                variations = ["open notepad", "start notepad", "launch notepad", "notepad open", "note pad", "notes", "open notes", "start notes", "notepad"]
            elif key == "open_jupyter":
                variations = ["open jupyter", "start jupyter", "launch jupyter", "jupyter notebook", "jupyter", "notebook", "python notebook", "start notebook"]
            elif key == "open_calculator":
                variations = ["open calculator", "start calculator", "launch calculator", "calc", "calculator", "open calc", "start calc"]
            elif key == "open_paint":
                variations = ["open paint", "start paint", "launch paint", "mspaint", "paint", "open mspaint", "start mspaint"]
            elif key == "open_explorer":
                variations = ["open explorer", "start explorer", "launch explorer", "file explorer", "explorer", "open file explorer", "start file explorer"]
            elif key == "open_cmd":
                variations = ["open cmd", "start cmd", "launch cmd", "command prompt", "cmd", "open command prompt", "start command prompt"]
            elif key == "open_task_manager":
                variations = ["open task manager", "start task manager", "launch task manager", "task manager", "open taskmgr", "start taskmgr"]
            elif key == "google_search":
                variations = ["google search", "search google", "search for", "google it", "search", "find", "look for", "google", "search karo"]
            elif key == "minimize_all":
                variations = ["minimize all", "minimize windows", "hide all windows", "hide windows", "minimize sab", "sab minimize", "hide all"]
            elif key == "minimize":
                variations = ["minimize", "minimize window", "window minimize", "chota karo", "minimize karo"]
            elif key == "maximize":
                variations = ["maximize", "maximize window", "window maximize", "bada karo", "maximize karo"]
            elif key == "close_window":
                variations = ["close window", "close current window", "band karo", "window band", "close", "band", "window close", "close karo"]
            elif key == "help":
                variations = ["help", "show help", "what can you do", "commands", "help me", "show commands", "guide", "help karo", "commands dikhao"]
            elif key == "exit":
                variations = ["exit", "quit", "close", "band karo", "bye bye", "goodbye", "quit karo", "band kar do", "exit karo", "bye"]
            elif key == "log":
                variations = ["log", "show log", "logs", "view log", "log file"]
            elif key == "list_projects":
                variations = ["list projects", "show projects", "projects", "my projects", "project list", "list my projects", "show my projects"]
            elif key == "open_project":
                variations = ["open project", "open a project", "project open", "open my project", "access project"]
            elif key == "run_project":
                variations = ["run project", "run a project", "project run", "start project", "launch project", "execute project"]
            self.commands[key] = [str(idx)] + variations

    def speak(self, text):
        print(f"{self.assistant_name}: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                command = self.recognizer.recognize_google(audio)
                print(f"You said: {command}")
                return command.lower()
            except:
                return None

    def get_command(self):
        print("Press 'T' to type or speak your command...")
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8').lower()
                if key == 't':
                    return input("Type your command: ").lower()
            command = self.listen()
            if command:
                return command

    def show_help(self):
        print("Available Commands:")
        for idx, key in enumerate(self.command_keys, 1):
            print(f"{idx}. {key.replace('_', ' ')}: {self.commands[key][1]}")

    def match_command(self, command):
        command = command.strip()
        # Match by number string or by text
        for key, variations in self.commands.items():
            if command in variations:
                return key
        return None

    @log_and_time
    def ssh_login(self, ip=None, user=None, password=None, command=None):
        """SSH login with support for web mode"""
        try:
            # Get credentials if not provided
            if ip is None:
                ip = input("Enter SSH IP: ")
            if user is None:
                user = input("Enter SSH username: ")
            if password is None:
                password = os.getenv('SSH_PASSWORD')
                if not password:
                    return "❌ SSH password not found in .env file"
            
            # Connect to SSH
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, username=user, password=password, timeout=10)
            
            if command:
                # Execute single command and return result
                stdin, stdout, stderr = ssh.exec_command(command)
                output = stdout.read().decode()
                error = stderr.read().decode()
                ssh.close()
                
                if error:
                    return f"❌ SSH Error: {error}"
                else:
                    return f"✅ SSH Command Result:\n{output}"
            else:
                # Interactive mode (terminal only)
                result = f"✅ Connected to {ip} as {user}"
                print(result)
                
                while True:
                    cmd = input("Enter Linux command (or 'exit ssh'): ")
                    if 'exit ssh' in cmd:
                        break
                    stdin, stdout, stderr = ssh.exec_command(cmd)
                    output = stdout.read().decode()
                    print(output)
                
                ssh.close()
                return result
                
        except Exception as e:
            return f"❌ SSH error: {e}"

    @log_and_time
    def send_whatsapp(self, phone=None, msg=None):
        """Send WhatsApp message with support for web mode"""
        try:
            if phone is None:
                phone = input("Enter phone number with country code: ")
            if msg is None:
                msg = input("Enter message: ")
            
            pywhatkit.sendwhatmsg_instantly(phone, msg)
            time.sleep(2)
            pyautogui.press('enter')
            return f"✅ WhatsApp message sent to {phone}"
        except Exception as e:
            return f"❌ WhatsApp error: {e}"

    @log_and_time
    def open_application(self, app):
        try:
            if app == "notepad":
                subprocess.Popen("notepad.exe")
                return f"✅ Opened {app}"
            elif app == "jupyter":
                subprocess.Popen(["jupyter", "notebook"])
                return f"✅ Opened {app}"
            elif app == "calculator":
                subprocess.Popen("calc.exe")
                return f"✅ Opened {app}"
            elif app == "paint":
                subprocess.Popen("mspaint.exe")
                return f"✅ Opened {app}"
            elif app == "explorer":
                subprocess.Popen("explorer.exe")
                return f"✅ Opened {app}"
            elif app == "cmd":
                subprocess.Popen("cmd.exe")
                return f"✅ Opened {app}"
            elif app == "task_manager":
                subprocess.Popen("taskmgr.exe")
                return f"✅ Opened {app}"
            else:
                return f"❌ Unknown app: {app}"
        except Exception as e:
            return f"❌ App error: {e}"

    @log_and_time
    def google_search(self, query=None):
        if query is None:
            query = input("What to search for? ")
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            return f"✅ Opened Google search for: {query}"
        except Exception as e:
            return f"❌ Search error: {e}"

    @log_and_time
    def window_management(self, action):
        try:
            if action == "minimize all":
                pyautogui.hotkey('winleft', 'd')
                return f"✅ Minimized all windows"
            elif action == "minimize":
                hwnd = win32gui.GetForegroundWindow()
                win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
                return f"✅ Minimized current window"
            elif action == "maximize":
                hwnd = win32gui.GetForegroundWindow()
                win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                return f"✅ Maximized current window"
            elif action == "close":
                pyautogui.hotkey('alt', 'f4')
                return f"✅ Closed current window"
        except Exception as e:
            return f"❌ Window error: {e}"

    @log_and_time
    def show_log(self):
        pwd = input("Enter log password: ")
        if pwd == "password":
            try:
                with open("voice_menu.log") as f:
                    print(f.read())
            except Exception as e:
                print(f"Log error: {e}")
        else:
            print("Incorrect password.")

    def transcribe_audio_file(self, audio_path):
        try:
            with sr.AudioFile(audio_path) as source:
                audio = self.recognizer.record(source)
            return self.recognizer.recognize_google(audio).lower()
        except Exception as e:
            return None

    def get_projects_list(self):
        """Get list of all available projects"""
        projects = {}
        
        # Check main project directories
        project_dirs = ["projects", "Resume maker", "file_handling"]
        
        for dir_name in project_dirs:
            if os.path.exists(dir_name):
                if dir_name == "projects":
                    # Handle nested projects in projects folder
                    try:
                        for subdir in os.listdir(dir_name):
                            subdir_path = os.path.join(dir_name, subdir)
                            if os.path.isdir(subdir_path):
                                projects[subdir] = {
                                    'path': subdir_path,
                                    'type': 'nested_project',
                                    'description': f"Project in {dir_name}/{subdir}"
                                }
                    except:
                        pass
                else:
                    # Handle direct project directories
                    projects[dir_name] = {
                        'path': dir_name,
                        'type': 'direct_project',
                        'description': f"Project: {dir_name}"
                    }
        
        return projects

    @log_and_time
    def list_projects(self):
        """List all available projects"""
        projects = self.get_projects_list()
        if not projects:
            print("No projects found.")
            return "No projects found."
        
        result = "Available Projects:\n"
        for i, (name, info) in enumerate(projects.items(), 1):
            result += f"{i}. {name} - {info['description']}\n"
        
        print(result)
        return result

    @log_and_time
    def open_project(self):
        """Open a project folder"""
        projects = self.get_projects_list()
        if not projects:
            print("No projects found.")
            return "No projects found."
        
        print("Available Projects:")
        project_list = list(projects.keys())
        for i, name in enumerate(project_list, 1):
            print(f"{i}. {name}")
        
        try:
            choice = input("Enter project number or name: ").strip()
            
            # Try to parse as number
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(project_list):
                    project_name = project_list[idx]
                else:
                    print("Invalid project number.")
                    return "Invalid project number."
            else:
                # Try to match by name
                project_name = choice
                if project_name not in projects:
                    print(f"Project '{choice}' not found.")
                    return f"Project '{choice}' not found."
            
            project_path = projects[project_name]['path']
            os.startfile(project_path)  # Open folder in Windows Explorer
            print(f"Opened project: {project_name}")
            return f"Opened project: {project_name}"
            
        except Exception as e:
            print(f"Error opening project: {e}")
            return f"Error opening project: {e}"

    @log_and_time
    def run_project(self, project_name=None):
        """Run a project"""
        projects = self.get_projects_list()
        if not projects:
            print("No projects found.")
            return "No projects found."
        
        try:
            if project_name:
                # Direct project name provided
                if project_name not in projects:
                    return f"Project '{project_name}' not found."
                choice = project_name
            else:
                # Interactive mode
                print("Available Projects:")
                project_list = list(projects.keys())
                for i, name in enumerate(project_list, 1):
                    print(f"{i}. {name}")
                
                choice = input("Enter project number or name: ").strip()
                
                # Try to parse as number
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(project_list):
                        project_name = project_list[idx]
                    else:
                        print("Invalid project number.")
                        return "Invalid project number."
                else:
                    # Try to match by name
                    project_name = choice
                    if project_name not in projects:
                        print(f"Project '{choice}' not found.")
                        return f"Project '{choice}' not found."
            
            project_path = projects[project_name]['path']
            
            # Check for common entry points
            entry_points = ['app.py', 'main.py', 'run.py', 'start.py']
            found_entry = None
            
            for entry in entry_points:
                entry_path = os.path.join(project_path, entry)
                if os.path.exists(entry_path):
                    found_entry = entry_path
                    break
            
            if found_entry:
                # Run the project in background
                try:
                    process = subprocess.Popen([sys.executable, found_entry], cwd=project_path)
                    print(f"Running project: {project_name}")
                    return f"🚀 Successfully launched {project_name} in background!\nEntry point: {os.path.basename(found_entry)}\nProcess ID: {process.pid}"
                except Exception as e:
                    return f"❌ Error launching {project_name}: {e}"
            else:
                # Just open the folder
                os.startfile(project_path)
                print(f"Opened project folder: {project_name}")
                return f"📁 Opened project folder: {project_name} (no entry point found)"
                
        except Exception as e:
            print(f"Error running project: {e}")
            return f"❌ Error running project: {e}"

    def run(self):
        self.speak(f"Hello! I'm {self.assistant_name}. Say '{self.assistant_name}' to wake me up!")
        self.show_help()
        while True:
            command = self.get_command()
            cmd_key = self.match_command(command)
            if not cmd_key:
                self.speak("Unknown command. Say 'help' to see available commands.")
                continue
            if cmd_key == "help":
                self.show_help()
            elif cmd_key == "exit":
                self.speak("Goodbye!")
                break
            elif cmd_key == "ssh_login":
                self.ssh_login()
            elif cmd_key == "send_whatsapp":
                self.send_whatsapp()
            elif cmd_key == "open_notepad":
                self.open_application("notepad")
            elif cmd_key == "open_jupyter":
                self.open_application("jupyter")
            elif cmd_key == "open_calculator":
                self.open_application("calculator")
            elif cmd_key == "open_paint":
                self.open_application("paint")
            elif cmd_key == "open_explorer":
                self.open_application("explorer")
            elif cmd_key == "open_cmd":
                self.open_application("cmd")
            elif cmd_key == "open_task_manager":
                self.open_application("task_manager")
            elif cmd_key == "google_search":
                self.google_search()
            elif cmd_key == "minimize_all":
                self.window_management("minimize all")
            elif cmd_key == "minimize":
                self.window_management("minimize")
            elif cmd_key == "maximize":
                self.window_management("maximize")
            elif cmd_key == "close_window":
                self.window_management("close")
            elif cmd_key == "log":
                self.show_log()
            elif cmd_key == "list_projects":
                self.list_projects()
            elif cmd_key == "open_project":
                self.open_project()
            elif cmd_key == "run_project":
                self.run_project()

    def run_command(self, command, log_password=None):
        cmd_key = self.match_command(command)
        if not cmd_key:
            return "Unknown command. Say 'help' to see available commands."
        if cmd_key == "help":
            return '\n'.join([f"{i+1}. {k.replace('_',' ')}: {self.commands[k][1]}" for i, k in enumerate(self.command_keys)])
        elif cmd_key == "exit":
            return "Goodbye!"
        elif cmd_key == "ssh_login":
            # Extract SSH details from command if possible
            if "ssh" in command.lower() and "to" in command.lower():
                # Try to extract IP from command like "ssh to 192.168.1.1"
                parts = command.lower().split("to")
                if len(parts) > 1:
                    ip = parts[1].strip()
                    return self.ssh_login(ip=ip)
            return "SSH login requires IP address. Example: 'ssh to 192.168.1.1' or use terminal mode for interactive SSH."
        elif cmd_key == "send_whatsapp":
            # Extract phone and message from command if possible
            if "whatsapp" in command.lower() and "to" in command.lower():
                # Try to extract phone from command like "send whatsapp to +1234567890"
                parts = command.lower().split("to")
                if len(parts) > 1:
                    phone = parts[1].strip()
                    return self.send_whatsapp(phone=phone, msg="Hello from Voice Menu!")
            return "WhatsApp requires phone number. Example: 'send whatsapp to +1234567890' or use terminal mode for custom messages."
        elif cmd_key == "open_notepad":
            return self.open_application("notepad")
        elif cmd_key == "open_jupyter":
            return self.open_application("jupyter")
        elif cmd_key == "open_calculator":
            return self.open_application("calculator")
        elif cmd_key == "open_paint":
            return self.open_application("paint")
        elif cmd_key == "open_explorer":
            return self.open_application("explorer")
        elif cmd_key == "open_cmd":
            return self.open_application("cmd")
        elif cmd_key == "open_task_manager":
            return self.open_application("task_manager")
        elif cmd_key == "google_search":
            # Extract search query from command
            if "search" in command.lower():
                parts = command.lower().split("search")
                if len(parts) > 1 and parts[1].strip():
                    query = parts[1].strip()
                    return self.google_search(query)
            elif "google" in command.lower():
                # Handle "google python tutorials" format
                parts = command.lower().split("google")
                if len(parts) > 1 and parts[1].strip():
                    query = parts[1].strip()
                    return self.google_search(query)
            return "Please specify what to search for. Example: 'search for python tutorials' or 'google python tutorials'"
        elif cmd_key == "minimize_all":
            return self.window_management("minimize all")
        elif cmd_key == "minimize":
            return self.window_management("minimize")
        elif cmd_key == "maximize":
            return self.window_management("maximize")
        elif cmd_key == "close_window":
            return self.window_management("close")
        elif cmd_key == "log":
            if log_password == "password":
                try:
                    with open("voice_menu.log") as f:
                        return f.read()
                except Exception as e:
                    return f"Log error: {e}"
            else:
                return "Incorrect password."
        elif cmd_key == "list_projects":
            return self.list_projects()
        elif cmd_key == "open_project":
            # Extract project name from command if possible
            if "open project" in command.lower():
                parts = command.lower().split("open project")
                if len(parts) > 1 and parts[1].strip():
                    project_name = parts[1].strip()
                    return self.open_project(project_name)
            return "Project opening requires project name. Example: 'open project New_genAI' or use terminal mode for interactive project selection."
        elif cmd_key == "run_project":
            # Check if a specific project name is provided
            if "run project" in command.lower():
                # Extract project name from command
                parts = command.lower().split("run project")
                if len(parts) > 1 and parts[1].strip():
                    project_name = parts[1].strip()
                    return self.run_project(project_name)
            return self.run_project()
        return "Command not supported in web mode."

if __name__ == "__main__":
    VoiceMenu().run() 