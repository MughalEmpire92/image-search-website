from flask import Flask, render_template, request, send_file
import requests
import config
import io

app = Flask(__name__)

def search_apis(query):
    images = []
    
    # Unsplash API
    unsplash_url = f"https://api.unsplash.com/search/photos?query={query}&client_id={config.UNSPLASH_KEY}"
    response = requests.get(unsplash_url)
    if response.status_code == 200:
        for img in response.json()['results']:
            images.append({
                'url': img['urls']['regular'],
                'download': img['links']['download'],
                'source': 'Unsplash'
            })
    
    # Pexels API with headers
    pexels_headers = {'Authorization': config.PEXELS_KEY}
    pexels_url = f"https://api.pexels.com/v1/search?query={query}&per_page=15"
    response = requests.get(pexels_url, headers=pexels_headers)
    if response.status_code == 200:
        for img in response.json()['photos']:
            images.append({
                'url': img['src']['large'],
                'download': img['src']['original'],
                'source': 'Pexels'
            })
    
    # Pixabay API
    pixabay_url = f"https://pixabay.com/api/?key={config.PIXABAY_KEY}&q={query}&image_type=photo"
    response = requests.get(pixabay_url)
    if response.status_code == 200:
        for img in response.json()['hits']:
            images.append({
                'url': img['webformatURL'],
                'download': img['largeImageURL'],
                'source': 'Pixabay'
            })
    
    return images

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        query = request.form['query']
        images = search_apis(query)
        return render_template('index.html', images=images, query=query)
    return render_template('index.html')

@app.route('/download')
def download():
    image_url = request.args.get('url')
    response = requests.get(image_url)
    img_bytes = io.BytesIO(response.content)
    return send_file(img_bytes, mimetype='image/jpeg', as_attachment=True, download_name='image.jpg')

if __name__ == '__main__':
    app.run(debug=True)