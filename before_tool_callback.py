"""
Location: Weather Agent -> Callbacks -> Before Tool Callback
Fixed signature: Accepts positional arguments cleanly!
"""


def before_tool_callback(tool, args, tool_context, **kwargs):
  """Fires immediately before GetWeatherDetailsUSA_getWeatherPoint executes."""
  tool_name = getattr(tool, "name", str(tool))
  print(f"[before_tool_callback] Tool: {tool_name}, Args: {args}")

  if "getWeatherPoint" in tool_name or "get_weather_point_info" in tool_name:
    raw_lat = args.get("latitude")
    raw_lon = args.get("longitude")

    if raw_lat is not None and raw_lon is not None:
      try:
        lat = float(raw_lat)
        lon = float(raw_lon)

        # Continental US cities must be negative longitude
        if lon > 0:
          lon = -abs(lon)
          args["longitude"] = lon
          print(
              f"[before_tool_callback] Auto-corrected longitude to negative:"
              f" {lon}"
          )

        args["latitude"] = lat

      except Exception as e:
        print(f"[before_tool_callback] Conversion error: {e}")

  # ⚠️ Return None so the NWS API tool actually runs!
  return None
