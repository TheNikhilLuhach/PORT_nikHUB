import os
import shutil
import gradio as gr
from datetime import datetime

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

def file_manager_interface():
    with gr.Blocks(title="File Manager") as interface:
        gr.Markdown("# File Manager")
        
        with gr.Tab("Directory Viewer"):
            directory_input = gr.Textbox(
                label="Enter Directory Path",
                placeholder="e.g., C:/Users/YourName/Documents"
            )
            directory_output = gr.Textbox(
                label="Directory Contents",
                lines=20,
                show_copy_button=True
            )
            browse_btn = gr.Button("View Directory")
            browse_btn.click(
                get_directory_contents,
                inputs=directory_input,
                outputs=directory_output
            )
        
        with gr.Tab("Rename File"):
            rename_dir = gr.Textbox(
                label="Directory Path",
                placeholder="e.g., C:/Users/YourName/Documents"
            )
            old_name = gr.Textbox(
                label="Current File Name",
                placeholder="e.g., oldfile.txt"
            )
            new_name = gr.Textbox(
                label="New File Name",
                placeholder="e.g., newfile.txt"
            )
            rename_output = gr.Textbox(label="Status")
            rename_btn = gr.Button("Rename File")
            rename_btn.click(
                rename_file,
                inputs=[rename_dir, old_name, new_name],
                outputs=rename_output
            )
        
        with gr.Tab("Delete File"):
            delete_dir = gr.Textbox(
                label="Directory Path",
                placeholder="e.g., C:/Users/YourName/Documents"
            )
            delete_filename = gr.Textbox(
                label="File Name to Delete",
                placeholder="e.g., file.txt"
            )
            delete_output = gr.Textbox(label="Status")
            delete_btn = gr.Button("Delete File")
            delete_btn.click(
                delete_file,
                inputs=[delete_dir, delete_filename],
                outputs=delete_output
            )
        
        with gr.Tab("Create Directory"):
            create_dir_path = gr.Textbox(
                label="Parent Directory Path",
                placeholder="e.g., C:/Users/YourName/Documents"
            )
            folder_name = gr.Textbox(
                label="New Folder Name",
                placeholder="e.g., newfolder"
            )
            create_output = gr.Textbox(label="Status")
            create_btn = gr.Button("Create Directory")
            create_btn.click(
                create_dir,
                inputs=[create_dir_path, folder_name],
                outputs=create_output
            )
        
        with gr.Tab("View File Content"):
            view_dir = gr.Textbox(
                label="Directory Path",
                placeholder="e.g., C:/Users/YourName/Documents"
            )
            view_filename = gr.Textbox(
                label="File Name",
                placeholder="e.g., file.txt"
            )
            view_output = gr.Textbox(
                label="File Content",
                lines=10,
                show_copy_button=True
            )
            view_btn = gr.Button("View File")
            view_btn.click(
                read_file_content,
                inputs=[view_dir, view_filename],
                outputs=view_output
            )
    
    return interface

if __name__ == "__main__":
    interface = file_manager_interface()
    interface.launch(share=False, server_name="0.0.0.0", server_port=7862) 