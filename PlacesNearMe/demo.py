from googleplaces import GooglePlaces, types, lang

API_KEY = 'AIzaSyBPGAbevdKkeXaZT0ZsR0qbO30Bpqqm0Mc'

google_places = GooglePlaces(API_KEY)

query_result = google_places.nearby_search(
    location='115 Broad Street, San Francisco',
    radius=1000, types=[types.TYPE_RESTAURANT])

if query_result.has_attributions:
    print(query_result.html_attributions)

for place in query_result.places:
    place.get_details()
    print(place.name)
    print(place.formatted_address + "\n")