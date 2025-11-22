# Virtual Environment Activation Instructions

## For Windows (PowerShell)
```powershell
cd TestCopilotGame
TestCopilotGame\venv\Scripts\Activate.ps1
```

Or if you get an execution policy error, use:
```powershell
cd TestCopilotGame
TestCopilotGame\venv\Scripts\activate.bat
```

## For Windows (Command Prompt)
```cmd
cd TestCopilotGame
TestCopilotGame\venv\Scripts\activate.bat
```

## For Linux/Mac
```bash
cd TestCopilotGame
source venv/bin/activate
```

## Verify Installation
After activating the virtual environment, verify pygame is installed:
```bash
python -c "import pygame; print(f'Pygame version: {pygame.version.ver}')"
```

## Run the Game
Once the venv is activated, run:
```bash
python main.py
```

## Note
The venv folder is located at: `TestCopilotGame/TestCopilotGame/venv/`
Pygame version 2.6.1 is already installed in this virtual environment.

