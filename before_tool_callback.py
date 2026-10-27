"""
Video 5: before_tool_callback implementation
Location: Weather Agent -> Callbacks -> Before Tool Callback
Targets: GetWeatherDetailsUSA
Features:
  1. Validates the tool name 'GetWeatherDetailsUSA'
  2. Sets a live 'Calling tool, please wait' status in session variables
  3. Normalizes coordinate precision (rounds to 4 decimals)
  4. Enforces an enterprise quota (Max 3 weather lookups per session)
"""

import time


def before_tool_callback(tool, args, tool_context, **kwargs):
  """Fires immediately before the OpenAPI tool executes.

  Signature accepts positional arguments cleanly.
  """
  tool_name = getattr(tool, "name", str(tool))
  print(f"[before_tool_callback] 🔍 Intercepting tool: {tool_name}")
  print(f"[before_tool_callback] 📥 Incoming arguments: {args}")

  # 1. Target our specific weather toolset
  if "GetWeatherDetailsUSA" in tool_name or "getWeatherPoint" in tool_name:

    # 2. Status Tracking: Update session variables with status and timestamp
    current_calls = tool_context.variables.get("weather_api_calls", 0) + 1
    tool_context.variables["weather_api_calls"] = current_count = current_calls
    tool_context.variables["tool_status"] = (
        "📡 Contacting National Weather Service API... Please wait."
    )
    tool_context.variables["last_tool_timestamp"] = time.strftime("%H:%M:%S")

    print(
        f"[before_tool_callback] Status updated: Calling GetWeatherDetailsUSA"
        f" (Call #{current_count})"
    )

    # 3. Parameter Normalization: Clean up coordinate precision
    # (Rounding prevents overly long float precision like 32.7766666667)
    if "latitude" in args and "longitude" in args:
      try:
        args["latitude"] = round(float(args["latitude"]), 4)
        args["longitude"] = round(float(args["longitude"]), 4)
        print(
            "[before_tool_callback] 🧹 Normalized coordinates to:"
            f" ({args['latitude']}, {args['longitude']})"
        )
      except (ValueError, TypeError) as e:
        print(f"[before_tool_callback] Parsing warning: {e}")

    # 4. Enterprise Rate Limiting: Cap at 3 weather queries per session
    MAX_ALLOWED_QUERIES = 2
    if current_count > MAX_ALLOWED_QUERIES:
      print(
          f"[before_tool_callback] 🛑 Quota exceeded ({current_count} >"
          f" {MAX_ALLOWED_QUERIES})! Short-circuiting."
      )

      # ⚠️ SHORT-CIRCUIT: Returning a dictionary BYPASSES the real API completely!
      # Gemini will read this result and politely explain the quota to the user.
      return {
          "status": "quota_exceeded",
          "message": (
              f"You have reached the maximum limit of {MAX_ALLOWED_QUERIES}"
              " weather lookups for this session. Please try again in a new"
              " session."
          ),
      }

  # Return None to allow GetWeatherDetailsUSA to execute the real API call!
  return None
