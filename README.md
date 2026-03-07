# Ai-Usage
A simple tool to check your OpenRouter API credit balance.

## Features

- **MenuBar App**: macOS menubar application showing your balance at a glance
- **Command-line Tool**: Simple Python script for checking balance
- Auto-refresh every 20 seconds (menubar app)
- Manual refresh option
- Display credit limit, usage, and remaining balance

## Prerequisites

- Python 3.6 or higher
- OpenRouter API key
- macOS (for menubar app)

## Setup

1. Get your API key from [OpenRouter](https://openrouter.ai/)

2. Set your API key as an environment variable:
   ```bash
   export OPENROUTER_API_KEY='your-api-key-here'
   ```
   
   For permanent setup, add this to your `~/.zshrc` or `~/.bash_profile`:
   ```bash
   echo "export OPENROUTER_API_KEY='your-api-key-here'" >> ~/.zshrc
   source ~/.zshrc
   ```

3. Install dependencies (for menubar app):
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### MenuBar App (Recommended)

Run the menubar app to see your balance at a glance:

```bash
python3 menubar_app.py
```

The app will:
- Display your balance in the menubar (💰 $X.XX)
- Auto-refresh every 20 seconds
- Show detailed information in the dropdown menu
- Allow manual refresh via the menu

To keep it running in the background, you can make it executable:
```bash
chmod +x menubar_app.py
./menubar_app.py
```

### Command-Line Tool

Run the script to check your credit balance:

```bash
python3 check_balance.py
```

Or make it executable and run directly:
```bash
chmod +x check_balance.py
./check_balance.py
```

## Output

The tools will display your OpenRouter account information including:
- **Credit Limit**: Total credit available
- **Usage**: Amount of credit used
- **Remaining**: Credit balance remaining
- **Key Label**: Your API key label (if set)
