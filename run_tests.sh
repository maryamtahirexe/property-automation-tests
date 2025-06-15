#!/bin/bash
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "🧪 Running Test Suite..."
python3 test_suite.py
