#!/usr/bin/env python3
"""
OpenRouter Credit Balance Checker

This script connects to OpenRouter API and displays your current credit balance.
"""

import os
import sys
import json
import urllib.request
import urllib.error


def get_credit_balance(api_key):
    """
    Fetch credit balance from OpenRouter API.
    
    Args:
        api_key (str): OpenRouter API key
        
    Returns:
        dict: API response containing credit information
    """
    url = "https://openrouter.ai/api/v1/credits"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    request = urllib.request.Request(url, headers=headers, method="GET")
    
    try:
        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read().decode())
            return data
    except urllib.error.HTTPError as e:
        print(f"Error: HTTP {e.code} - {e.reason}")
        print(f"Response: {e.read().decode()}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def main():
    api_key = os.environ.get("OPENROUTER_API_KEY")
    
    if not api_key:
        print("Error: OPENROUTER_API_KEY environment variable is not set.")
        print("Please set it with: export OPENROUTER_API_KEY='your-api-key'")
        sys.exit(1)
    
    print("Fetching OpenRouter credit balance...")
    balance_info = get_credit_balance(api_key)
    print(json.dumps(balance_info, indent=2))

if __name__ == "__main__":
    main()
