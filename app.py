from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from scraper import search_businesses
import os
from dotenv import load_dotenv
import traceback

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        app.logger.error(f"Error rendering index: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        location = data.get('location')
        if not location:
            return jsonify({'error': 'Location is required'}), 400

        niche = data.get('niche')
        if not niche:
            return jsonify({'error': 'Business type is required'}), 400

        radius = int(data.get('radius', 50000))
        include_websites = data.get('includeWebsites', False)
        max_results = int(data.get('maxResults', 100))
        min_rating = float(data.get('minRating', 0))
        open_now = data.get('openNow', False)
        
        api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        if not api_key:
            return jsonify({'error': 'API key not configured'}), 500

        places = search_businesses(
            api_key=api_key,
            location_query=location,
            niche=niche,
            radius=radius,
            max_results=max_results,
            include_websites=include_websites,
            min_rating=min_rating,
            open_now=open_now
        )
        
        if not places:
            return jsonify({'results': [], 'message': 'No results found'}), 200
            
        return jsonify({'results': places})
    except ValueError as e:
        app.logger.error(f"Value Error: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error in search: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': 'An error occurred while processing your request'}), 500

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)