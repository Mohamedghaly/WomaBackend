# Image Extractor Tool 🖼️

A powerful command-line tool to download, extract, resize, and convert images for your Woma E-commerce platform.

## Features

✅ **Download from URLs** - Fetch images from any web URL  
✅ **Process Local Files** - Extract and optimize images from your computer  
✅ **Batch Processing** - Process multiple images at once  
✅ **Image Resizing** - Automatically resize to standard dimensions  
✅ **Format Conversion** - Convert between JPG, PNG, WebP, GIF  
✅ **Optimization** - Compress images while maintaining quality  
✅ **Smart Naming** - Auto-generate unique filenames  

## Installation

The required dependencies are already in `requirements.txt`. Install them with:

```bash
cd WomaBackend
source venv/bin/activate  # Activate virtual environment
pip install -r requirements.txt
```

## Quick Start

### 1. Download Image from URL

```bash
python image_extractor.py --url "https://example.com/product-image.jpg"
```

### 2. Extract from Local File

```bash
python image_extractor.py --file "/Users/mohamedghaly/Desktop/product.jpg"
```

### 3. Download and Resize

```bash
python image_extractor.py --url "https://example.com/image.jpg" --resize 800x800
```

### 4. Convert to WebP

```bash
python image_extractor.py --file "image.jpg" --format webp --quality 90
```

## Usage Examples

### Basic Usage

#### Download Single Image
```bash
python image_extractor.py --url "https://example.com/shirt.jpg"
```

#### Download Multiple Images
```bash
python image_extractor.py \
  --url "https://example.com/image1.jpg" \
  --url "https://example.com/image2.jpg" \
  --url "https://example.com/image3.jpg"
```

#### Extract from Local Files
```bash
python image_extractor.py --file "/path/to/image1.jpg" --file "/path/to/image2.png"
```

### Advanced Usage

#### Resize and Convert
```bash
python image_extractor.py \
  --url "https://example.com/large-image.jpg" \
  --resize 1200x1200 \
  --format webp \
  --quality 85
```

#### Custom Output Directory
```bash
python image_extractor.py \
  --url "https://example.com/product.jpg" \
  --output ./media/products/
```

#### Batch Processing from File

Create a text file `urls.txt` with one URL per line:
```
https://example.com/image1.jpg
https://example.com/image2.jpg
https://example.com/image3.jpg
```

Then run:
```bash
python image_extractor.py --batch urls.txt --type url --resize 800x800
```

For local files, create `files.txt`:
```
/Users/mohamedghaly/Desktop/product1.jpg
/Users/mohamedghaly/Desktop/product2.png
/Users/mohamedghaly/Desktop/product3.jpg
```

Then run:
```bash
python image_extractor.py --batch files.txt --type file --format webp
```

## Command-Line Options

### Input Options

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--url` | `-u` | Image URL to download | `-u "https://..."`  |
| `--file` | `-f` | Local file path | `-f "/path/to/image.jpg"` |
| `--batch` | `-b` | Text file with URLs/paths | `-b urls.txt` |
| `--type` | `-t` | Type in batch file (url/file) | `-t url` |

### Output Options

| Option | Short | Description | Default | Example |
|--------|-------|-------------|---------|---------|
| `--output` | `-o` | Output directory | `./extracted_images` | `-o ./media/` |
| `--resize` | `-r` | Target size (WxH) | Original size | `-r 800x600` |
| `--format` | - | Output format | Original | `--format webp` |
| `--quality` | `-q` | Image quality (1-100) | 85 | `-q 90` |

### Supported Formats

- **Input:** JPG, JPEG, PNG, GIF, WebP, BMP
- **Output:** JPG, JPEG, PNG, WebP

## Common Use Cases

### 1. Product Images for E-commerce

Download and optimize product images:
```bash
python image_extractor.py \
  --url "https://supplier.com/product-123.jpg" \
  --resize 1200x1200 \
  --format webp \
  --quality 85 \
  --output ./media/products/
```

### 2. Bulk Import Product Images

Create `product_images.txt`:
```
https://cdn.example.com/products/tshirt-blue.jpg
https://cdn.example.com/products/tshirt-red.jpg
https://cdn.example.com/products/pants-black.jpg
```

Run:
```bash
python image_extractor.py \
  --batch product_images.txt \
  --resize 1000x1000 \
  --format webp \
  --output ./media/products/
```

### 3. Convert Local Images

Convert all local images to WebP:
```bash
python image_extractor.py \
  --file "image1.jpg" \
  --file "image2.png" \
  --file "image3.jpg" \
  --format webp \
  --quality 90
```

### 4. Create Thumbnails

```bash
python image_extractor.py \
  --file "/path/to/large-image.jpg" \
  --resize 300x300 \
  --format jpg \
  --quality 80 \
  --output ./media/thumbnails/
```

## Integration with Django Backend

### Upload Extracted Images to Products

After extracting images, you can reference them in your product data:

```python
# Example: After extracting to ./media/products/
{
    "product_id": "uuid-here",
    "images": [
        {
            "image": "products/product_abc123.webp",
            "alt_text": "Blue T-Shirt Front View",
            "is_primary": true
        }
    ]
}
```

## Tips & Best Practices

### 1. Image Sizes for E-commerce

**Product Images:**
- Main: 1200x1200 (high quality)
- Thumbnail: 300x300 (for lists)
- Detail: 800x800 (for variations)

```bash
# Main product image
python image_extractor.py --url "https://..." --resize 1200x1200 --format webp

# Thumbnail
python image_extractor.py --url "https://..." --resize 300x300 --format webp
```

### 2. Format Recommendations

- **WebP**: Best for web (smaller file size, good quality)
- **JPG**: Universal compatibility
- **PNG**: For images with transparency

### 3. Quality Settings

- **90-100**: High quality, larger files (hero images)
- **80-90**: Good quality, balanced (product images) ⭐ **Recommended**
- **70-80**: Lower quality, smaller files (thumbnails)

### 4. Batch Processing

For processing many images, create a text file:

```bash
# Create URLs list
cat > product_urls.txt << EOF
https://example.com/product1.jpg
https://example.com/product2.jpg
https://example.com/product3.jpg
EOF

# Process all at once
python image_extractor.py \
  --batch product_urls.txt \
  --resize 1000x1000 \
  --format webp \
  --quality 85
```

## Troubleshooting

### Error: "Module 'PIL' not found"

Install Pillow:
```bash
pip install Pillow
```

### Error: "Module 'requests' not found"

Install requests:
```bash
pip install requests
```

### Error: "File not found"

For local files, use absolute paths:
```bash
python image_extractor.py --file "/Users/mohamedghaly/Desktop/image.jpg"
```

Or relative paths from the current directory:
```bash
python image_extractor.py --file "./images/product.jpg"
```

### Error: "Connection timeout"

For slow connections, the timeout is 30 seconds. If downloading fails, try:
1. Check your internet connection
2. Verify the URL is accessible
3. Try downloading in smaller batches

## Output

The tool will create an output directory (default: `./extracted_images/`) with:
- Extracted and processed images
- Proper naming and format
- Optimized file sizes

Example output:
```
extracted_images/
├── product_abc12345.webp
├── shirt_blue.webp
├── pants_black.jpg
└── image_f8a3b2c1.png
```

## Integration Example

Complete workflow for adding product images:

```bash
# 1. Extract images
python image_extractor.py \
  --url "https://cdn.example.com/product.jpg" \
  --resize 1200x1200 \
  --format webp \
  --output ./media/products/

# 2. The output will show the saved file path
# ✅ Saved: media/products/product_abc123.webp (234.5 KB)

# 3. Use this path in your Django admin or API to create product variations
```

## Quick Reference

```bash
# Download from URL
python image_extractor.py -u "URL" -o ./output/

# Extract from file  
python image_extractor.py -f "/path/to/file.jpg" -o ./output/

# Resize
python image_extractor.py -u "URL" -r 800x800

# Convert format
python image_extractor.py -f "file.jpg" --format webp

# Batch process
python image_extractor.py -b urls.txt -r 1000x1000 --format webp -q 85

# Full example
python image_extractor.py \
  --url "https://example.com/image.jpg" \
  --resize 1200x1200 \
  --format webp \
  --quality 90 \
  --output ./media/products/
```

---

**Created for:** Woma E-commerce Platform  
**Purpose:** Image management and optimization  
**License:** Internal use only
