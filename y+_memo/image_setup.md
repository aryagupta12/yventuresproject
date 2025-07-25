# 🖼️ Image Processing Setup

Your Investment Memo Generator now supports image processing with OCR (Optical Character Recognition)!

## ✅ What's New

- **Image Upload**: Support for PNG, JPG, JPEG, TIFF, BMP files
- **OCR Text Extraction**: Extract text from images, screenshots, charts
- **Auto-Processing**: Images are processed alongside other documents

## 📋 Installation Requirements

### 1. Install Python Dependencies
```bash
pip install pillow pytesseract
```

### 2. Install Tesseract OCR Engine

#### macOS (using Homebrew)
```bash
brew install tesseract
```

#### Ubuntu/Debian
```bash
sudo apt-get install tesseract-ocr
```

#### Windows
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install and add to PATH

#### Verify Installation
```bash
tesseract --version
```

## 🚀 Usage

1. **Upload Images**: Select image files in the file uploader
2. **Extract Text**: Click "Extract Information from Files"
3. **Auto-Process**: Text is extracted and analyzed with your other documents

## 📝 Supported Image Types

- **Screenshots**: Capture text from presentations, documents
- **Charts/Graphs**: Extract data labels and titles
- **Scanned Documents**: Convert scanned pages to text
- **Photos**: Extract any visible text

## ⚠️ Notes

- OCR accuracy depends on image quality and text clarity
- Works best with high-contrast, clear text
- May require manual review for complex layouts
- Processing time varies with image size and complexity

## 🔧 Troubleshooting

**Error: "Image processing libraries not available"**
- Install: `pip install pillow pytesseract`

**Error: "Make sure Tesseract OCR is installed"**
- Install Tesseract OCR for your operating system
- Ensure it's added to your system PATH

**Poor OCR Results**
- Use higher resolution images
- Ensure good contrast between text and background
- Try different image formats (PNG usually works best) 