import os
import yfinance as yf

# List of Nifty50 tickers
TICKERS = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS"]

# Directory to save the CSV files
CSV_DIR = "temp_csv"

def download_nifty50_data():
    """Download Nifty50 stocks data and save it as CSV in the specified folder."""
    # Create the directory if it doesn't exist
    os.makedirs(CSV_DIR, exist_ok=True)
    
    for ticker in TICKERS:
        print(f"Downloading data for {ticker}...")
        # Download the data for the past day with a 5-minute interval
        data = yf.download(ticker, 
                           interval="5m", 
                        period="1d", 
                        #start= "2025-01-02",
                        #end = "2025-01-03",
                           progress=False)
        
        data.rename(columns={"Adj Close":"Adj_Close"}, inplace=True)
        if data.empty:
            print(f"No data found for {ticker}. Skipping.")
            continue
        
        # Replace '.' with '_' in the filename
        file_name = f"{ticker.replace('.', '_')}.csv"
        file_path = os.path.join(CSV_DIR, file_name)
        
        # Save the data to a CSV file
        data.tail(3).to_csv(file_path)
        print(f"Data for {ticker} saved to {file_path}.")

if __name__ == "__main__":
    download_nifty50_data()
