from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from scraper import search_businesses
import os
from dotenv import load_dotenv
import traceback
import csv
from io import StringIO
import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

def convert_to_csv(places):
    output = StringIO()
    writer = csv.writer(output)
    
    # Write headers
    headers = ['Name', 'Address', 'Phone', 'Website', 'Rating', 'Total Reviews', 'Price Level', 'Currently Open']
    writer.writerow(headers)
    
    # Write data
    for place in places:
        row = [
            place.get('Name', 'N/A'),
            place.get('Address', 'N/A'),
            place.get('Phone', 'N/A'),
            place.get('Website', 'N/A'),
            place.get('Rating', 'N/A'),
            place.get('User Ratings Total', 'N/A'),
            place.get('Price Level', 'N/A'),
            'Yes' if place.get('Currently Open') else 'No'
        ]
        writer.writerow(row)
    
    return output.getvalue()

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

@app.route('/export-csv', methods=['POST'])
def export_csv():
    try:
        data = request.get_json()
        if not data or 'results' not in data:
            return jsonify({'error': 'No data provided'}), 400

        # Create a single StringIO buffer
        output = StringIO()
        writer = csv.writer(output)
        
        # Write headers
        headers = ['Name', 'Address', 'Phone', 'Website', 'Rating', 'Total Reviews', 'Price Level', 'Currently Open']
        writer.writerow(headers)
        
        # Write data
        for place in data['results']:
            row = [
                place.get('Name', 'N/A'),
                place.get('Address', 'N/A'),
                place.get('Phone', 'N/A'),
                place.get('Website', 'N/A'),
                place.get('Rating', 'N/A'),
                place.get('User Ratings Total', 'N/A'),
                place.get('Price Level', 'N/A'),
                'Yes' if place.get('Currently Open') else 'No'
            ]
            writer.writerow(row)
        
        # Create filename with timestamp
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"business_results_{timestamp}.csv"
        
        # Reset buffer position
        output.seek(0)
        
        # Create response with explicit headers
        response = send_file(
            output,
            mimetype='text/csv',
            as_attachment=True
        )
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
        
    except Exception as e:
        app.logger.error(f"Error in CSV export: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': 'An error occurred while exporting to CSV'}), 500

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)