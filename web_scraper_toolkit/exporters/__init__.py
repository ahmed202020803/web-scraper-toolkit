"""
Data exporters for the Web Scraper Toolkit.
"""

import logging
from typing import Dict, List, Any, Optional, Type, Union

logger = logging.getLogger(__name__)

class BaseExporter:
    """
    Base class for all data exporters.
    
    This class defines the interface that all data exporters must implement.
    """
    
    def export(self, data: Union[Dict[str, Any], List[Dict[str, Any]]], output_path: str) -> None:
        """
        Export data to the specified output path.
        
        Args:
            data (Union[Dict[str, Any], List[Dict[str, Any]]]): The data to export.
            output_path (str): The path where to save the exported data.
        """
        raise NotImplementedError("Subclasses must implement this method")


# Registry of available exporters
_exporters: Dict[str, Type[BaseExporter]] = {}

def register_exporter(name: str):
    """
    Decorator to register an exporter.
    
    Args:
        name (str): The name of the exporter.
    
    Returns:
        Callable: The decorator function.
    """
    def decorator(cls):
        _exporters[name] = cls
        return cls
    return decorator

def get_exporter(name: str) -> BaseExporter:
    """
    Get an instance of the specified exporter.
    
    Args:
        name (str): The name of the exporter.
    
    Returns:
        BaseExporter: An instance of the specified exporter.
    
    Raises:
        ValueError: If the specified exporter is not found.
    """
    # Import exporters here to avoid circular imports
    from .json_exporter import JSONExporter
    from .csv_exporter import CSVExporter
    from .excel_exporter import ExcelExporter
    from .sqlite_exporter import SQLiteExporter
    
    # Normalize name
    name = name.lower()
    
    # Map file extensions to exporter names
    extension_map = {
        "json": "json",
        "csv": "csv",
        "xlsx": "excel",
        "xls": "excel",
        "db": "sqlite",
        "sqlite": "sqlite",
        "sqlite3": "sqlite"
    }
    
    # Map name to exporter name if it's a file extension
    if name in extension_map:
        name = extension_map[name]
    
    if name not in _exporters:
        available_exporters = ", ".join(_exporters.keys())
        raise ValueError(f"Exporter '{name}' not found. Available exporters: {available_exporters}")
    
    exporter_cls = _exporters[name]
    return exporter_cls()