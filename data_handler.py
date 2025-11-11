import pandas as pd
import logging
import numpy as np
import os

logger = logging.getLogger(__name__)

def clean_Data_saveto_exel(csv_path: str) -> pd.DataFrame:
    """
    Clean CSV data and save to Excel format.
    
    Args:
        csv_path (str): Path to the CSV file to clean
        
    Returns:
        pd.DataFrame: Cleaned dataframe
    """
    logger.info(f"Starting data cleaning process for {csv_path}")
    
    try:
        # Read CSV file
        df = pd.read_csv(csv_path)
        
        # Clean data
        clean_df = df.drop_duplicates()
        clean_df = clean_df.replace(r'^\s*$', np.nan, regex=True)
        clean_df = clean_df.dropna()
        
        # Create Excel output path
        dir_path = os.path.dirname(csv_path)
        base_name = os.path.splitext(os.path.basename(csv_path))[0]
        output_file = os.path.join(dir_path, f"{base_name}_cleaned.xlsx")
        
        # Save to Excel
        clean_df.to_excel(output_file, index=False)
        logger.info(f"Cleaned data saved to {output_file}")
        print(f"Cleaned data saved to {output_file}")
        
        return clean_df
        
    except Exception as e:
        logger.error(f"Error cleaning data: {str(e)}")
        print(f"Error cleaning data: {str(e)}")
        return pd.DataFrame()

