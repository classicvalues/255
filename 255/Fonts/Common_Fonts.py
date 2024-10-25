import os
import requests
import json

# Base directory for fonts
base_dir = "C:\\Artificial_Intelligence\\Fonts"

# Font list API endpoint (for Google Fonts API key usage)
API_KEY = "AIzaSyBGZIVydL2mTzazixiUoVpqhdNv_2t_oUc"
api_url = f"https://www.googleapis.com/webfonts/v1/webfonts?sort=popularity&key={API_KEY}"

# Fetch the list of 100 most popular fonts
response = requests.get(api_url)
fonts = response.json().get("items", [])[:100]  # Limit to 100 fonts

# Function to download font variants
def download_font(font):
    font_name = font["family"].replace(" ", "+")
    font_folder = os.path.join(base_dir, font["family"].replace(" ", "_"))
    
    # Ensure directory exists for each font
    os.makedirs(font_folder, exist_ok=True)

    for variant in font["variants"]:
        variant_url = f"https://fonts.googleapis.com/css2?family={font_name}:wght@{variant}"
        try:
            css_response = requests.get(variant_url)
            css_response.raise_for_status()

            # Find font URL in CSS and download it
            font_url = None
            for line in css_response.text.splitlines():
                if "url(" in line:
                    start = line.find("url(") + 4
                    end = line.find(")", start)
                    font_url = line[start:end].strip("'")

                    if font_url:
                        font_response = requests.get(font_url)
                        font_response.raise_for_status()
                        
                        # Save the font file with variant name
                        font_filename = os.path.join(font_folder, f"{font['family'].replace(' ', '_')}_{variant}.ttf")
                        with open(font_filename, "wb") as font_file:
                            font_file.write(font_response.content)
                        print(f"Downloaded {font['family']} variant {variant} successfully.")

        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred for {font['family']} variant {variant}: {e}")

# Download each font into its respective folder
for font in fonts:
    download_font(font)
