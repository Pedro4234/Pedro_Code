import requests

# Alpha Vantage API key
API_KEY = 'QWH7C3KRNZU78TBM'

# Function to fetch stock data from Alpha Vantage
def fetch_stock_data(ticker):
    url = f'https://www.alphavantage.co/query'
    params = {
        'function': 'OVERVIEW',
        'symbol': ticker,
        'apikey': API_KEY
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()

        # Check if the rate limit exceeded
        if 'Note' in data:
            print(f"⚠️ Rate limit exceeded. Please try again later.")
            return None

        # Check if the API returned an error message
        if 'Error Message' in data:
            print(f"⚠️ Error: {data['Error Message']}")
            return None

        # Check if we have stock data
        if 'Symbol' not in data:
            print(f"⚠️ Error fetching data for {ticker}")
            return None

        # Extract stock data
        stock_info = {
            'price': safe_float(data.get('50DayMovingAverage', 0)),
            'eps': safe_float(data.get('EPS', 0)),
            'pe_ratio': safe_float(data.get('PERatio', 0)),
            'dividend_yield': safe_float(data.get('DividendYield', 0)),
            '52w_high': safe_float(data.get('52WeekHigh', 0)),
            '52w_low': safe_float(data.get('52WeekLow', 0)),
            'beta': safe_float(data.get('Beta', 0)),
            'return_on_assets': safe_float(data.get('ReturnOnAssetsTTM', 0)),
            'eps_growth': safe_float(data.get('EPS', 0))  # EPS growth not directly available
        }

        return stock_info

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Network Error: {e}")
        return None
    except ValueError as e:
        print(f"⚠️ JSON Parsing Error: {e}")
        return None
    except Exception as e:
        print(f"⚠️ Unexpected Error: {e}")
        return None

# Safe float conversion to avoid errors with invalid data
def safe_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

# Function to rate a stock based on updated criteria
def rate_stock(stock_info):
    score = 0
    rating_details = {}
    
    # 1. Proximity to 52W Low (5 pts spread out)
    if stock_info['52w_low'] > 0 and stock_info['price'] > 0:
        # Calculate percentage above 52-week low
        percent_above_low = ((stock_info['price'] - stock_info['52w_low']) / stock_info['52w_low']) * 100
        
        # Assign points based on a more granular scale
        if percent_above_low <= 15:  # Within 5% of 52-week low
            proximity_points = 4
        elif percent_above_low <= 20:  # Within 5-10% of 52-week low
            proximity_points = 3
        elif percent_above_low <= 30:  # Within 10-15% of 52-week low
            proximity_points = 2
        elif percent_above_low <= 40:  # Within 15-20% of 52-week low
            proximity_points = 1
        else:  # More than 25% above 52-week low
            proximity_points = 0
    else:
        proximity_points = 0
    
    score += proximity_points
    rating_details['Proximity to 52W Low'] = f"{proximity_points}/4"

    # 2. EPS Growth (Past Year)
    if stock_info['eps_growth'] > 4:
        eps_growth_points = 5
    elif stock_info['eps_growth'] > 3:
        eps_growth_points = 4
    elif stock_info['eps_growth'] > 2:
        eps_growth_points = 3
    elif stock_info['eps_growth'] > 1:
        eps_growth_points = 2
    else:
        eps_growth_points = 1
    score += eps_growth_points
    rating_details['EPS Growth'] = f"{eps_growth_points}/5"

    # 3. PE Ratio
    if stock_info['pe_ratio'] <= 0:
        pe_points = 0
    elif stock_info['pe_ratio'] <= 10:
        pe_points = 5
    elif stock_info['pe_ratio'] <= 15:
        pe_points = 4
    elif stock_info['pe_ratio'] <= 20:
        pe_points = 3
    elif stock_info['pe_ratio'] <= 25:
        pe_points = 2
    elif stock_info['pe_ratio'] <= 30:
        pe_points = 1
    else:
        pe_points = 0
    score += pe_points
    rating_details['PE Ratio'] = f"{pe_points}/5"

    # 4. Dividend Yield (%)
    if stock_info['dividend_yield'] > 2:
        dividend_points = 3
    elif stock_info['dividend_yield'] > 1:
        dividend_points = 2
    elif stock_info['dividend_yield'] > 0:
        dividend_points = 1
    else:
        dividend_points = 0
    score += dividend_points
    rating_details['Dividend Yield'] = f"{dividend_points}/3"

    # 5. Return on Assets (%)
    if stock_info['return_on_assets'] > 20:
        roa_points = 3
    elif stock_info['return_on_assets'] > 10:
        roa_points = 2
    elif stock_info['return_on_assets'] > 5:
        roa_points = 1
    else:
        roa_points = 0
    score += roa_points
    rating_details['Return on Assets'] = f"{roa_points}/3"

    # 6. Beta
    if stock_info['beta'] < 1.25:
        beta_points = 3
    elif stock_info['beta'] < 1.75:
        beta_points = 2
    else:
        beta_points = 1
    score += beta_points
    rating_details['Beta'] = f"{beta_points}/3"

    return score, rating_details

# Function to display stock data side by side
def display_comparison(stock_info1, ticker1, stock_info2, ticker2):
    print(f"\n📊 Stock Comparison: {ticker1} vs {ticker2}")
    print(f"{'Metric':<20} {ticker1:<10} {ticker2:<10}")
    print("-" * 42)
    print(f"{'Price':<20} {stock_info1['price']:<10.2f} {stock_info2['price']:<10.2f}")
    print(f"{'EPS':<20} {stock_info1['eps']:<10.2f} {stock_info2['eps']:<10.2f}")
    print(f"{'P/E Ratio':<20} {stock_info1['pe_ratio']:<10.2f} {stock_info2['pe_ratio']:<10.2f}")
    print(f"{'Dividend Yield (%)':<20} {stock_info1['dividend_yield']:<10.2f} {stock_info2['dividend_yield']:<10.2f}")
    print(f"{'52W High':<20} {stock_info1['52w_high']:<10.2f} {stock_info2['52w_high']:<10.2f}")
    print(f"{'52W Low':<20} {stock_info1['52w_low']:<10.2f} {stock_info2['52w_low']:<10.2f}")
    print(f"{'Beta':<20} {stock_info1['beta']:<10.2f} {stock_info2['beta']:<10.2f}")
    print(f"{'ROA (%)':<20} {stock_info1['return_on_assets']:<10.2f} {stock_info2['return_on_assets']:<10.2f}")
    print(f"{'EPS Growth (%)':<20} {stock_info1['eps_growth']:<10.2f} {stock_info2['eps_growth']:<10.2f}")

# Function to display stock data
def display_stock_data(stock_info, ticker):
    print(f"\n📈 Stock Data for {ticker}:")
    print(f"Price: {stock_info['price']:.2f}")
    print(f"EPS: {stock_info['eps']:.2f}")
    print(f"P/E Ratio: {stock_info['pe_ratio']:.2f}")
    print(f"Dividend Yield (%): {stock_info['dividend_yield']:.2f}")
    print(f"52W High: {stock_info['52w_high']:.2f}")
    print(f"52W Low: {stock_info['52w_low']:.2f}")
    print(f"Beta: {stock_info['beta']:.2f}")
    print(f"Return on Assets (%): {stock_info['return_on_assets']:.2f}")
    print(f"EPS Growth Past Year (%): {stock_info['eps_growth']:.2f}")

# Function to display rating details
def display_rating(rating, rating_details, ticker):
    print(f"\n⭐ Rating for {ticker}: {rating}/20")
    print("\nRating Breakdown:")
    print("-" * 30)
    for criterion, score in rating_details.items():
        print(f"{criterion:<20} {score}")

# Main function
def main():
    print("=== Stock Analysis Tool (Alpha Vantage) ===")
    
    while True:
        print("\n1. View stock data")
        print("2. Compare 2 stocks")
        print("3. Rate a stock")
        print("4. Quit")
        
        try:
            choice = input("Choose an option (1/2/3/4): ").strip()
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

        if choice == '1':
            ticker = input("Enter stock ticker: ").strip().upper()
            stock_info = fetch_stock_data(ticker)
            if stock_info:
                display_stock_data(stock_info, ticker)

        elif choice == '2':
            ticker1 = input("Enter first stock ticker: ").strip().upper()
            ticker2 = input("Enter second stock ticker: ").strip().upper()
            stock_info1 = fetch_stock_data(ticker1)
            stock_info2 = fetch_stock_data(ticker2)
            if stock_info1 and stock_info2:
                display_comparison(stock_info1, ticker1, stock_info2, ticker2)
                
                # Also show and compare ratings
                rating1, details1 = rate_stock(stock_info1)
                rating2, details2 = rate_stock(stock_info2)
                print(f"\nRating: {ticker1}: {rating1}/20 | {ticker2}: {rating2}/20")

        elif choice == '3':
            ticker = input("Enter stock ticker to rate: ").strip().upper()
            stock_info = fetch_stock_data(ticker)
            if stock_info:
                rating, rating_details = rate_stock(stock_info)
                display_rating(rating, rating_details, ticker)

        elif choice == '4':
            print("Goodbye!")
            break

        else:
            print("❌ Invalid option, please try again.")

# Run the main function
if __name__ == "__main__":
    main()