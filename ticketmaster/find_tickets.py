"""
A script to test out Ticketmaster APIs.
https://developer.ticketmaster.com/products-and-docs/apis/getting-started/
"""

import requests


def find_concerts(api_key, artist_name, city):
    """Find concerts given artist name and city."""
    
    base_url = "https://app.ticketmaster.com/discovery/v2/events"
    
    # Set up parameters for the request
    params = {
        'apikey': api_key,
        'keyword': artist_name,
        'city': city,
        'classificationName': 'music'
    }

    # Build data structure to hold concert info
    found_concerts = {}

    try:
        # Make the request to the Ticketmaster API
        response = requests.get(base_url, params=params)

        # Check for errors in the response
        response.raise_for_status()

        # Parse the response as JSON
        data = response.json()

        # Check if there are any events
        if 'events' in data['_embedded'] and data['_embedded']['events']:
            print("Found concerts.\n")
            for event in data['_embedded']['events']:
                found_concerts[event['id']] = {
                    'name': event['name'],
                    'date': event['dates']['start']['localDate'],
                    'venue': event['_embedded']['venues'][0]['name'],
                    'url': event['url']
                }
            return found_concerts
        else:
            print("No concerts found.")

    except requests.exceptions.RequestException as e:
        print(f"Error making request to Ticketmaster API: {e}")


def find_ticket_availability(api_key, found_concerts):
    """Find ticket availability for each concert given event_ids."""

    event_ids = ','.join(found_concerts.keys())

    base_url = 'https://app.ticketmaster.com/inventory-status/v1/availability?events={universalids}'

    url = base_url.format(universalids=event_ids)

    params = {
        'apikey': api_key
    }

    try:
        # Make the request to the Ticketmaster API
        response = requests.get(url, params=params)

        # Check for errors in the response
        response.raise_for_status()

        # Parse the response as JSON
        concerts = response.json()

        for concert in concerts:
            if found_concerts[concert['eventId']]:
                found_concerts[concert['eventId']]['ticket_status'] = concert['status']
                found_concerts[concert['eventId']]['resale_ticket_status'] = concert['resaleStatus']

        return found_concerts

    except requests.exceptions.RequestException as e:
        print(f"Error making request to Ticketmaster API: {e}")


def format_output_text(concerts):
    """Format output text of concert information to terminal."""

    try:
        for id in concerts:
            print("Name: ", concerts[id]['name'])
            print("Date: ", concerts[id]['date'])
            print("Venue: ", concerts[id]['venue'])
            print("Ticket Status: ", concerts[id]['ticket_status'])
            print("Resale Ticket Status: ", concerts[id]['resale_ticket_status'])
            print("URL: ", concerts[id]['url'])
            print("\n")

    except:
        print("Error trying to format the output.")


api_key = "" # Retrieve from Ticketmaster developer account.
artist_name = "" # Artist name.
city = "" # City name.

found_concerts = find_concerts(api_key, artist_name, city)
found_concerts = find_ticket_availability(api_key, found_concerts)
format_output_text(found_concerts)
