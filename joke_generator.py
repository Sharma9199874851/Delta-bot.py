#!/usr/bin/env python3
"""Random Joke Generator."""

import requests

# Joke API URL
API_URL = "https://v2.jokeapi.dev/joke/Any"


def fetch_joke():
    """Fetch a random joke from the JokeAPI."""
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            joke_data = response.json()
            if joke_data['type'] == 'single':
                # Single part joke
                return joke_data['joke']
            elif joke_data['type'] == 'twopart':
                # Two part joke
                return f"{joke_data['setup']} ... {joke_data['delivery']}"
        else:
            return "Failed to fetch joke from API. Please try again later!"
    except Exception as e:
        return f"An error occurred: {e}"


def main():
    """Main function to generate a random joke."""
    print("Fetching a random joke for you...\n")
    joke = fetch_joke()
    print(f"Here's your joke: \n{joke}")


if __name__ == "__main__":
    main()