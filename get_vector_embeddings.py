import pandas as pd
import numpy as np

def vector_embedding(df, length):
    # Map of possible column names to standardized names
    column_maps = {
        'open': ['open', 'Open', 'into'],
        'high': ['high', 'High', 'inth'],
        'low': ['low', 'Low', 'intl'],
        'close': ['close', 'Close', 'intc'],
        'volume': ['volume', 'Volume', 'intv']
    }
    
    # Function to get the first available column from possibilities
    def get_column(df, possibilities):
        for col in possibilities:
            if col in df.columns:
                return df[col].values
        raise KeyError(f"None of the columns {possibilities} found in DataFrame")
    
    # Convert data to numpy arrays using flexible column names
    try:
        candle_open = get_column(df, column_maps['open'])
        candle_high = get_column(df, column_maps['high'])
        candle_low = get_column(df, column_maps['low'])
        candle_close = get_column(df, column_maps['close'])
        candle_volume = get_column(df, column_maps['volume'])
        
        # Convert strings to float if necessary
        candle_open = candle_open.astype(float)
        candle_high = candle_high.astype(float)
        candle_low = candle_low.astype(float)
        candle_close = candle_close.astype(float)
        candle_volume = candle_volume.astype(float)
        
        # Calculate candle properties
        candle_body = candle_close - candle_open
        upper_shadow = candle_high - np.maximum(candle_open, candle_close)
        lower_shadow = np.minimum(candle_open, candle_close) - candle_low
        
        # Normalize the data
        def normalize(arr):
            return (arr - np.mean(arr)) / (np.std(arr) if np.std(arr) != 0 else 1)
        
        # Create feature vector
        features = np.concatenate([
            normalize(candle_body),
            normalize(upper_shadow),
            normalize(lower_shadow),
            normalize(candle_volume)
        ])
        
        return features
        
    except Exception as e:
        print(f"Error in vector_embedding: {e}")
        print(f"Available columns: {df.columns.tolist()}")
        print(f"First row: {df.iloc[0]}")
        raise
   