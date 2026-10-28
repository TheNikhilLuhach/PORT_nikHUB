#!/usr/bin/env python3
"""
Port Manager Script - Helps resolve port conflicts
"""

import subprocess
import sys
import os

def get_process_info(pid):
    """Get process information by PID"""
    try:
        result = subprocess.run(['tasklist', '/FI', f'PID eq {pid}', '/FO', 'CSV'], 
                              capture_output=True, text=True, shell=True)
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:
            # Parse CSV output
            parts = lines[1].split(',')
            if len(parts) >= 2:
                return parts[0].strip('"'), parts[1].strip('"')
    except:
        pass
    return "Unknown", "Unknown"

def check_port(port):
    """Check what's using a specific port"""
    try:
        result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True, shell=True)
        lines = result.stdout.split('\n')
        
        for line in lines:
            if f':{port}' in line and 'LISTENING' in line:
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    process_name, memory = get_process_info(pid)
                    return pid, process_name, memory
    except:
        pass
    return None, None, None

def kill_process(pid):
    """Kill a process by PID"""
    try:
        subprocess.run(['taskkill', '/PID', pid, '/F'], shell=True)
        return True
    except:
        return False

def main():
    print("🔧 Port Conflict Manager")
    print("=" * 50)
    
    # Check all conflicting ports
    ports_to_check = [7862, 7863, 8501, 8502]
    
    print("📊 Current Port Usage:")
    print("-" * 30)
    
    for port in ports_to_check:
        pid, process_name, memory = check_port(port)
        if pid:
            print(f"🚨 Port {port}: {process_name} (PID: {pid}) - {memory}")
        else:
            print(f"✅ Port {port}: Available")
    
    print("\n" + "=" * 50)
    print("🎯 Available Actions:")
    print("1. Kill all conflicting processes")
    print("2. Kill specific port process")
    print("3. Check port status")
    print("4. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                print("\n🔄 Killing all conflicting processes...")
                killed_count = 0
                for port in ports_to_check:
                    pid, process_name, memory = check_port(port)
                    if pid:
                        if kill_process(pid):
                            print(f"✅ Killed {process_name} (PID: {pid}) on port {port}")
                            killed_count += 1
                        else:
                            print(f"❌ Failed to kill process on port {port}")
                
                print(f"\n🎉 Successfully killed {killed_count} processes!")
                print("💡 You can now run your applications without port conflicts.")
                break
                
            elif choice == "2":
                port = input("Enter port number to kill: ").strip()
                try:
                    port = int(port)
                    pid, process_name, memory = check_port(port)
                    if pid:
                        if kill_process(pid):
                            print(f"✅ Killed {process_name} (PID: {pid}) on port {port}")
                        else:
                            print(f"❌ Failed to kill process on port {port}")
                    else:
                        print(f"ℹ️ No process found on port {port}")
                except ValueError:
                    print("❌ Invalid port number")
                    
            elif choice == "3":
                print("\n📊 Current Port Status:")
                print("-" * 30)
                for port in ports_to_check:
                    pid, process_name, memory = check_port(port)
                    if pid:
                        print(f"🚨 Port {port}: {process_name} (PID: {pid}) - {memory}")
                    else:
                        print(f"✅ Port {port}: Available")
                        
            elif choice == "4":
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1-4.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 