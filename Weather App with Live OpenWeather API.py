
import os
import time
import requests

BASE_URL = "https://api.openweathermap.org/data/2.5"
CACHE_SECONDS = 600  # 10 minutes
cache = {}


def get_api_key():
    """Read the API key from an environment variable."""
    return os.getenv("OPENWEATHER_API_KEY")


def fetch_json(endpoint, city, api_key):
    """Request an endpoint and return its JSON response."""
    response = requests.get(
        f"{BASE_URL}/{endpoint}",
        params={
            "q": city,
            "appid": api_key,
            "units": "metric"
        },
        timeout=10
    )

    if response.status_code == 401:
        raise ValueError(
            "Invalid or inactive API key. Check your key and try again later."
        )
    if response.status_code == 404:
        raise ValueError("City not found. Check the spelling and try again.")

    response.raise_for_status()
    return response.json()


def get_weather(city):
    """Return current weather and forecast, using a short cache."""
    key = city.strip().casefold()
    now = time.time()

    if key in cache and now - cache[key][0] < CACHE_SECONDS:
        return cache[key][1]

    api_key = get_api_key()
    if not api_key:
        raise ValueError(
            "API key missing. Set OPENWEATHER_API_KEY first."
        )

    current = fetch_json("weather", city, api_key)
    forecast = fetch_json("forecast", city, api_key)

    result = {
        "city": current.get("name", city),
        "temperature": current["main"]["temp"],
        "humidity": current["main"]["humidity"],
        "condition": current["weather"][0]["description"],
        "forecast": forecast.get("list", [])[:3]
    }

    cache[key] = (now, result)
    return result


def display_weather(weather):
    """Print current conditions and upcoming forecast entries."""
    print("\n========== WEATHER REPORT ==========")
    print(f"City: {weather['city']}")
    print(f"Temperature: {weather['temperature']:.1f} °C")
    print(f"Humidity: {weather['humidity']}%")
    print(f"Current conditions: {weather['condition'].capitalize()}")

    print("\nShort forecast (next three 3-hour periods):")

    if not weather["forecast"]:
        print("Forecast data is unavailable.")
    else:
        for item in weather["forecast"]:
            date = item.get("dt_txt", "Time unavailable")
            details = item.get("weather", [{}])[0]
            description = details.get("description", "Unknown")
            temperature = item.get("main", {}).get("temp")

            if temperature is not None:
                print(
                    f"{date}: {temperature:.1f} °C, "
                    f"{description}"
                )
            else:
                print(f"{date}: {description}")

    print("====================================")


def main():
    print("Welcome to the Python Weather App!")

    while True:
        city = input(
            "\nEnter a city name, or type 'quit' to exit: "
        ).strip()

        if city.casefold() == "quit":
            print("Goodbye!")
            break

        if not city:
            print("Please enter a city name.")
            continue

        try:
            weather = get_weather(city)
            display_weather(weather)
        except ValueError as error:
            print(f"Error: {error}")
        except requests.Timeout:
            print("The weather service took too long to respond.")
        except requests.ConnectionError:
            print("Could not connect. Check your internet connection.")
        except requests.RequestException as error:
            print(f"Weather API request failed: {error}")
        except (KeyError, IndexError, TypeError, ValueError) as error:
            print(f"Unexpected weather data format: {error}")


if __name__ == "__main__":
    main()
