"""
Video 6: after_tool_callback implementation
Location: Weather Agent -> Callbacks -> After Tool Callback
Strips bloated GeoJSON responses down to 4 essential fields before Gemini reads them.
"""


def after_tool_callback(tool, args, tool_context, tool_response, **kwargs):
  """Fires immediately after a tool finishes running,

  before the response is passed back to Gemini.
  """
  tool_name = getattr(tool, "name", str(tool))

  # Target our weather tools
  if "getWeatherPoint" in tool_name or "get_weather_point_info" in tool_name:
    if not isinstance(tool_response, dict):
      return None

    # Drill down into NWS properties
    properties = tool_response.get("properties", tool_response)
    relative_loc = properties.get("relativeLocation", {}).get("properties", {})

    # Extract ONLY the vital fields needed for the user
    trimmed_payload = {
        "city": relative_loc.get("city", "Unknown City"),
        "state": relative_loc.get("state", "USA"),
        "time_zone": properties.get("timeZone", "America/New_York"),
        "forecast_url": properties.get("forecast"),
    }

    # Save the city into session variables for future reference
    tool_context.variables["last_city_checked"] = trimmed_payload["city"]

    print(f"[after_tool_callback] Trimmed 150 lines down to: {trimmed_payload}")

    # Return the clean dictionary to replace the 150-line raw GeoJSON!
    return trimmed_payload

  # Pass through unchanged for any other tool
  return None
