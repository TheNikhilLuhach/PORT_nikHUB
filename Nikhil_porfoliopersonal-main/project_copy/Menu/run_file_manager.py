#!/usr/bin/env python3
"""
Script to run the File Manager Streamlit app with proper port management
"""

import subprocess
import sys
import os
import time
import socket

def is_port_available(port):
    """Check if a port is available"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except OSError:
        return False

def find_available_port(start_port=7862, max_attempts=10):
    """Find an available port starting from start_port"""
    for i in range(max_attempts):
        port = start_port + i
        if is_port_available(port):
            return port
    return None

def main():
    print("🚀 Starting File Manager Streamlit App...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("file_handling/app.py"):
        print("❌ Error: app.py not found in file_handling/")
        print("💡 Make sure you're running this from the Menu directory")
        return
    
    # Find an available port
    print("🔍 Checking for available ports...")
    port = find_available_port()
    
    if port is None:
        print("❌ Error: No available ports found")
        return
    
    print(f"✅ Using port {port}")
    
    # Change to the file_handling directory
    os.chdir("file_handling")
    
    # Run the Streamlit app
    print(f"🌐 Starting Streamlit app on port {port}...")
    print(f"📱 The app will be available at: http://localhost:{port}")
    print("=" * 50)
    
    try:
        # Run streamlit with the specified port
        cmd = [sys.executable, "-m", "streamlit", "run", "app.py", 
               "--server.port", str(port),
               "--server.address", "localhost"]
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except Exception as e:
        print(f"❌ Error running app: {e}")

if __name__ == "__main__":
    main() 