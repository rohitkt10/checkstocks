# Stock Price Tracker

A Python-based app to fetch stock prices and check YTD returns. I use the [Alpha Vantage API](https://www.alphavantage.co/) and [Flask](https://flask.palletsprojects.com/en/3.0.x/).

## Installation

Clone the repository and navigate to the project directory:

```sh
git clone https://github.com/rohitkt10/stock-price-tracker.git
cd checkstocks
```

### Configuration
Set up your Alpha Vantage API key as an environment variable:
```sh
export ALPHAVANTAGE_API_KEY=...
```
### Install the required dependencies:
```sh
pip install -r requirements.txt
```

## Running the Application
Start the Flask application:
```sh
python run.py
```
The application will be available at [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

## License
This project is licensed under the MIT License. See the LICENSE file for details.
