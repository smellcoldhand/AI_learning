# File: get_fact.py

import requests
import json

def fetch_random_fact():
    """
    Connects to the Useless Facts API, fetches a random fact, and displays it.
    """
    # The URL for the API endpoint that provides a random fact in English
    api_url = "https://uselessfacts.jsph.pl/random.json?language=en"
    
    print("Connecting to the Fact Stream... 📡")
    
    try:
        # Make a GET request to the API
        response = requests.get(api_url)
        
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()
        
        # Parse the JSON response into a Python dictionary
        data = response.json()
        
        # Extract the fact text from the dictionary
        fact = data.get('text')
        
        if fact:
            print("\n✅ Success! Here is your fact:")
            print("---------------------------------")
            print(fact)
            print("---------------------------------")
        else:
            print("\n⚠️ Could not find the fact text in the API response.")

    except requests.exceptions.RequestException as e:
        # Handle connection errors, timeouts, etc.
        print(f"\n❌ Error: Could not connect to the API. Reason: {e}")
    except json.JSONDecodeError:
        # Handle cases where the response is not valid JSON
        print("\n❌ Error: Failed to decode the API response.")

if __name__ == "__main__":
    fetch_random_fact()
