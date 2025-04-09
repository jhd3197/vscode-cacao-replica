"""
Utility functions for the sample project.
"""

import os
import sys
import time
import random
from typing import List, Dict, Any, Optional, Tuple, Union

def generate_id(prefix: str = "", length: int = 8) -> str:
    """Generate a random ID with optional prefix."""
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    random_part = ''.join(random.choice(chars) for _ in range(length))
    return f"{prefix}{random_part}"

def format_time(timestamp: float) -> str:
    """Format a timestamp into a human-readable string."""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

def get_file_info(file_path: str) -> Dict[str, Any]:
    """Get information about a file."""
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    
    stats = os.stat(file_path)
    return {
        "path": file_path,
        "size": stats.st_size,
        "created": format_time(stats.st_ctime),
        "modified": format_time(stats.st_mtime),
        "accessed": format_time(stats.st_atime),
        "is_directory": os.path.isdir(file_path),
        "extension": os.path.splitext(file_path)[1] if not os.path.isdir(file_path) else None
    }

def list_directory(directory: str, recursive: bool = False) -> List[Dict[str, Any]]:
    """List files in a directory, optionally recursively."""
    if not os.path.exists(directory) or not os.path.isdir(directory):
        return [{"error": "Directory not found or not a directory"}]
    
    result = []
    
    if recursive:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                result.append(get_file_info(file_path))
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                result.append(get_file_info(dir_path))
    else:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            result.append(get_file_info(item_path))
    
    return result

def safe_read_file(file_path: str, default: str = "") -> str:
    """Safely read a file with error handling."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
        return default

def safe_write_file(file_path: str, content: str) -> bool:
    """Safely write to a file with error handling."""
    try:
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing to file {file_path}: {str(e)}")
        return False

def get_file_type(file_path: str) -> str:
    """Determine file type based on extension."""
    if os.path.isdir(file_path):
        return "directory"
        
    extension = os.path.splitext(file_path)[1].lower()
    
    type_map = {
        ".py": "python",
        ".js": "javascript",
        ".html": "html",
        ".css": "css",
        ".json": "json",
        ".md": "markdown",
        ".txt": "text",
        ".jpg": "image",
        ".jpeg": "image",
        ".png": "image",
        ".gif": "image",
        ".svg": "image"
    }
    
    return type_map.get(extension, "unknown")