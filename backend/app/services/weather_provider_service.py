import requests
from datetime import datetime

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
HISTORICAL_WEATHER_URL = (
    "https://archive-api.open-meteo.com/v1/archive"
)

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}

def get_coordinates_for_farm(farm) -> tuple[float, float]:
    location_parts = [
        farm.location,
        farm.village,
        farm.district,
        farm.state,
    ]

    location = ", ".join(
        part.strip()
        for part in location_parts
        if part and part.strip()
    )

    if not location:
        raise ValueError("Farm location is required")

    return get_coordinates(location)
def get_coordinates(location: str) -> tuple[float, float]:
    """
    Convert a farm location into latitude and longitude.
    """

    # Clean known prefix from the farm location.
    cleaned_location = location.strip()

    cleaned_location = cleaned_location.replace(
        "D.Ravulapalem",
        "Ravulapalem",
    )

    cleaned_location = cleaned_location.replace(
        "D. Ravulapalem",
        "Ravulapalem",
    )

    # Try several location formats.
    locations_to_try = [
        cleaned_location,
        "Ravulapalem, Andhra Pradesh",
        "Ravulapalem",
    ]

    # Remove duplicates.
    locations_to_try = list(
        dict.fromkeys(locations_to_try)
    )

    for search_location in locations_to_try:
        response = requests.get(
            GEOCODING_URL,
            params={
                "name": search_location,
                "count": 1,
                "language": "en",
                "format": "json",
            },
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()
        results = data.get("results")

        if results:
            return (
                results[0]["latitude"],
                results[0]["longitude"],
            )

    raise ValueError(
        f"Location not found: {location}"
    )


def get_weather_forecast(
    latitude: float,
    longitude: float,
) -> dict:
    """
    Get current and forecast weather.
    """

    response = requests.get(
        WEATHER_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "precipitation,"
                "wind_speed_10m,"
                "weather_code"
            ),
            "hourly": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "precipitation_probability,"
                "precipitation,"
                "weather_code"
            ),
            "forecast_days": 2,
            "timezone": "auto",
        },
        timeout=10,
    )

    response.raise_for_status()

    return response.json()
def get_tomorrow_weather_forecast(
    latitude: float,
    longitude: float,
) -> dict:
    """
    Get aggregated weather forecast for tomorrow.
    """

    data = get_weather_forecast(
        latitude,
        longitude,
    )

    hourly = data.get("hourly", {})
    times = hourly.get("time", [])

    if not times:
        raise ValueError(
            "Hourly forecast data is unavailable"
        )

    # The first hourly timestamp tells us the provider's
    # local date for the forecast.
    first_date = datetime.fromisoformat(
        times[0]
    ).date()

    tomorrow = first_date

    # If the first forecast date is today, use the next day.
    current_date = datetime.now().date()

    if tomorrow <= current_date:
        from datetime import timedelta

        tomorrow = current_date + timedelta(days=1)

    tomorrow_indices = []

    for index, timestamp in enumerate(times):
        forecast_date = datetime.fromisoformat(
            timestamp
        ).date()

        if forecast_date == tomorrow:
            tomorrow_indices.append(index)

    if not tomorrow_indices:
        raise ValueError(
            "Tomorrow's forecast data is unavailable"
        )

    temperatures = [
        hourly["temperature_2m"][index]
        for index in tomorrow_indices
        if hourly["temperature_2m"][index] is not None
    ]

    humidity_values = [
        hourly["relative_humidity_2m"][index]
        for index in tomorrow_indices
        if hourly["relative_humidity_2m"][index] is not None
    ]

    rainfall_values = [
        hourly["precipitation"][index]
        for index in tomorrow_indices
        if hourly["precipitation"][index] is not None
    ]

    precipitation_probabilities = [
        hourly["precipitation_probability"][index]
        for index in tomorrow_indices
        if hourly["precipitation_probability"][index]
        is not None
    ]

    weather_codes = [
        hourly["weather_code"][index]
        for index in tomorrow_indices
        if hourly["weather_code"][index] is not None
    ]

    if not temperatures:
        raise ValueError(
            "Tomorrow's temperature forecast is unavailable"
        )

    # Use the most frequent weather code for the day.
    weather_code = (
        max(
            set(weather_codes),
            key=weather_codes.count,
        )
        if weather_codes
        else None
    )

    return {
        "date": tomorrow.isoformat(),
        "temperature_min": min(temperatures),
        "temperature_max": max(temperatures),
        "humidity": (
            sum(humidity_values) / len(humidity_values)
            if humidity_values
            else None
        ),
        "rainfall": sum(rainfall_values),
        "precipitation_probability": (
            max(precipitation_probabilities)
            if precipitation_probabilities
            else None
        ),
        "weather_condition": WEATHER_CODES.get(
            weather_code,
            "Unknown",
        ),
    }

def get_current_weather(
    location: str,
) -> dict:
    """
    Get current weather for a farm location.
    """

    latitude, longitude = get_coordinates(
        location
    )

    data = get_weather_forecast(
        latitude,
        longitude,
    )

    current = data["current"]

    weather_code = current.get(
        "weather_code"
    )

    return {
        "temperature": current.get(
            "temperature_2m"
        ),
        "humidity": current.get(
            "relative_humidity_2m"
        ),
        "rainfall": current.get(
            "precipitation"
        ),
        "wind_speed": current.get(
            "wind_speed_10m"
        ),
        "weather_condition": WEATHER_CODES.get(
            weather_code,
            "Unknown",
        ),
    }
def get_historical_weather_summary(
    latitude: float,
    longitude: float,
    start_date: str,
    end_date: str,
) -> dict:
    """
    Get historical weather summary for a location.

    Returns:
        annual rainfall,
        average temperature,
        maximum temperature,
        minimum temperature.
    """

    response = requests.get(
        HISTORICAL_WEATHER_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date,
            "end_date": end_date,
            "daily": (
                "temperature_2m_mean,"
                "temperature_2m_max,"
                "temperature_2m_min,"
                "precipitation_sum"
            ),
            "timezone": "auto",
        },
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    daily = data.get("daily", {})

    mean_temperatures = daily.get(
        "temperature_2m_mean",
        [],
    )

    max_temperatures = daily.get(
        "temperature_2m_max",
        [],
    )

    min_temperatures = daily.get(
        "temperature_2m_min",
        [],
    )

    rainfall_values = daily.get(
        "precipitation_sum",
        [],
    )

    mean_values = [
        value
        for value in mean_temperatures
        if value is not None
    ]

    max_values = [
        value
        for value in max_temperatures
        if value is not None
    ]

    min_values = [
        value
        for value in min_temperatures
        if value is not None
    ]

    rainfall = [
        value
        for value in rainfall_values
        if value is not None
    ]

    if not mean_values:
        raise ValueError(
            "Historical average temperature data is unavailable"
        )

    if not max_values:
        raise ValueError(
            "Historical maximum temperature data is unavailable"
        )

    if not min_values:
        raise ValueError(
            "Historical minimum temperature data is unavailable"
        )

    if not rainfall:
        raise ValueError(
            "Historical rainfall data is unavailable"
        )

    return {
        "annual_rainfall": sum(rainfall),
        "avg_temperature": (
            sum(mean_values)
            / len(mean_values)
        ),
        "max_temperature": max(max_values),
        "min_temperature": min(min_values),
    }