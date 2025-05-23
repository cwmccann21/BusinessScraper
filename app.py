from flask import Flask, render_template, request, jsonify
from scraper import statewide_search, save_to_excel
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    niche = data.get('niche')
    radius = int(data.get('radius', 50000))
    include_websites = data.get('includeWebsites', False)
    max_results = int(data.get('maxResults', 100))
    
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key:
        return jsonify({'error': 'API key not configured'}), 500

    try:
        places = statewide_search(api_key, niche, radius, max_results, include_websites)
        return jsonify({'results': places})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)