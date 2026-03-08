#!/usr/bin/env bash
set -euo pipefail

APP_NAME="OpenRouter Balance"
APP_BUNDLE="dist/${APP_NAME}.app"
DMG_NAME="OpenRouter-Balance-1.0.0.dmg"

./.venv/bin/python setup.py py2app

if [[ ! -d "${APP_BUNDLE}" ]]; then
  echo "Build failed: ${APP_BUNDLE} not found"
  exit 1
fi

hdiutil create -volname "${APP_NAME}" -srcfolder "${APP_BUNDLE}" -ov -format UDZO "dist/${DMG_NAME}"

echo "DMG created: dist/${DMG_NAME}"
