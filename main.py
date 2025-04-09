"""
VS Code Replica using Cacao Framework

This application demonstrates how to create a VS Code-like interface
using the Cacao framework, with a file explorer sidebar and code editor.
"""

import os
import sys
import json
from typing import Dict, List, Any, Optional

import cacao
from cacao import State, Component
from cacao.extensions.react_extension import ReactExtension

# Debug toggle
DEBUG = False

# Create the app with React extension for CodeMirror
app = cacao.App(extensions=[ReactExtension()])

# Define states
workspace_state = State({})       # Workspace file structure

# File icons based on file type
FILE_ICONS = {
    "directory": "📁",
    "python": "🐍",
    "javascript": "📜",
    "html": "🌐",
    "css": "🎨",
    "json": "📋",
    "markdown": "📝",
    "text": "📄",
    "image": "🖼️",
    "unknown": "📎"
}

# Get file type based on extension
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

# Get icon for file type
def get_file_icon(file_path: str) -> str:
    """Get icon for file type."""
    file_type = get_file_type(file_path)
    return FILE_ICONS.get(file_type, FILE_ICONS["unknown"])

# Read file content
def read_file_content(file_path: str) -> str:
    """Read file content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

# Scan workspace directory and build file tree
def scan_workspace(workspace_dir: str) -> Dict[str, Any]:
    """Scan workspace directory and build file tree."""
    workspace = {"name": os.path.basename(workspace_dir), "path": workspace_dir, "type": "directory", "children": []}
    
    try:
        items = os.listdir(workspace_dir)
        
        # Sort items: directories first, then files alphabetically
        dirs = sorted([item for item in items if os.path.isdir(os.path.join(workspace_dir, item))])
        files = sorted([item for item in items if not os.path.isdir(os.path.join(workspace_dir, item))])
        sorted_items = dirs + files
        
        for item in sorted_items:
            item_path = os.path.join(workspace_dir, item)
            item_type = "directory" if os.path.isdir(item_path) else get_file_type(item_path)
            
            if os.path.isdir(item_path):
                # Recursively scan subdirectories
                workspace["children"].append(scan_workspace(item_path))
            else:
                workspace["children"].append({
                    "name": item,
                    "path": item_path,
                    "type": item_type
                })
    except Exception as e:
        print(f"Error scanning workspace: {str(e)}")
    
    return workspace

# Initialize workspace
workspace_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workspace")
workspace_state.set(scan_workspace(workspace_dir))

# Set default file (README.md)
default_file_path = os.path.join(workspace_dir, "README.md")
current_file_state = State(default_file_path)  # Currently selected file

# Load default file content
default_content = read_file_content(default_file_path)
file_content_state = State(default_content)    # Content of the selected file



# File Explorer Component
class FileExplorer(Component):
    def __init__(self):
        super().__init__()
        self.id = "file-explorer"
        self.component_type = "file-explorer"
    
    def render_file_tree(self, node: Dict[str, Any], level: int = 0) -> Dict[str, Any]:
        """Render a file tree node."""
        is_directory = node.get("type") == "directory"
        node_path = node.get("path", "") # Get path early
        
        # Create the file/directory item
        if is_directory:
            # Directory item
            item = {
                "type": "div",
                "component_id": f"dir-item-{node_path.replace(os.sep, '_')}",
                "props": {
                    "style": {
                        "paddingLeft": f"{level * 16}px",
                        "display": "flex",
                        "alignItems": "center",
                        "padding": "4px 8px",
                        "borderRadius": "4px",
                        "margin": "2px 0",
                    },
                    "children": [
                        # Directory icon
                        {
                            "type": "span",
                            "props": {
                                "content": get_file_icon(node_path),
                                "style": {
                                    "marginRight": "8px",
                                    "fontSize": "16px"
                                }
                            }
                        },
                        # Directory name
                        {
                            "type": "span",
                            "props": {
                                "content": node.get("name", ""),
                                "style": {
                                    "fontSize": "14px",
                                    "color": "#cccccc"
                                }
                            }
                        }
                    ]
                }
            }
        else:
            # Check if this file is the currently selected file
            is_current_file = node_path == current_file_state.value
            
            # File item - Using a div with a button that has the path in its data property
            item = {
                "type": "div",
                "component_id": f"file-item-{node_path.replace(os.sep, '_')}",
                "component_type": "file-item",
                "props": {
                    "style": {
                        "paddingLeft": f"{level * 16}px",
                        "display": "flex",
                        "alignItems": "center",
                        "padding": "4px 8px",
                        "borderRadius": "4px",
                        "margin": "2px 0",
                        "cursor": "pointer",
                        "backgroundColor": "#37373d" if is_current_file else "transparent",  # Highlight current file
                        "transition": "background-color 0.2s ease",  # Smooth transition for hover
                        ":hover": {
                            "backgroundColor": "#2a2d2e"  # Darker background on hover
                        }
                    },
                    "children": [
                        # File icon
                        {
                            "type": "span",
                            "props": {
                                "content": get_file_icon(node_path),
                                "style": {
                                    "marginRight": "8px",
                                    "fontSize": "16px",
                                    "color": "#75beff" if is_current_file else "#cccccc"  # Blue icon for current file
                                }
                            }
                        },
                        # File name as a button with explicit path in data
                        {
                            "type": "button",
                            "component_type": "file-button",
                            "props": {
                                "label": node.get("name", ""),
                                "action": "select_file",
                                "data": {"path": node_path},  # This will now be passed to the event handler
                                "style": {
                                    "fontSize": "14px",
                                    "color": "#ffffff" if is_current_file else "#cccccc",  # Brighter text for current file
                                    "fontWeight": "bold" if is_current_file else "normal",  # Bold text for current file
                                    "background": "none",
                                    "border": "none",
                                    "padding": "4px 8px",  # Larger clickable area
                                    "margin": "-4px -8px",  # Offset the padding to maintain layout
                                    "width": "calc(100% + 16px)",  # Ensure button covers the full width
                                    "cursor": "pointer",
                                    "textAlign": "left",
                                    "transition": "color 0.2s ease, text-decoration 0.2s ease",  # Smooth transitions
                                    ":hover": {
                                        "color": "#ffffff",  # Brighter text on hover
                                        "textDecoration": "underline"
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        
        # If it's a directory, add its children
        if is_directory and "children" in node:
            children_container = {
                "type": "div",
                "props": {
                    "children": []
                }
            }
            
            for child in node.get("children", []):
                rendered_child = self.render_file_tree(child, level + 1)
                if rendered_child: # Only append if not None
                    children_container["props"]["children"].append(rendered_child)
            
            return {
                "type": "div",
                "props": {
                    "children": [item, children_container]
                }
            }
        
        # Return the item (file or directory without children)
        return item
    
    def render(self, ui_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Render the file explorer component."""
        workspace = workspace_state.value
        if DEBUG:
            print(f"DEBUG: FileExplorer.render - workspace data: {json.dumps(workspace, indent=2)}")
        
        return {
            "type": "div",
            "props": {
                "style": {
                    "height": "100%",
                    "overflow": "auto",
                    "backgroundColor": "#252526",
                    "color": "#cccccc",
                    "padding": "8px"
                },
                "children": [
                    {
                        "type": "h3",
                        "props": {
                            "content": "EXPLORER",
                            "style": {
                                "fontSize": "11px",
                                "fontWeight": "bold",
                                "textTransform": "uppercase",
                                "color": "#bbbbbb",
                                "padding": "8px 0",
                                "margin": "0"
                            }
                        }
                    },
                    self.render_file_tree(workspace)
                ]
            }
        }

# Editor Component
class Editor(Component):
    def __init__(self):
        super().__init__()
        self.id = "editor"
        self.component_type = "editor"
    
    def render(self, ui_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Render the editor component."""
        if DEBUG:
            print(f"DEBUG: Editor.render called.")
        current_file = current_file_state.value
        file_content = file_content_state.value
        if DEBUG:
            print(f"DEBUG: Editor.render - current_file: {current_file}")
            print(f"DEBUG: Editor.render - file_content (length): {len(file_content)}")
        
        if not current_file:
            # Welcome screen when no file is selected
            return {
                "type": "div",
                "props": {
                    "style": {
                        "height": "100%",
                        "display": "flex",
                        "flexDirection": "column",
                        "justifyContent": "center",
                        "alignItems": "center",
                        "backgroundColor": "#1e1e1e",
                        "color": "#cccccc",
                        "padding": "20px"
                    },
                    "children": [
                        {
                            "type": "h1",
                            "props": {
                                "content": "VS Code Replica",
                                "style": {
                                    "fontSize": "32px",
                                    "fontWeight": "300",
                                    "marginBottom": "20px",
                                    "color": "#0098ff"
                                }
                            }
                        },
                        {
                            "type": "p",
                            "props": {
                                "content": "Select a file from the explorer to start editing",
                                "style": {
                                    "fontSize": "16px",
                                    "color": "#cccccc"
                                }
                            }
                        }
                    ]
                }
            }
        
        # Get file extension for syntax highlighting
        file_ext = os.path.splitext(current_file)[1].lower().replace(".", "")
        if file_ext == "py":
            mode = "python"
        elif file_ext == "js":
            mode = "javascript"
        elif file_ext == "html":
            mode = "htmlmixed"
        elif file_ext == "css":
            mode = "css"
        elif file_ext == "json":
            mode = "javascript"
        elif file_ext == "md":
            mode = "markdown"
        else:
            mode = "text"
        
        # Editor header with filename
        header = {
            "type": "div",
            "props": {
                "style": {
                    "backgroundColor": "#2d2d2d",
                    "padding": "8px 16px",
                    "borderBottom": "1px solid #1e1e1e",
                    "display": "flex",
                    "alignItems": "center"
                },
                "children": [
                    {
                        "type": "span",
                        "props": {
                            "content": get_file_icon(current_file),
                            "style": {
                                "marginRight": "8px",
                                "fontSize": "16px"
                            }
                        }
                    },
                    {
                        "type": "span",
                        "props": {
                            "content": os.path.basename(current_file),
                            "style": {
                                "fontSize": "14px",
                                "color": "#cccccc"
                            }
                        }
                    }
                ]
            }
        }
        
        # Editable text editor using textarea
        editor = {
            "type": "div",
            "props": {
                "style": {
                    "backgroundColor": "#1e1e1e",
                    "color": "#cccccc",
                    "fontFamily": "monospace",
                    "padding": "10px",
                    "overflow": "auto",
                    "height": "100%",
                    "display": "flex",
                    "flexDirection": "column"
                },
                "children": [
                    {
                        "type": "textarea",
                        "component_id": "code-editor-textarea",
                        "props": {
                            "content": file_content,
                            "action": "update_file_content",
                            "data": {"path": current_file},
                            "style": {
                                "margin": "0",
                                "padding": "10px",
                                "fontSize": "14px",
                                "lineHeight": "1.5",
                                "backgroundColor": "#1e1e1e",
                                "color": "#cccccc",
                                "border": "none",
                                "outline": "none",
                                "resize": "none",
                                "width": "100%",
                                "height": "100%",
                                "fontFamily": "'Consolas', 'Courier New', monospace",
                                "tabSize": "4",
                                "whiteSpace": "pre",
                                "overflowWrap": "normal",
                                "overflowX": "auto"
                            }
                        }
                    }
                ]
            }
        }
        
        return {
            "type": "div",
            "props": {
                "style": {
                    "height": "100%",
                    "display": "flex",
                    "flexDirection": "column",
                    "backgroundColor": "#1e1e1e"
                },
                "children": [
                    header,
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "flex": "1",
                                "overflow": "hidden"
                            },
                            "children": [editor]
                        }
                    }
                ]
            }
        }

# Status Bar Component
class StatusBar(Component):
    def __init__(self):
        super().__init__()
        self.id = "status-bar"
        self.component_type = "status-bar"
    
    def render(self, ui_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Render the status bar component."""
        current_file = current_file_state.value
        file_type = get_file_type(current_file) if current_file else "none"
        
        return {
            "type": "div",
            "props": {
                "style": {
                    "height": "22px",
                    "backgroundColor": "#007acc",
                    "color": "white",
                    "display": "flex",
                    "alignItems": "center",
                    "padding": "0 10px",
                    "fontSize": "12px",
                    "justifyContent": "space-between"
                },
                "children": [
                    # Left side
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "display": "flex",
                                "alignItems": "center"
                            },
                            "children": [
                                {
                                    "type": "span",
                                    "props": {
                                        "content": "VS Code Replica",
                                        "style": {
                                            "marginRight": "15px"
                                        }
                                    }
                                }
                            ]
                        }
                    },
                    # Right side
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "display": "flex",
                                "alignItems": "center"
                            },
                            "children": [
                                {
                                    "type": "span",
                                    "props": {
                                        "content": file_type.upper() if current_file else "",
                                        "style": {
                                            "marginLeft": "15px"
                                        }
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }

# Create components
file_explorer = FileExplorer()
editor = Editor()
status_bar = StatusBar()

# Register event handler for file selection
@app.event("select_file")
def handle_select_file(event_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Handle file selection event."""
    if DEBUG:
        print(f"DEBUG: Raw event data received by handle_select_file: {event_data}")
    
    # Extract file path from event data
    if not event_data or "path" not in event_data:
        if DEBUG:
            print("DEBUG: No path in event data")
        return {"error": "No path in event data"}
    
    file_path = event_data["path"]
    if DEBUG:
        print(f"DEBUG: Found file path in event data: {file_path}")
    
    # Check if it's a directory
    if os.path.isdir(file_path):
        if DEBUG:
            print(f"DEBUG: Cannot open directory: {file_path}")
        return {"error": "Cannot open directory"}
    
    # Update current file state
    if DEBUG:
        print(f"DEBUG: Setting current_file_state to: {file_path}")
    current_file_state.set(file_path)
    
    # Read file content
    content = read_file_content(file_path)
    if DEBUG:
        print(f"DEBUG: Read content (first 50 chars): {content[:50]}")
        print(f"DEBUG: Setting file_content_state (length): {len(content)}")
    file_content_state.set(content)
    
    if DEBUG:
        print(f"Selected file: {file_path}")
    
    return {
        "file": file_path,
        "type": get_file_type(file_path)
    }

# Event handler for updating file content
@app.event("update_file_content")
def handle_update_file_content(event_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Handle file content update event."""
    if DEBUG:
        print(f"DEBUG: File content update event received: {event_data}")
    
    if not event_data or "path" not in event_data or "content" not in event_data:
        if DEBUG:
            print("DEBUG: Missing path or content in update event")
        return {"error": "Missing path or content"}
    
    file_path = event_data["path"]
    new_content = event_data["content"]
    
    # Check if it's a directory
    if os.path.isdir(file_path):
        if DEBUG:
            print(f"DEBUG: Cannot update directory: {file_path}")
        return {"error": "Cannot update directory"}
    
    # Write the updated content to the file
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        if DEBUG:
            print(f"DEBUG: Successfully updated file: {file_path}")
        
        # Update the file content state
        file_content_state.set(new_content)
        
        return {
            "success": True,
            "file": file_path
        }
    except Exception as e:
        if DEBUG:
            print(f"DEBUG: Error updating file: {str(e)}")
        return {
            "error": f"Error updating file: {str(e)}"
        }

# Main layout
@app.mix("/")
def home() -> Dict[str, Any]:
    """Main route handler."""
    return {
        "type": "div",
        "props": {
            "style": {
                "display": "flex",
                "flexDirection": "column",
                "height": "100vh",
                "backgroundColor": "#1e1e1e",
                "color": "#cccccc",
                "fontFamily": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
            },
            "children": [
                # Main content with sidebar and editor
                {
                    "type": "div",
                    "props": {
                        "style": {
                            "display": "flex",
                            "flex": "1",
                            "overflow": "hidden"
                        },
                        "children": [
                            # Sidebar (File Explorer)
                            {
                                "type": "div",
                                "props": {
                                    "style": {
                                        "width": "250px",
                                        "borderRight": "1px solid #333333",
                                        "overflow": "hidden",
                                        "display": "flex",
                                        "flexDirection": "column"
                                    },
                                    "children": [file_explorer.render()]
                                }
                            },
                            # Editor area
                            {
                                "type": "div",
                                "props": {
                                    "style": {
                                        "flex": "1",
                                        "overflow": "hidden"
                                    },
                                    "children": [editor.render()]
                                }
                            }
                        ]
                    }
                },
                # Status bar
                status_bar.render()
            ]
        }
    }

if __name__ == "__main__":
    import argparse
    
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="VS Code Replica")
    parser.add_argument("--mode", choices=["web", "desktop"], default="desktop",
                       help="Run mode: 'web' for browser or 'desktop' for desktop window")
    parser.add_argument("--width", type=int, default=1200, help="Window width (desktop mode only)")
    parser.add_argument("--height", type=int, default=800, help="Window height (desktop mode only)")
    
    args = parser.parse_args()
    
    # Launch application
    app.brew(
        type=args.mode,
        title="VS Code Replica",
        width=args.width,
        height=args.height,
        resizable=True,
        fullscreen=False,
    )