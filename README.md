# Viridian Systems - Business Intelligence Search Tool

A professional web application that helps you find and analyze businesses across the United States using the Google Maps API. This tool allows you to search for specific types of businesses, filter by various criteria, and export the results to Excel.

## Features

- 🔍 Advanced business search with multiple filters
- 📍 Search anywhere in the United States
- ⭐ Filter by rating (3+, 4+, 4.5+ stars)
- 📊 Customizable search radius (1km to 50km)
- 💼 Business status filtering
- 🌐 Website availability filtering
- 📥 Export results to Excel
- 🎨 Modern, responsive UI

## Project Structure

```
project/
├── backend/               # Backend Python package
│   ├── __init__.py       # Flask app initialization
│   ├── config.py         # Configuration settings
│   ├── routes.py         # API routes and form handling
│   └── utils.py          # Business search utilities
├── frontend/             # Frontend assets
│   ├── static/           # Static files
│   │   ├── css/         # Stylesheets
│   │   ├── js/          # JavaScript files
│   │   └── img/         # Images and icons
│   └── templates/        # HTML templates
├── instance/             # Instance-specific files
│   └── downloads/        # Generated Excel files
├── venv/                 # Virtual environment
├── .env                  # Environment variables
├── app.py               # Application entry point
├── README.md            # Project documentation
└── requirements.txt     # Python dependencies
```

## Setup

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:
```env
GOOGLE_MAPS_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here  # For Flask sessions
```

5. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

1. Enter a location (city, state, or specific address)
2. Specify the type of business you want to find
3. Customize your search:
   - Select search radius (1km to 50km)
   - Choose minimum rating requirement
   - Filter by business status
   - Option to include only businesses with websites
4. Click "Search" and wait for results
5. Download the Excel file containing your results

## API Fields Retrieved

For each business, we collect:
- Business name
- Address
- Phone number
- Website (if available)
- Email (if available)
- Opening hours
- Rating
- Business status
- Price level
- Google Maps URL

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## About Viridian Systems

Viridian Systems specializes in developing advanced business intelligence tools that help organizations make data-driven decisions. Our tools combine modern design with powerful functionality to deliver exceptional user experiences. 