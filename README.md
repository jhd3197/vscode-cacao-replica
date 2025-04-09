# VS Code Replica with Cacao Framework

## Overview
This project is a lightweight replica of Visual Studio Code, built using the [Cacao](https://github.com/jhd3197/Cacao). It demonstrates how to create a desktop-like application with a file explorer, code editor, and syntax highlighting.

<img width="887" alt="image" src="https://github.com/user-attachments/assets/fd95e9c6-74b0-47e9-81ee-36ef69fac313" />

## Features
- **File Explorer**: Browse and select files from the workspace directory.
- **Code Editor**: Edit files with syntax highlighting for various languages.
- **Status Bar**: Displays the current file type and application status.
- **Dynamic File Loading**: Automatically updates the editor with the selected file's content.

## Technologies Used
- **Cacao Framework**: For building the UI components and managing application state.
- **Python**: The core programming language for the application.
- **HTML/CSS/JavaScript**: For rendering the UI and providing interactivity.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/jhd3197/vscode-cacao-replica.git
   ```
2. Navigate to the project directory:
   ```bash
   cd vscode-cacao-replica
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the application in either web or desktop mode:

### Desktop Mode
```bash
python main.py --mode desktop
```

### Web Mode
```bash
python main.py --mode web
```

## Command-Line Arguments
- `--mode`: Choose between `web` or `desktop` mode. Default is `desktop`.
- `--width`: Set the window width (desktop mode only). Default is `1200`.
- `--height`: Set the window height (desktop mode only). Default is `800`.

## Project Structure
```
.
├── main.py          # Entry point of the application
├── README.md        # Project documentation
├── requirements.txt # Python dependencies
├── workspace/       # Sample workspace directory
│   ├── config.json
│   ├── index.html
│   ├── main.py
│   ├── README.md
│   ├── script.js
│   ├── styles.css
│   └── src/         # Additional source files
│       ├── app.py
│       ├── components.py
│       └── utils.py
```


## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- [Cacao Framework](https://github.com/jhd3197/Cacao) for providing the tools to build this application.
- Inspired by Visual Studio Code's design and functionality.
