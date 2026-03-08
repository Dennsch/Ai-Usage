from setuptools import setup

APP = ["menubar_app.py"]
DATA_FILES = []
OPTIONS = {
    "argv_emulation": False,
    "plist": {
        "CFBundleName": "OpenRouter Balance",
        "CFBundleDisplayName": "OpenRouter Balance",
        "CFBundleIdentifier": "ai.usage.openrouter.balance",
        "CFBundleVersion": "1.0.0",
        "CFBundleShortVersionString": "1.0.0",
        "LSUIElement": True,
    },
    "packages": ["rumps"],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
