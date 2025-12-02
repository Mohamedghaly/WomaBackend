#!/bin/bash

# Image Extractor Quick Start Demo
# This script demonstrates the image extractor capabilities

echo "🖼️  Image Extractor Tool - Quick Demo"
echo "======================================"
echo ""

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Virtual environment not activated. Activating..."
    source venv/bin/activate
fi

# Install dependencies if needed
echo "📦 Checking dependencies..."
pip install -q Pillow requests 2>/dev/null || echo "Dependencies already installed"

echo ""
echo "✅ Ready! Here are some example commands:"
echo ""
echo "1️⃣  Download image from URL:"
echo "   python image_extractor.py --url 'https://via.placeholder.com/800' --resize 400x400"
echo ""
echo "2️⃣  Extract from local file:"
echo "   python image_extractor.py --file '/path/to/image.jpg' --format webp"
echo ""
echo "3️⃣  Batch processing:"
echo "   python image_extractor.py --batch urls.txt --resize 1000x1000"
echo ""
echo "4️⃣  Full example with all options:"
echo "   python image_extractor.py --url 'IMAGE_URL' --resize 1200x1200 --format webp --quality 90 --output ./media/"
echo ""
echo "📖 For full documentation, see: IMAGE_EXTRACTOR_GUIDE.md"
echo ""
echo "🚀 Try it now! Example:"
echo "   python image_extractor.py --url 'https://via.placeholder.com/1000' --resize 800x800 --format jpg"
echo ""
