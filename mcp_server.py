from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP("TravelTools")

@mcp.tool()
def get_live_weather_forecast(city: str = "Singapore", days: int = 3) -> str:
    """Retrieves current weather conditions and a multi-day forecast for Singapore."""
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude=1.3521&longitude=103.8198"
            f"&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max"
            f"&current_weather=true&timezone=Asia%2FSingapore"
        )
        resp = requests.get(url, timeout=8)
        resp.raise_for_status()
        data = resp.json()
        current = data.get("current_weather", {})
        daily = data.get("daily", {})

        output = [
            f"[Live Data via MCP] Current Singapore Temperature: {current.get('temperature')}°C, Wind: {current.get('windspeed')} km/h.",
            f"[Live Data via MCP] {days}-Day Forecast for Singapore:"
        ]
        for i in range(min(days, len(daily.get("time", [])))):
            date = daily["time"][i]
            t_max = daily["temperature_2m_max"][i]
            rain = daily["precipitation_probability_max"][i]
            advice = "High rain probability (indoor activities advised)" if rain >= 40 else "Low rain probability (suitable for outdoor activities)"
            output.append(f"  • {date}: Max {t_max}°C, Rain Probability {rain}% -> {advice}")
        return "\n".join(output)
    except Exception as e:
        return f"[Live Data via MCP Error]: Unable to retrieve live weather data ({str(e)})."

@mcp.tool()
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert an amount between two currencies using current exchange rates.
    amount: Numeric value to convert.
    from_currency: 3-letter currency code (e.g., USD, INR, SGD, EUR).
    to_currency: 3-letter currency code (e.g., SGD, INR, USD).
    """
    from_cur = from_currency.upper().strip()
    to_cur = to_currency.upper().strip()

    if from_cur == to_cur:
        return f"{amount:.2f} {from_cur} is equal to {amount:.2f} {to_cur}."

    try:
        url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_cur}&to={to_cur}"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        converted = data["rates"][to_cur]
        rate = converted / amount
        return (
            f"Live Conversion: {amount:.2f} {from_cur} = {converted:.2f} {to_cur} "
            f"(Exchange rate: 1 {from_cur} = {rate:.4f} {to_cur})"
        )
    except Exception as e:
        return f"Error: Currency conversion failed for {from_cur} to {to_cur}. Details: {str(e)}"
        
if __name__ == "__main__":
    mcp.run(transport="stdio")
