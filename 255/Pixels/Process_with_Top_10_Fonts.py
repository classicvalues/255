import csv
import requests
from collections import Counter
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# Google Fonts API key
API_KEY = "AIzaSyBGZIVydL2mTzazixiUoVpqhdNv_2t_oUc"
FONT_SIZE = 40

# Define output file and paths
OUTPUT_PATH = r"C:\Artificial_Intelligence\Pixels\English_Top_10_Fonts_Main_Pixels\Inter_pixels.csv"
INPUT_FILE = r"C:\Artificial_Intelligence\Tokens\English_Tokens\tokens_part_1.csv"

def get_top_fonts(api_key, count=10):
    print(f"Fetching top {count} fonts from Google Fonts...")
    url = f"https://www.googleapis.com/webfonts/v1/webfonts?key={api_key}&sort=popularity"
    response = requests.get(url)
    if response.status_code == 200:
        font_data = response.json().get("items", [])
        top_fonts = [font["family"] for font in font_data[:count]]
        print(f"Top fonts retrieved: {top_fonts}")
        return top_fonts
    else:
        print(f"Failed to retrieve fonts, status code: {response.status_code}")
        return []

def get_google_font_url(font_name):
    url = f"https://www.googleapis.com/webfonts/v1/webfonts?key={API_KEY}"
    response = requests.get(url)
    font_data = response.json().get("items", [])
    font_url = next((font["files"]["regular"] for font in font_data if font["family"] == font_name), None)
    
    if font_url:
        print(f"Found URL for font '{font_name}': {font_url}")
    else:
        print(f"Font '{font_name}' not found in Google Fonts.")
        
    return font_url

def fetch_font(font_name):
    font_url = get_google_font_url(font_name)
    if font_url:
        response = requests.get(font_url)
        if response.status_code == 200:
            return BytesIO(response.content)
        else:
            print(f"Failed to download font '{font_name}', status code: {response.status_code}.")
    return None

# Aggregate pixel data
def calculate_most_used_pixel(input_file, font_name):
    font_stream = fetch_font(font_name)
    if not font_stream:
        return None

    font = ImageFont.truetype(font_stream, FONT_SIZE)
    pixel_counter = Counter()
    print(f"Processing characters for font: {font_name}")

    # Process each row in the CSV file
    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Read header row
        print(f"Header columns: {headers}")

        for row in reader:
            token = row[0]  # Accessing the Token column (first cell of the row)

            # Use columns 2 to 63 (index 1 to 62) for potential processing
            for col_index in range(1, 63):  # Processing columns 2 to 63 (0-based index)
                if len(row) > col_index:  # Ensure column exists
                    # Optional: You could access other characters here if needed
                    character = row[col_index]  # Accessing the character from the current column
                    # For now, we're focusing on the Token for pixel calculation
                    pass

            # Render character to image based on the token
            img = Image.new("L", (FONT_SIZE, FONT_SIZE), color=255)
            draw = ImageDraw.Draw(img)
            draw.text((10, 5), token, font=font, fill=0)

            # Count pixel occurrences
            pixels = list(img.getdata())
            pixel_counter.update(pixels)

            # Print progress for each token processed
            print(f"Processed token: '{token}', Pixel Count: {len(pixels)}")

    # Find the most used pixel overall
    if pixel_counter:
        most_common_pixel, count = pixel_counter.most_common(1)[0]
        print(f"Most used pixel for '{font_name}': {most_common_pixel} (Count: {count})")
        return most_common_pixel, count
    else:
        print(f"No pixels found for font: {font_name}.")
        return None

# Write aggregated data for each font
top_fonts = get_top_fonts(API_KEY)

with open(OUTPUT_PATH, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Font", "Most Used Pixel", "Pixel Count"])

    for font_name in top_fonts:
        print(f"Calculating most used pixel for font: {font_name}...")
        most_used_pixel, pixel_count = calculate_most_used_pixel(INPUT_FILE, font_name)
        if most_used_pixel is not None:
            writer.writerow([font_name, most_used_pixel, pixel_count])
            print(f"{font_name}: Most Used Pixel = {most_used_pixel}, Count = {pixel_count}")

print("Processing complete. Results saved to:", OUTPUT_PATH)
