#!/usr/bin/env python3
"""
OpenRouter Balance Menubar App

A macOS menubar application to monitor your OpenRouter API credit balance.
"""

import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime
import threading

try:
    import rumps
except ImportError:
    print("Error: rumps library is required.")
    print("Install with: pip install rumps")
    sys.exit(1)


class BalanceMenuBar(rumps.App):
    """MenuBar application for displaying OpenRouter balance."""
    
    def __init__(self):
        super(BalanceMenuBar, self).__init__("💰 Loading...")
        self.api_key = os.environ.get("OPENROUTER_API_KEY")
        self.current_data = None
        self.last_update = None
        
        # Check for API key
        if not self.api_key:
            self.show_api_key_error()
            return
        
        # Build initial menu
        self.build_menu()
        
        # Fetch balance immediately
        self.refresh_balance(None)
        
        # Start auto-refresh timer (every 20 seconds)
        self.refresh_timer = rumps.Timer(self.refresh_balance, 20)
        self.refresh_timer.start()
    
    def show_api_key_error(self):
        """Display error when API key is missing."""
        self.title = "💰 Error"
        rumps.alert(
            title="API Key Required",
            message="OPENROUTER_API_KEY environment variable not set.\n\n"
            "Set it with:\nexport OPENROUTER_API_KEY='your-key'",
            ok="Quit"
        )
        rumps.quit_application()
    
    def build_menu(self):
        """Construct the dropdown menu."""
        self.menu.clear()
        
        if self.current_data:
            self.add_balance_items()
        else:
            self.menu.add(rumps.MenuItem("Loading...", callback=None))
        
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem("Refresh", callback=self.refresh_balance))
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem("Quit", callback=self.quit_app))
    
    def add_balance_items(self):
        """Add balance information items to menu."""
        if 'data' not in self.current_data:
            self.menu.add(rumps.MenuItem("No data available", callback=None))
            return
        
        info = self.current_data['data']
        
        # Display credit information
        if isinstance(info, dict):
            total = info.get('total_credits', 0)
            usage = info.get('total_usage', 0)
            remaining = total - usage
            self.menu.add(rumps.MenuItem(f"Credits:    ${total:.2f}", callback=None))
            self.menu.add(rumps.MenuItem(f"Used:       ${usage:.2f}", callback=None))
            self.menu.add(rumps.MenuItem(f"Remaining:  ${remaining:.2f}", callback=None))
        elif isinstance(info, (int, float)):
            self.menu.add(rumps.MenuItem(f"Balance: ${info:.2f}", callback=None))
        else:
            self.menu.add(rumps.MenuItem(f"Balance: {info}", callback=None))
        
        # Show last update time
        if self.last_update:
            self.menu.add(rumps.separator)
            time_str = self.last_update.strftime("%I:%M %p")
            self.menu.add(rumps.MenuItem(f"Updated: {time_str}", callback=None))
    
    def fetch_api_data(self):
        """Retrieve balance data from OpenRouter API."""
        api_url = "https://openrouter.ai/api/v1/credits"
        
        req = urllib.request.Request(
            api_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            method="GET"
        )
        
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as err:
            raise Exception(f"HTTP {err.code}: {err.reason}")
        except Exception as err:
            raise Exception(f"Request failed: {str(err)}")
    
    def refresh_balance(self, sender):
        """Refresh the balance from API."""
        try:
            self.current_data = self.fetch_api_data()
            self.last_update = datetime.now()
            self.update_display()
        except Exception as err:
            self.title = "💰 Error"
            rumps.notification("Balance Update Failed", "", str(err))
    
    def update_display(self):
        """Update the menubar title and menu contents."""
        if self.current_data and 'data' in self.current_data:
            info = self.current_data['data']
            if isinstance(info, dict) and 'total_credits' in info:
                remaining = info['total_credits'] - info.get('total_usage', 0)
                self.title = f"💰 ${remaining:.2f}"
            elif isinstance(info, (int, float)):
                self.title = f"💰 ${info:.2f}"
            else:
                self.title = "💰 N/A"
        self.build_menu()
    
    def quit_app(self, sender):
        rumps.quit_application()

if __name__ == "__main__":
    BalanceMenuBar().run()
