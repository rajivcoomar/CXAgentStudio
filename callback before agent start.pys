import base64
import json

# Fallback test token generated from jwt.io (contains userid: 1024, dob: "1990-05-18")
# You can use this for local testing in the Agent Studio simulator!
MOCK_TEST_TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJ1c2VyaWQiOjEwMjQsImRvYiI6IjE5OTAtMDUtMTgiLCJuYW1lIjoiUmFqaXYgQ29vbWFyIn0."
    "4Qp3f-cO_uQpA6i2lD4tS9fU8r7kY-wX1z2A3b4C5dE"
)


def decode_jwt_payload(token: str) -> dict:
  """Decodes the payload section of a JWT token using pure standard library (base64 + json)."""
  try:
    # 1. Split the token into Header, Payload, Signature
    token_parts = token.strip().split(".")
    if len(token_parts) < 2:
      return {}

    payload_b64 = token_parts[1]

    # 2. Add Base64 padding if missing
    rem = len(payload_b64) % 4
    if rem > 0:
      payload_b64 += "=" * (4 - rem)

    # 3. Decode base64url into JSON dictionary
    decoded_bytes = base64.urlsafe_b64decode(payload_b64)
    return json.loads(decoded_bytes.decode("utf-8"))

  except Exception as e:
    print(f"[decode_jwt_payload] Error parsing token: {e}")
    return {}


def before_agent_callback(callback_context):
  """Fires before the agent processes the turn.

  Extracts userid and dob from the auth token and populates session variables.
  """
  # 1. Look for 'auth_token' in the session variables.
  # If not provided by client, fall back to our mock token for testing.
  token = callback_context.variables.get("auth_token", MOCK_TEST_TOKEN)

  if token:
    payload = decode_jwt_payload(token)

    # 2. Extract values from the token payload
    extracted_userid = payload.get("userid")
    extracted_dob = payload.get("dob")
    customer_name = payload.get("name", "Valued Customer")

    # 3. Update the CX Agent Studio session variables directly!
    # (Matches 'userid' and 'dob' declared in your app.json)
    if extracted_userid is not None:
      callback_context.variables["userid"] = extracted_userid

    if extracted_dob is not None:
      callback_context.variables["dob"] = extracted_dob

    print(
        f"[before_agent_callback] Successfully loaded User: {customer_name},"
        f" ID: {extracted_userid}, DOB: {extracted_dob}"
    )

  # Return None to allow the agent to proceed normally with the populated variables
  return None
