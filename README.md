# Ai-Usage
A simple tool to check your OpenRouter API credit balance.

## Features

- Connect to OpenRouter API
- Display current credit balance
- Simple command-line interface

## Prerequisites

- Python 3.6 or higher
- OpenRouter API key

## Setup

1. Get your API key from [OpenRouter](https://openrouter.ai/)

2. Set your API key as an environment variable:
   ```bash
   export OPENROUTER_API_KEY='your-api-key-here'
   ```

## Usage

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

The script will display your OpenRouter account information including:
- Credit balance
- Usage limits
- Rate limits
- Other account details
