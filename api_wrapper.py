import os
import requests
from dotenv import load_dotenv

class GoogleAPIWrapper:
    def __init__(self, api_key=None):
        """
        Initialize the API wrapper with your Google API key
        :param api_key: Your Google API key (optional if using .env file)
        """
        # Load environment variables from .env file
        load_dotenv()
        
        # Use provided API key or get from environment
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        
        if not self.api_key:
            raise ValueError("API key is required. Either pass it directly or set it in .env file.")

    def create_api_url(self, base_url, endpoint):
        """
        Create a complete API URL with the API key
        :param base_url: The base URL of the API
        :param endpoint: The specific endpoint to call
        :return: Complete URL with API key
        """
        # Make sure the URL ends with '/'
        if not base_url.endswith('/'):
            base_url += '/'
            
        # Remove leading '/' from endpoint if present
        if endpoint.startswith('/'):
            endpoint = endpoint[1:]
            
        # Construct the full URL with the API key
        return f"{base_url}{endpoint}?key={self.api_key}"

    def make_request(self, url, method="GET", data=None):
        """
        Make an HTTP request to the API
        :param url: The complete URL to call
        :param method: HTTP method (GET, POST, etc.)
        :param data: Data to send with the request (for POST, PUT, etc.)
        :return: Response from the API
        """
        try:
            response = requests.request(method, url, json=data)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return None

# Example usage
if __name__ == "__main__":
    # Example API key (replace with your actual key)
    API_KEY = "YOUR_API_KEY"
    
    # Create an instance of the wrapper
    api = GoogleAPIWrapper(API_KEY)
    
    # Example: Creating a URL for the Gemini API
    base_url = "https://generativelanguage.googleapis.com/v1/models/"
    endpoint = "gemini-pro:generateText"
    
    # Get the complete URL
    url = api.create_api_url(base_url, endpoint)
    
    # Make a request (example)
    data = {
        "prompt": {"text": "Hello, how are you?"}
    }
    response = api.make_request(url, method="POST", data=data)
    print(response)
