"""
UI Components for the sample project.
This file demonstrates a component-based architecture.
"""

from typing import Dict, List, Any, Optional, Callable

class Component:
    """Base component class."""
    
    def __init__(self, id: str = None):
        self.id = id
        self.children: List[Component] = []
        self.parent: Optional[Component] = None
        self.event_handlers: Dict[str, Callable] = {}
    
    def add_child(self, child: 'Component') -> 'Component':
        """Add a child component."""
        self.children.append(child)
        child.parent = self
        return self
    
    def remove_child(self, child: 'Component') -> bool:
        """Remove a child component."""
        if child in self.children:
            self.children.remove(child)
            child.parent = None
            return True
        return False
    
    def on(self, event: str, handler: Callable) -> 'Component':
        """Register an event handler."""
        self.event_handlers[event] = handler
        return self
    
    def trigger(self, event: str, data: Any = None) -> Any:
        """Trigger an event."""
        if event in self.event_handlers:
            return self.event_handlers[event](data)
        return None
    
    def render(self) -> Dict[str, Any]:
        """Render the component (to be implemented by subclasses)."""
        raise NotImplementedError("Subclasses must implement render()")


class Button(Component):
    """Button component."""
    
    def __init__(self, label: str, id: str = None, style: Dict[str, Any] = None):
        super().__init__(id)
        self.label = label
        self.style = style or {}
    
    def render(self) -> Dict[str, Any]:
        """Render the button component."""
        return {
            "type": "button",
            "props": {
                "id": self.id,
                "label": self.label,
                "style": self.style,
                "children": [child.render() for child in self.children]
            }
        }


class Container(Component):
    """Container component."""
    
    def __init__(self, id: str = None, style: Dict[str, Any] = None):
        super().__init__(id)
        self.style = style or {}
    
    def render(self) -> Dict[str, Any]:
        """Render the container component."""
        return {
            "type": "div",
            "props": {
                "id": self.id,
                "style": self.style,
                "children": [child.render() for child in self.children]
            }
        }


class Text(Component):
    """Text component."""
    
    def __init__(self, content: str, id: str = None, style: Dict[str, Any] = None):
        super().__init__(id)
        self.content = content
        self.style = style or {}
    
    def render(self) -> Dict[str, Any]:
        """Render the text component."""
        return {
            "type": "text",
            "props": {
                "id": self.id,
                "content": self.content,
                "style": self.style,
                "children": [child.render() for child in self.children]
            }
        }


class Input(Component):
    """Input component."""
    
    def __init__(self, 
                 id: str = None, 
                 placeholder: str = "", 
                 value: str = "", 
                 input_type: str = "text",
                 style: Dict[str, Any] = None):
        super().__init__(id)
        self.placeholder = placeholder
        self.value = value
        self.input_type = input_type
        self.style = style or {}
    
    def render(self) -> Dict[str, Any]:
        """Render the input component."""
        return {
            "type": "input",
            "props": {
                "id": self.id,
                "placeholder": self.placeholder,
                "value": self.value,
                "type": self.input_type,
                "style": self.style,
                "children": [child.render() for child in self.children]
            }
        }


# Example usage
def create_sample_ui() -> Dict[str, Any]:
    """Create a sample UI structure."""
    container = Container(id="main-container", style={"padding": "20px"})
    
    # Add a title
    title = Text(
        content="Sample UI Components", 
        style={"fontSize": "24px", "fontWeight": "bold", "marginBottom": "20px"}
    )
    container.add_child(title)
    
    # Add a form
    form = Container(style={"display": "flex", "flexDirection": "column", "gap": "10px"})
    
    username_input = Input(
        id="username",
        placeholder="Enter username",
        style={"padding": "8px", "borderRadius": "4px", "border": "1px solid #ccc"}
    )
    
    password_input = Input(
        id="password",
        placeholder="Enter password",
        input_type="password",
        style={"padding": "8px", "borderRadius": "4px", "border": "1px solid #ccc"}
    )
    
    submit_button = Button(
        label="Login",
        style={
            "padding": "8px 16px",
            "backgroundColor": "#4CAF50",
            "color": "white",
            "border": "none",
            "borderRadius": "4px",
            "cursor": "pointer",
            "marginTop": "10px"
        }
    )
    
    # Register event handler
    def handle_submit(data):
        print(f"Login submitted with data: {data}")
        return {"success": True}
    
    submit_button.on("click", handle_submit)
    
    # Add components to form
    form.add_child(username_input)
    form.add_child(password_input)
    form.add_child(submit_button)
    
    # Add form to container
    container.add_child(form)
    
    return container.render()