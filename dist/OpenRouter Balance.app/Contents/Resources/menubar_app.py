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
        self.config_path = os.path.join(self._application_support, "settings.json")
        self.api_key = self.load_api_key()
        self.current_data = None
        self.last_update = None

        # Build initial menu
        self.build_menu()

        # Set startup display and fetch balance if configured
        if self.api_key:
            self.refresh_balance(None)
        else:
            self.title = "💰 Setup"

        # Start auto-refresh timer (every 20 seconds)
        self.refresh_timer = rumps.Timer(self.refresh_balance, 20)
        self.refresh_timer.start()

    def load_api_key(self):
        """Load API key from environment first, then local settings file."""
        env_key = os.environ.get("OPENROUTER_API_KEY")
        if env_key and env_key.strip():
            return env_key.strip()

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                file_key = data.get("openrouter_api_key", "").strip()
                return file_key or None
        except (OSError, json.JSONDecodeError, AttributeError):
            return None

    def save_api_key(self, api_key):
        """Persist API key in app settings."""
        payload = {"openrouter_api_key": api_key}
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(payload, f)
        try:
            os.chmod(self.config_path, 0o600)
        except OSError:
            pass

    def build_menu(self):
        """Construct the dropdown menu."""
        self.menu.clear()

        if self.current_data:
            self.add_balance_items()
        elif not self.api_key:
            self.menu.add(rumps.MenuItem("API key not set", callback=None))
            self.menu.add(rumps.MenuItem("Right-click -> Settings to save key", callback=None))
        else:
            self.menu.add(rumps.MenuItem("Loading...", callback=None))

        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem("Settings", callback=self.open_settings))
        self.menu.add(rumps.MenuItem("Clear Saved API Key", callback=self.clear_saved_api_key))
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

    def open_settings(self, sender):
        """Open settings prompt to save API key."""
        prompt = rumps.Window(
            title="Settings",
            message="Enter your OpenRouter API key.",
            default_text=self.api_key or "",
            ok="Save",
            cancel=True,
            secure=True,
        )
        response = prompt.run()
        if not response.clicked:
            return

        new_key = response.text.strip()
        if not new_key:
            rumps.alert(title="Invalid API Key", message="API key cannot be empty.")
            return

        self.api_key = new_key
        self.save_api_key(new_key)
        self.current_data = None
        self.last_update = None
        self.title = "💰 Loading..."
        self.build_menu()
        self.refresh_balance(None)
        rumps.notification("Settings Saved", "", "OpenRouter API key updated.")

    def clear_saved_api_key(self, sender):
        """Remove saved API key and return to setup mode."""
        try:
            os.remove(self.config_path)
        except FileNotFoundError:
            pass
        except OSError as err:
            rumps.alert(title="Could Not Clear Key", message=str(err))
            return

        env_key = os.environ.get("OPENROUTER_API_KEY")
        self.api_key = env_key.strip() if env_key else None
        self.current_data = None
        self.last_update = None
        self.title = "💰 Setup" if not self.api_key else "💰 Loading..."
        self.build_menu()

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
        if not self.api_key:
            self.current_data = None
            self.last_update = None
            self.title = "💰 Setup"
            self.build_menu()
            return

        try:
            self.current_data = self.fetch_api_data()
            self.last_update = datetime.now()
            self.update_display()
        except Exception as err:
            self.title = "💰 Error"
            rumps.notification("Balance Update Failed", "", str(err))
            self.build_menu()
    
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
