import os
import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

app = Flask(__name__)

def scrape_images(query, num_images):
    url = f"https://www.google.com/search?tbm=isch&q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    image_elements = soup.find_all("img", limit=num_images + 1)[1:]  # Skip first image as it's usually the logo
    image_urls = [img['src'] for img in image_elements]
    return image_urls

def download_images(image_urls, save_path):
    for i, url in enumerate(image_urls):
        img_response = requests.get(url)
        img = Image.open(BytesIO(img_response.content))
        img.save(os.path.join(save_path, f"image_{i+1}.jpg"))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form['keyword']
        num_images = int(request.form['num_images'])

        # Scrape images using Google search
        image_urls = scrape_images(keyword, num_images)

        # Create a folder on the desktop to save images
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        save_folder = os.path.join(desktop_path, f"{keyword}_images")
        os.makedirs(save_folder, exist_ok=True)

        # Download and save images to the desktop folder
        download_images(image_urls, save_folder)

        return f"Images have been saved to: {save_folder}"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

