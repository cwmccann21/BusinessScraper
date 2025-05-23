from flask import Blueprint, render_template, jsonify, send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired
import os
from datetime import datetime
from .utils import search_businesses, save_to_excel
from .config import Config

main_bp = Blueprint('main', __name__)

class SearchForm(FlaskForm):
    location = StringField('Location', validators=[DataRequired()], 
                         description='Enter city, state, or address (e.g., "Boston, MA" or "123 Main St, Chicago, IL")')
    keyword = StringField('Business Type', validators=[DataRequired()],
                        description='Enter business type (e.g., restaurant, gym, salon)')
    radius = SelectField('Search Radius', choices=Config.RADIUS_OPTIONS,
                        coerce=int, default=Config.DEFAULT_RADIUS)
    min_rating = SelectField('Minimum Rating', choices=Config.RATING_OPTIONS,
                           coerce=float, default=0)
    business_status = SelectField('Business Status', choices=Config.STATUS_OPTIONS,
                                default='all')
    include_websites = BooleanField('Only Include Businesses with Websites')
    submit = SubmitField('Search')

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        # Get form data
        location = form.location.data
        keyword = form.keyword.data
        radius = form.radius.data
        min_rating = form.min_rating.data
        business_status = form.business_status.data
        include_websites = form.include_websites.data
        
        # Start the search
        results = search_businesses(
            location_query=location,
            keyword=keyword,
            radius=radius,
            min_rating=min_rating,
            business_status=business_status,
            include_websites=include_websites,
            max_results=Config.MAX_RESULTS
        )
        
        if results:
            # Generate unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"business_data_{timestamp}.xlsx"
            filepath = os.path.join(Config.DOWNLOAD_FOLDER, filename)
            
            # Ensure downloads directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Save results
            save_to_excel(results, filepath)
            
            return jsonify({
                'status': 'success',
                'message': f'Found {len(results)} businesses near {location}',
                'download_url': f'/download/{filename}'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': f'No results found near {location} matching your criteria'
            })
    
    return render_template('index.html', form=form)

@main_bp.route('/download/<filename>')
def download(filename):
    return send_from_directory(
        Config.DOWNLOAD_FOLDER,
        filename,
        as_attachment=True
    ) 