# Set the directory where your images are stored
import os
from PIL import Image
from main import get_indices as main_get_indices
import pandas as pd

images_directory = 'images'  # Change this to your image folder path



def return_indices(results):
    # If results is already a DataFrame, use it directly
    if isinstance(results, pd.DataFrame):
        df = results
    # Handle nested data structure
    elif isinstance(results, dict) and 'data' in results:
        df = pd.DataFrame(results['data'])
    elif hasattr(results, 'columns') and 'data' in results.columns:
        # If data is already in DataFrame format but still nested
        df = pd.DataFrame([eval(x) if isinstance(x, str) else x for x in results['data']])
    else:
        df = pd.DataFrame(results)
    
    print("DataFrame in return_indices:", df.columns.tolist())
    print("First row in return_indices:", df.iloc[0])
    
    df_5, df_10, df_15, df_20, df_25, df_50, df_100 = get_data(df)
    indices, distances = main_get_indices(df_5, df_10, df_15, df_20, df_25, df_50, df_100)
    
    return distances, indices


def get_previous_indices(results, images):
    # If results is already a DataFrame, use it directly
    if isinstance(results, pd.DataFrame):
        df = results
    # Handle nested data structure
    elif isinstance(results, dict) and 'data' in results:
        df = pd.DataFrame(results['data'])
    elif hasattr(results, 'columns') and 'data' in results.columns:
        # If data is already in DataFrame format but still nested
        df = pd.DataFrame([eval(x) if isinstance(x, str) else x for x in results['data']])
    else:
        df = pd.DataFrame(results)
        
    df_5, df_10, df_15, df_20, df_25, df_50, df_100 = get_data(df)
    indices, distances = main_get_indices(df_5, df_10, df_15, df_20, df_25, df_50, df_100)
    
    return distances, indices



