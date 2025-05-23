from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from scraper import statewide_search
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

        niche = data.get('niche')
        if not niche:
            return jsonify({'error': 'Niche is required'}), 400

        radius = int(data.get('radius', 50000))
        include_websites = data.get('includeWebsites', False)
        max_results = int(data.get('maxResults', 100))
        
        api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        if not api_key:
            return jsonify({'error': 'API key not configured'}), 500

        places = statewide_search(api_key, niche, radius, max_results, include_websites)
        
        if not places:
            return jsonify({'results': [], 'message': 'No results found'}), 200
            
        return jsonify({'results': places})
    except ValueError as e:
        app.logger.error(f"Value Error: {str(e)}")
        return jsonify({'error': 'Invalid input parameters'}), 400
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