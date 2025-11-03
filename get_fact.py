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



import json
import os

# Define the file path for your fact archive
FACTS_FILE = 'facts.json'

def load_facts():
    """
    Loads the list of facts from the JSON file.
    If the file doesn't exist, it returns an empty list.
    """
    if not os.path.exists(FACTS_FILE):
        return []  # Return an empty list if the file is not found
    
    # Use 'with' to ensure the file is properly closed
    with open(FACTS_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return [] # Return an empty list if the file is empty or corrupted

def save_facts(facts_list):
    """
    Saves the list of facts to the JSON file.
    'indent=4' makes the file human-readable.
    """
    with open(FACTS_FILE, 'w') as f:
        json.dump(facts_list, f, indent=4)
    print(f"✅ Facts saved successfully to {FACTS_FILE}")

def is_duplicate(new_fact, facts_list):
    """
    Checks if a new fact (based on its 'text' field) already exists in the list.
    """
    for existing_fact in facts_list:
        if existing_fact['text'] == new_fact['text']:
            return True
    return False

def add_fact(fact_text):
    """
    Main function to add a new, unique fact to the archive.
    """
    # 1. Load existing facts
    facts = load_facts()
    
    # 2. Create the new fact object (dictionary)
    # We can add more fields later, like 'source' or 'date_added'
    new_fact = {
        'id': len(facts) + 1, # Simple ID generation
        'text': fact_text
    }
    
    # 3. Check for duplicates
    if is_duplicate(new_fact, facts):
        print(f"⚠️ Duplicate found. Fact '{fact_text}' is already in the archive.")
    else:
        # 4. Add the new fact and save
        facts.append(new_fact)
        save_facts(facts)
        print(f"🚀 New fact added: '{fact_text}'")

# --- Main execution ---
if __name__ == "__main__":
    print("--- Running Fact Archive Test ---")
    
    # --- Test Case 1: Add a new fact ---
    print("\nAttempting to add a new fact...")
    add_fact("The Eiffel Tower can be 15 cm taller during the summer.")

    # --- Test Case 2: Add another new fact ---
    print("\nAttempting to add another new fact...")
    add_fact("A group of flamingos is called a 'flamboyance'.")

    # --- Test Case 3: Add a duplicate fact ---
    print("\nAttempting to add a duplicate fact...")
    add_fact("The Eiffel Tower can be 15 cm taller during the summer.")
    
    print("\n--- Test Complete ---")
    print(f"Check the '{FACTS_FILE}' file to see your archive!")

import requests
import json
import time
import schedule

# --- Configuration ---
API_URL = "https://uselessfacts.jsph.pl/random.json?language=en"
ARCHIVE_FILE = "facts_archive.json"
FETCH_INTERVAL_MINUTES = 1 # Set how often to fetch a new fact (in minutes)

# --- Core Functions (You should already have these) ---

def load_archive(filename):
    """Loads the fact archive from a JSON file."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If file doesn't exist or is empty, start with an empty list
        return []

def save_archive(filename, data):
    """Saves the fact archive to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"✅ Archive updated! Total facts: {len(data)}")

def fetch_fact(url):
    """Fetches a single fact from the API."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        fact_data = response.json()
        return fact_data['text']
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error fetching fact: {e}")
        return None

# --- The Automation Job ---

def collect_new_fact():
    """
    This is the main job function that the scheduler will run.
    It orchestrates fetching, checking for duplicates, and saving.
    """
    print(f"🚀 Running job: Trying to collect a new fact...")
    
    # 1. Load existing facts
    fact_archive = load_archive(ARCHIVE_FILE)
    
    # 2. Fetch a new fact
    new_fact = fetch_fact(API_URL)
    
    if new_fact:
        # 3. Check for duplicates (case-insensitive for robustness)
        is_duplicate = any(new_fact.lower() == existing_fact.lower() for existing_fact in fact_archive)
        
        if not is_duplicate:
            # 4. If unique, add to archive and save
            fact_archive.append(new_fact)
            save_archive(ARCHIVE_FILE, fact_archive)
        else:
            print("💡 Fact is a duplicate. Not adding.")

# --- Scheduler Setup & Execution ---

print("🎯 Automation script started. Press Ctrl+C to exit.")

# Schedule the job to run at the specified interval
schedule.every(FETCH_INTERVAL_MINUTES).minutes.do(collect_new_fact)

# Run the first job immediately without waiting for the first interval
collect_new_fact() 

# Infinite loop to keep the script running and check for scheduled jobs
while True:
    schedule.run_pending()
    time.sleep(1) # Sleep for 1 second to prevent high CPU usage



