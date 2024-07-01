import json
import requests
import logging
from django.views import View
from django.http import JsonResponse
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = "50e65509ac624eff827200502243006"
API_KEY = os.getenv('API_KEY')

class HelloView(View):
    def get(self, request):
        visitor_name = request.GET.get('visitor_name', 'Guest')

        # Get the client's IP address, handling the case for X-Forwarded-For
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # The header could contain multiple IP addresses, take the first one
            client_ip = x_forwarded_for.split(',')[0].strip()
        else:
            # Fallback to REMOTE_ADDR if no X-Forwarded-For header is present
            client_ip = request.META.get('REMOTE_ADDR')

        logging.info(f"Client IP: {client_ip}")
        print(client_ip)

        response_data = {
            'client_ip': client_ip,
            'location': 'Unknown location',
            'greeting': f"Hello, {visitor_name}!"
        }

        try:
            # Get location using the IP
            location_url = f"http://ip-api.com/json/{client_ip}"
            location_response = requests.get(location_url)
            location_data = location_response.json()  # Parse JSON directly

            logging.info(f"Location response: {location_data}")

            if location_data['status'] == 'success':
                city = location_data.get('city', 'Unknown location')
                response_data['location'] = city

                if city != 'Unknown location':
                    # Use a weather API to get the temperature
                    weather_url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
                    weather_response = requests.get(weather_url)
                    weather_data = weather_response.json()  # Parse JSON directly

                    logging.info(f"Weather response: {weather_data}")

                    if 'current' in weather_data:
                        temperature = weather_data['current']['temp_c']
                        greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}"
                        response_data['greeting'] = greeting
                    else:
                        logging.error(f"Weather data does not contain 'current': {weather_data}")
                        response_data['error'] = "Could not retrieve temperature data."
                else:
                    logging.error("City is unknown, skipping weather API call.")
            else:
                logging.error(f"Location data retrieval failed: {location_data}")
                response_data['error'] = "Could not retrieve location data."

        except requests.exceptions.RequestException as e:
            logging.error(f"RequestException: {e}")
            response_data['error'] = str(e)

        except ValueError as e:
            logging.error(f"ValueError: {e}")
            response_data['error'] = str(e)

        return JsonResponse(response_data)
