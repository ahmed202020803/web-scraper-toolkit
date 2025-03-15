"""
JSON exporter for the Web Scraper Toolkit.
"""

import json
import logging
import os
from typing import Dict, List, Any, Union

from . import BaseExporter, register_exporter

logger = logging.getLogger(__name__)

@register_exporter("json")
class JSONExporter(BaseExporter):
    """
    Exporter for JSON format.
    
    This exporter saves data to a JSON file.
    """
    
    def export(self, data: Union[Dict[str, Any], List[Dict[str, Any]]], output_path: str) -> None:
        """
        Export data to a JSON file.
        
        Args:
            data (Union[Dict[str, Any], List[Dict[str, Any]]]): The data to export.
            output_path (str): The path where to save the JSON file.
        """
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Data exported to JSON file: {output_path}")
        except Exception as e:
            logger.error(f"Error exporting data to JSON file: {str(e)}")
            raise

    def export_jsonl(self, data: List[Dict[str, Any]], output_path: str) -> None:
        """
        Export data to a JSON Lines file.
        
        Args:
            data (List[Dict[str, Any]]): The data to export.
            output_path (str): The path where to save the JSON Lines file.
        """
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for item in data:
                    f.write(json.dumps(item, ensure_ascii=False) + '\n')
            
            logger.info(f"Data exported to JSON Lines file: {output_path}")
        except Exception as e:
            logger.error(f"Error exporting data to JSON Lines file: {str(e)}")
            raise

    def export_pretty(self, data: Union[Dict[str, Any], List[Dict[str, Any]]], output_path: str) -> None:
        """
        Export data to a pretty-printed JSON file.
        
        Args:
            data (Union[Dict[str, Any], List[Dict[str, Any]]]): The data to export.
            output_path (str): The path where to save the JSON file.
        """
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)
            
            logger.info(f"Data exported to pretty-printed JSON file: {output_path}")
        except Exception as e:
            logger.error(f"Error exporting data to pretty-printed JSON file: {str(e)}")
            raise

    def export_compressed(self, data: Union[Dict[str, Any], List[Dict[str, Any]]], output_path: str) -> None:
        """
        Export data to a compressed JSON file.
        
        Args:
            data (Union[Dict[str, Any], List[Dict[str, Any]]]): The data to export.
            output_path (str): The path where to save the compressed JSON file.
        """
        import gzip
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        try:
            with gzip.open(output_path, 'wt', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)
            
            logger.info(f"Data exported to compressed JSON file: {output_path}")
        except Exception as e:
            logger.error(f"Error exporting data to compressed JSON file: {str(e)}")
            raise