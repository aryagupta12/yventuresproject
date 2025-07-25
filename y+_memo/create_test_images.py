#!/usr/bin/env python3
"""
Script to create test images for OCR testing
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_test_image(text, filename, size=(600, 400), bg_color="white", text_color="black"):
    """Create a test image with text"""
    
    # Create image
    img = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a system font, fallback to default
    try:
        # For macOS
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 20)
        title_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
    except:
        try:
            # For Linux
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        except:
            # Fallback to default
            font = ImageFont.load_default()
            title_font = ImageFont.load_default()
    
    # Split text into lines
    lines = text.split('\n')
    y_offset = 30
    
    for i, line in enumerate(lines):
        if i == 0:  # Title line
            draw.text((30, y_offset), line, font=title_font, fill=text_color)
            y_offset += 40
        else:
            draw.text((30, y_offset), line, font=font, fill=text_color)
            y_offset += 30
    
    # Save image
    img.save(filename)
    print(f"Created: {filename}")

def main():
    """Create test images"""
    
    # Test Image 1: Company Overview
    company_overview = """TechFlow Solutions - Company Overview
AI-powered workflow automation platform
Target Market: Mid to large enterprises  
Business Model: SaaS subscription
Founded: 2023
Team Size: 12 employees
Stage: Series A
Revenue: $450K ARR
Burn Rate: $75K/month"""
    
    create_test_image(company_overview, "test_company_overview.png")
    
    # Test Image 2: Financial Data
    financial_data = """Financial Metrics - TechFlow Solutions
Current Cash: $800K
Monthly Burn: $75K/month
Revenue: $450K ARR
Previous Funding: $2.5M Seed
Current Round: $8M Series A
Post-Money Valuation: $35M
Use of Capital: Team expansion, sales scaling"""
    
    create_test_image(financial_data, "test_financial_metrics.png", bg_color="#f0f0f0")
    
    # Test Image 3: Team Information
    team_info = """Founding Team - TechFlow Solutions
CEO: Sarah Chen
Former Google engineering lead, 10+ years experience
Built automation tools at Slack

CTO: Marcus Rodriguez  
Ex-McKinsey consultant, Stanford MBA
Previously scaled sales at Salesforce and Box

Deep expertise in workflow automation and AI/ML"""
    
    create_test_image(team_info, "test_team_info.png", bg_color="#e8f4f8")
    
    print("\n✅ Test images created successfully!")
    print("📸 Files created:")
    print("  - test_company_overview.png")
    print("  - test_financial_metrics.png") 
    print("  - test_team_info.png")
    print("\n🧪 Use these images to test OCR functionality!")

if __name__ == "__main__":
    main() 