#!/usr/bin/env python3
"""
Image Extractor Tool for Woma E-commerce

This tool can:
1. Download images from URLs
2. Copy/process images from local file paths
3. Convert images to optimized formats
4. Resize images to standard sizes
5. Save images with proper naming

Usage:
    python image_extractor.py --url "https://example.com/image.jpg" --output ./images/
    python image_extractor.py --file "/path/to/image.jpg" --output ./images/
    python image_extractor.py --file "image.jpg" --resize 800x800 --format webp
"""

import os
import sys
import argparse
import requests
from pathlib import Path
from urllib.parse import urlparse
import uuid
from PIL import Image
from io import BytesIO


class ImageExtractor:
    """Extract and process images from URLs or local files."""
    
    SUPPORTED_FORMATS = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp']
    DEFAULT_OUTPUT_DIR = './extracted_images'
    
    def __init__(self, output_dir=None, resize=None, format=None, quality=85):
        """
        Initialize the image extractor.
        
        Args:
            output_dir (str): Directory to save extracted images
            resize (tuple): Target size as (width, height) or None
            format (str): Output format (jpg, png, webp, etc.)
            quality (int): Image quality for compression (1-100)
        """
        self.output_dir = Path(output_dir or self.DEFAULT_OUTPUT_DIR)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.resize = resize
        self.format = format
        self.quality = quality
        
    def download_from_url(self, url, filename=None):
        """
        Download an image from a URL.
        
        Args:
            url (str): URL of the image
            filename (str): Optional custom filename
            
        Returns:
            str: Path to the saved image or None if failed
        """
        try:
            print(f"📥 Downloading from URL: {url}")
            
            # Download the image
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Check if it's an image
            content_type = response.headers.get('content-type', '')
            if 'image' not in content_type.lower():
                print(f"⚠️  Warning: URL doesn't appear to be an image (content-type: {content_type})")
            
            # Open image from bytes
            image = Image.open(BytesIO(response.content))
            
            # Generate filename if not provided
            if not filename:
                # Try to get filename from URL
                parsed_url = urlparse(url)
                url_filename = os.path.basename(parsed_url.path)
                if url_filename and '.' in url_filename:
                    filename = url_filename
                else:
                    # Generate UUID-based filename
                    ext = self.format or image.format.lower()
                    filename = f"image_{uuid.uuid4().hex[:8]}.{ext}"
            
            # Process and save
            return self._process_and_save(image, filename)
            
        except requests.RequestException as e:
            print(f"❌ Failed to download image: {e}")
            return None
        except Exception as e:
            print(f"❌ Error processing image: {e}")
            return None
    
    def extract_from_file(self, file_path, filename=None):
        """
        Extract/copy an image from a local file path.
        
        Args:
            file_path (str): Path to the local image file
            filename (str): Optional custom filename
            
        Returns:
            str: Path to the saved image or None if failed
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                print(f"❌ File not found: {file_path}")
                return None
            
            print(f"📂 Reading from file: {file_path}")
            
            # Open the image
            image = Image.open(file_path)
            
            # Generate filename if not provided
            if not filename:
                filename = file_path.name
            
            # Process and save
            return self._process_and_save(image, filename)
            
        except Exception as e:
            print(f"❌ Error processing file: {e}")
            return None
    
    def _process_and_save(self, image, filename):
        """
        Process (resize, convert) and save the image.
        
        Args:
            image (PIL.Image): Image object
            filename (str): Output filename
            
        Returns:
            str: Path to the saved image
        """
        # Get image info
        original_size = image.size
        original_format = image.format
        print(f"📐 Original: {original_size[0]}x{original_size[1]} ({original_format})")
        
        # Convert RGBA to RGB if saving as JPEG
        output_format = self.format or original_format or 'png'
        if output_format.lower() in ['jpg', 'jpeg'] and image.mode in ['RGBA', 'LA', 'P']:
            print("🔄 Converting RGBA to RGB for JPEG format")
            rgb_image = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            rgb_image.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
            image = rgb_image
        
        # Resize if requested
        if self.resize:
            print(f"📏 Resizing to: {self.resize[0]}x{self.resize[1]}")
            image = image.resize(self.resize, Image.Resampling.LANCZOS)
        
        # Ensure filename has correct extension
        name_parts = os.path.splitext(filename)
        filename = f"{name_parts[0]}.{output_format.lower()}"
        
        # Save the image
        output_path = self.output_dir / filename
        
        # Save with appropriate parameters
        save_kwargs = {'quality': self.quality, 'optimize': True}
        if output_format.lower() in ['jpg', 'jpeg']:
            save_kwargs['format'] = 'JPEG'
        elif output_format.lower() == 'png':
            save_kwargs['format'] = 'PNG'
        elif output_format.lower() == 'webp':
            save_kwargs['format'] = 'WEBP'
        
        image.save(output_path, **save_kwargs)
        
        # Get file size
        file_size = output_path.stat().st_size / 1024  # KB
        print(f"✅ Saved: {output_path} ({file_size:.1f} KB)")
        
        return str(output_path)
    
    def batch_extract(self, sources, source_type='url'):
        """
        Extract multiple images from URLs or files.
        
        Args:
            sources (list): List of URLs or file paths
            source_type (str): 'url' or 'file'
            
        Returns:
            list: Paths to saved images
        """
        results = []
        total = len(sources)
        
        print(f"\n{'='*60}")
        print(f"🚀 Batch extracting {total} images from {source_type}s")
        print(f"{'='*60}\n")
        
        for i, source in enumerate(sources, 1):
            print(f"\n[{i}/{total}] Processing: {source}")
            print("-" * 60)
            
            if source_type == 'url':
                result = self.download_from_url(source)
            else:
                result = self.extract_from_file(source)
            
            if result:
                results.append(result)
        
        print(f"\n{'='*60}")
        print(f"✅ Successfully extracted {len(results)}/{total} images")
        print(f"📁 Output directory: {self.output_dir.absolute()}")
        print(f"{'='*60}\n")
        
        return results


def parse_size(size_str):
    """Parse size string like '800x600' into tuple."""
    if not size_str:
        return None
    try:
        width, height = size_str.lower().split('x')
        return (int(width), int(height))
    except:
        return None


def main():
    parser = argparse.ArgumentParser(
        description='Extract and process images from URLs or local files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download from URL
  python image_extractor.py --url "https://example.com/image.jpg"
  
  # Download multiple URLs
  python image_extractor.py --url "url1.jpg" --url "url2.jpg"
  
  # Extract from local file
  python image_extractor.py --file "/path/to/image.jpg"
  
  # Resize and convert to WebP
  python image_extractor.py --url "image.jpg" --resize 800x800 --format webp
  
  # Batch process from file list
  python image_extractor.py --batch urls.txt --type url
        """
    )
    
    # Input sources
    parser.add_argument('--url', '-u', action='append', help='Image URL to download (can be used multiple times)')
    parser.add_argument('--file', '-f', action='append', help='Local image file path (can be used multiple times)')
    parser.add_argument('--batch', '-b', help='File containing list of URLs or paths (one per line)')
    parser.add_argument('--type', '-t', choices=['url', 'file'], default='url', help='Type of sources in batch file (default: url)')
    
    # Output options
    parser.add_argument('--output', '-o', default='./extracted_images', help='Output directory (default: ./extracted_images)')
    parser.add_argument('--resize', '-r', help='Resize images to WIDTHxHEIGHT (e.g., 800x600)')
    parser.add_argument('--format', choices=['jpg', 'jpeg', 'png', 'webp'], help='Convert to specified format')
    parser.add_argument('--quality', '-q', type=int, default=85, help='Image quality 1-100 (default: 85)')
    
    args = parser.parse_args()
    
    # Validate inputs
    if not any([args.url, args.file, args.batch]):
        parser.print_help()
        sys.exit(1)
    
    # Parse resize parameter
    resize = parse_size(args.resize)
    
    # Create extractor
    extractor = ImageExtractor(
        output_dir=args.output,
        resize=resize,
        format=args.format,
        quality=args.quality
    )
    
    # Process sources
    if args.batch:
        # Batch mode
        try:
            with open(args.batch, 'r') as f:
                sources = [line.strip() for line in f if line.strip()]
            extractor.batch_extract(sources, source_type=args.type)
        except FileNotFoundError:
            print(f"❌ Batch file not found: {args.batch}")
            sys.exit(1)
    else:
        # Individual mode
        results = []
        
        if args.url:
            for url in args.url:
                result = extractor.download_from_url(url)
                if result:
                    results.append(result)
        
        if args.file:
            for file_path in args.file:
                result = extractor.extract_from_file(file_path)
                if result:
                    results.append(result)
        
        if results:
            print(f"\n✅ Extracted {len(results)} image(s) to: {extractor.output_dir.absolute()}")
        else:
            print("\n❌ No images were extracted")


if __name__ == '__main__':
    main()
