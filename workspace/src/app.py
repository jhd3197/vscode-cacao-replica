"""
Main application module for the sample project.
This file demonstrates a more complex Python application structure.
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ConfigManager:
    """Manages application configuration."""
    
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from JSON file."""
        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
            logger.info(f"Configuration loaded from {self.config_path}")
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {self.config_path}")
            self.config = {"error": "Configuration not found"}
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in configuration file: {self.config_path}")
            self.config = {"error": "Invalid configuration format"}
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key."""
        return self.config.get(key, default)
    
    def get_nested(self, *keys: str, default: Any = None) -> Any:
        """Get a nested configuration value."""
        current = self.config
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current

class Application:
    """Main application class."""
    
    def __init__(self, config_path: str = "../config.json"):
        self.config_manager = ConfigManager(config_path)
        self.name = self.config_manager.get("appName", "Default App")
        self.version = self.config_manager.get("version", "0.0.0")
        logger.info(f"Initializing application: {self.name} v{self.version}")
    
    def run(self) -> None:
        """Run the application."""
        logger.info(f"Running {self.name}")
        theme = self.config_manager.get_nested("settings", "theme", default="light")
        font_size = self.config_manager.get_nested("settings", "fontSize", default=12)
        
        logger.info(f"Using theme: {theme}, font size: {font_size}")
        
        # Simulate application execution
        print(f"Welcome to {self.name} v{self.version}!")
        print(f"Theme: {theme}")
        print(f"Font Size: {font_size}")
        
        # List features
        features = self.config_manager.get("features", {})
        if features:
            print("\nEnabled Features:")
            for feature, enabled in features.items():
                status = "Enabled" if enabled else "Disabled"
                print(f"- {feature}: {status}")

if __name__ == "__main__":
    app = Application()
    app.run()