#!/usr/bin/env python3
"""
Merge auralo-collection (full site with all elements) with working carousels from auralo-desert-collection
"""

# Read the full auralo-collection HTML (with all elements, timers, popups, etc.)
with open('/Users/nelsonchan/Downloads/auralo-desert-collection/index-full.html', 'r', encoding='utf-8') as f:
    full_html = f.read()

# Read our working carousel HTML
with open('/Users/nelsonchan/Downloads/auralo-desert-collection/index.html', 'r', encoding='utf-8') as f:
    carousel_html = f.read()

# Extract the story carousel section from our working version
import re

# Extract story carousel
story_carousel_pattern = r'<!-- Story Carousel Section -->.*?</section>\s*(?=<!-- TikTok Reviews Section -->)'
story_carousel_match = re.search(story_carousel_pattern, carousel_html, re.DOTALL)
if story_carousel_match:
    working_story_carousel = story_carousel_match.group(0)
else:
    print("Warning: Could not find story carousel in working version")
    working_story_carousel = ""

# Extract TikTok carousel  
tiktok_carousel_pattern = r'<!-- TikTok Reviews Section -->.*?</section>\s*(?=<!-- Trustpilot Reviews Section -->)'
tiktok_carousel_match = re.search(tiktok_carousel_pattern, carousel_html, re.DOTALL)
if tiktok_carousel_match:
    working_tiktok_carousel = tiktok_carousel_match.group(0)
else:
    print("Warning: Could not find TikTok carousel in working version")
    working_tiktok_carousel = ""

# Extract Trustpilot carousel
trustpilot_carousel_pattern = r'<!-- Trustpilot Reviews Section -->.*?</section>\s*(?=<!-- Trust & Guarantee Section -->)'
trustpilot_carousel_match = re.search(trustpilot_carousel_pattern, carousel_html, re.DOTALL)
if trustpilot_carousel_match:
    working_trustpilot_carousel = trustpilot_carousel_match.group(0)
else:
    print("Warning: Could not find Trustpilot carousel in working version")
    working_trustpilot_carousel = ""

# Extract carousel JavaScript from working version
carousel_js_pattern = r'// Initialize all carousels with one-at-a-time navigation.*?// Cart functionality'
carousel_js_match = re.search(carousel_js_pattern, carousel_html, re.DOTALL)
if carousel_js_match:
    working_carousel_js = carousel_js_match.group(0)
else:
    print("Warning: Could not find carousel JavaScript in working version")
    working_carousel_js = ""

# Now replace the carousel sections in the full HTML

# Replace story carousel (find the section with "Why This Desert Road Set Exists")
story_section_pattern = r'<section class="story-section"[^>]*>.*?<h2[^>]*>Why This Desert Road Set Exists</h2>.*?</section>'
if re.search(story_section_pattern, full_html, re.DOTALL):
    full_html = re.sub(story_section_pattern, working_story_carousel, full_html, flags=re.DOTALL)
    print("Replaced story carousel section")
else:
    # Try alternative pattern
    story_alt_pattern = r'<!-- Story Carousel Section -->.*?<div class="story-carousel".*?</div>\s*</div>\s*</section>'
    if re.search(story_alt_pattern, full_html, re.DOTALL):
        full_html = re.sub(story_alt_pattern, working_story_carousel, full_html, flags=re.DOTALL)
        print("Replaced story carousel (alt pattern)")
    else:
        # Insert after product section if not found
        product_end = full_html.find('</section>', full_html.find('THE GIRLS WHO WEAR THIS'))
        if product_end > 0:
            full_html = full_html[:product_end+10] + '\n\n' + working_story_carousel + '\n\n' + full_html[product_end+10:]
            print("Inserted story carousel after product section")

# Replace TikTok carousel
tiktok_section_pattern = r'<section[^>]*>.*?<h2[^>]*>What People Are Saying on TikTok</h2>.*?</section>\s*(?=<div class="cta-section"|<section)'
if re.search(tiktok_section_pattern, full_html, re.DOTALL):
    full_html = re.sub(tiktok_section_pattern, working_tiktok_carousel + '\n', full_html, flags=re.DOTALL)
    print("Replaced TikTok carousel section")

# Replace Trustpilot carousel  
trustpilot_section_pattern = r'<section[^>]*>.*?<h2[^>]*>What People Are Saying on Trustpilot</h2>.*?</section>\s*(?=<div class="cta-section"|<section)'
if re.search(trustpilot_section_pattern, full_html, re.DOTALL):
    full_html = re.sub(trustpilot_section_pattern, working_trustpilot_carousel + '\n', full_html, flags=re.DOTALL)
    print("Replaced Trustpilot carousel section")

# Replace the carousel JavaScript initialization
# Find the carousel initialization code and replace it
carousel_init_pattern = r'// Complete carousel system from original Netlify source.*?console\.log\(\'\ud83c\udf89 Complete carousel system initialized!\'\);'
if re.search(carousel_init_pattern, full_html, re.DOTALL):
    full_html = re.sub(carousel_init_pattern, working_carousel_js, full_html, flags=re.DOTALL)
    print("Replaced carousel JavaScript")
else:
    # Try alternative pattern
    alt_js_pattern = r'/\* Carousel script \*/.*?initializeAllCarousels\(\);'
    if re.search(alt_js_pattern, full_html, re.DOTALL):
        full_html = re.sub(alt_js_pattern, working_carousel_js, full_html, flags=re.DOTALL)
        print("Replaced carousel JavaScript (alt pattern)")

# Save the merged HTML
with open('/Users/nelsonchan/Downloads/auralo-desert-collection/index-merged.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

print("\nMerged HTML saved to index-merged.html")
print("This contains ALL elements from auralo-collection (timers, popups, etc.) with working carousels from auralo-desert-collection")