import os
import json

class DataReader:
    """
    Central utility designed to safely handle dynamic JSON parsing for isolated test contexts.
    Maps file targets strictly using the runtime execution module identities.
    """
    
    @staticmethod
    def get_ui_data(testcase_name: str) -> dict:
        """Parses and pulls UI specific data mapped directly to a file matching the testcase naming convention."""
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_path, "test_data", "ui_data", f"{testcase_name}.json")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Missing data mapping configuration file at: {file_path}")
            
        with open(file_path, "r") as stream:
            data = json.load(stream)
        return data.get(testcase_name, {})

    @staticmethod
    def get_api_data(testcase_name: str) -> dict:
        """Parses and pulls API specific data mapped directly to a file matching the testcase naming convention."""
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_path, "test_data", "api_data", f"{testcase_name}.json")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Missing data mapping configuration file at: {file_path}")
            
        with open(file_path, "r") as stream:
            data = json.load(stream)
        return data.get(testcase_name, {})
