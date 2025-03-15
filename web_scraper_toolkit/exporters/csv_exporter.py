"""
CSV exporter for the Web Scraper Toolkit.
"""

import csv
import logging
import os
from typing import Dict, List, Any, Union, Optional

from . import BaseExporter, register_exporter

logger = logging.getLogger(__name__)

@register_exporter("csv")
class CSVExporter(BaseExporter):
    """
    Exporter for CSV format.
    
    This exporter saves data to a CSV file.
    """
    
    def export(self, data: Union[Dict[str, Any], List[Dict[str, Any]]], output_path: str,
              delimiter: str = ',', quotechar: str = '"', encoding: str = 'utf-8') -> None:
        """
        Export data to a CSV file.
        
        Args:
            data (Union[Dict[str, Any], List[Dict[str, Any]]]): The data to export.
            output_path (str): The path where to save the CSV file.
            delimiter (str, optional): The delimiter to use. Default is ','.
            quotechar (str, optional): The quote character to use. Default is '"'.
            encoding (str, optional): The encoding to use. Default is 'utf-8'.
        """
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        # Convert single dict to list
        if isinstance(data, dict):
            data = [data]
        
        # Check if data is empty
        if not data:
            logger.warning("No data to export")
            with open(output_path, 'w', encoding=encoding, newline='') as f:
                f.write("")
            return
        
        try:
            # Get fieldnames from the first item
            fieldnames = list(data[0].keys())
            
            # Add any additional fields from other items
            for item in data[1:]:
                for key in item.keys():
                    if key not in fieldnames:
                        fieldnames.append(key)
            
            with open(output_path, 'w', encoding=encoding, newline='') as f:
                writer = csv.DictWriter(
                    f, fieldnames=fieldnames, delimiter=delimiter, quotechar=quotechar,
                    quoting=csv.QUOTE_MINIMAL
                )
                
                # Write header
                writer.writeheader()
                
                # Write data
                for item in data:
                    # Convert any non-string values to strings
                    row = {}
                    for key, value in item.items():
                        if isinstance(value, (list, dict)):
                            row[key] = str(value)
                        else:
                            row[key] = value
                    
                    writer.writerow(row)
            
            logger.info(f"Data exported to CSV file: {output_path}")
        except Exception as e:
            logger.error(f"Error exporting data to CSV file: {str(e)}")
            raise
    
    def export_with_pandas(self, data: Union[Dict[str, Any], List[Dict[str, Any]]], output_path: str,
                          index: bool = False, encoding: str = 'utf-8') -> None:
        """
        Export data to a CSV file using pandas.
        
        Args:
            data (Union[Dict[str, Any], List[Dict[str, Any]]]): The data to export.
            output_path (str): The path where to save the CSV file.
            index (bool, optional): Whether to include the index. Default is False.
            encoding (str, optional): The encoding to use. Default is 'utf-8'.
        """
        try:
            import pandas as pd
        except ImportError:
            logger.error("pandas is required for export_with_pandas")
            raise ImportError("pandas is required for export_with_pandas")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        # Convert single dict to list
        if isinstance(data, dict):
            data = [data]
        
        # Check if data is empty
        if not data:
            logger.warning("No data to export")
            with open(output_path, 'w', encoding=encoding, newline='') as f:
                f.write("")
            return
        
        try:
            # Convert to DataFrame
            df = pd.DataFrame(data)
            
            # Export to CSV
            df.to_csv(output_path, index=index, encoding=encoding)
            
            logger.info(f"Data exported to CSV file using pandas: {output_path}")
        except Exception as e:
            logger.error(f"Error exporting data to CSV file using pandas: {str(e)}")
            raise
    
    def export_compressed(self, data: Union[Dict[str, Any], List[Dict[str, Any]]], output_path: str,
                         delimiter: str = ',', quotechar: str = '"', encoding: str = 'utf-8') -> None:
        """
        Export data to a compressed CSV file.
        
        Args:
            data (Union[Dict[str, Any], List[Dict[str, Any]]]): The data to export.
            output_path (str): The path where to save the compressed CSV file.
            delimiter (str, optional): The delimiter to use. Default is ','.
            quotechar (str, optional): The quote character to use. Default is '"'.
            encoding (str, optional): The encoding to use. Default is 'utf-8'.
        """
        import gzip
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        # Convert single dict to list
        if isinstance(data, dict):
            data = [data]
        
        # Check if data is empty
        if not data:
            logger.warning("No data to export")
            with gzip.open(output_path, 'wt', encoding=encoding, newline='') as f:
                f.write("")
            return
        
        try:
            # Get fieldnames from the first item
            fieldnames = list(data[0].keys())
            
            # Add any additional fields from other items
            for item in data[1:]:
                for key in item.keys():
                    if key not in fieldnames:
                        fieldnames.append(key)
            
            with gzip.open(output_path, 'wt', encoding=encoding, newline='') as f:
                writer = csv.DictWriter(
                    f, fieldnames=fieldnames, delimiter=delimiter, quotechar=quotechar,
                    quoting=csv.QUOTE_MINIMAL
                )
                
                # Write header
                writer.writeheader()
                
                # Write data
                for item in data:
                    # Convert any non-string values to strings
                    row = {}
                    for key, value in item.items():
                        if isinstance(value, (list, dict)):
                            row[key] = str(value)
                        else:
                            row[key] = value
                    
                    writer.writerow(row)
            
            logger.info(f"Data exported to compressed CSV file: {output_path}")
        except Exception as e:
            logger.error(f"Error exporting data to compressed CSV file: {str(e)}")
            raise