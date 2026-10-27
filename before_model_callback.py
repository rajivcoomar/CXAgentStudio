"""
Video 3: before_model_callback implementation
Location: Read The Manual Bot -> Callbacks -> Before Model Callback
Inspects outgoing prompts for prompt injection / jailbreak attempts.
"""

# List of dangerous patterns to block
BLOCKED_PATTERNS = [
    "ignore previous instructions",
    "ignore all instructions",
    "reveal your prompt",
    "system instructions",
    "jailbreak",
    "dan mode",
]


def before_model_callback(callback_context, llm_request):
  """Fires immediately before the prompt payload is sent to Gemini.

  No google.adk imports needed!
  """
  # 1. Extract the user's latest message from the llm_request contents
  user_text = ""
  if hasattr(llm_request, "contents") and llm_request.contents:
    last_content = llm_request.contents[-1]
    if hasattr(last_content, "parts"):
      for part in last_content.parts:
        if hasattr(part, "text") and part.text:
          user_text = part.text.lower().strip()

  print(f"[before_model_callback] Intercepted prompt: '{user_text}'")

  # 2. Check for security violations
  for pattern in BLOCKED_PATTERNS:
    if pattern in user_text:
      print(f"[before_model_callback] 🚨 Security Threat Detected: '{pattern}'")

      # Track in session variables that an attack was attempted
      callback_context.variables["security_incident"] = True

      # Overwrite the malicious text inside the part with a safe question
      # so the model never sees the attack payload!
      for part in llm_request.contents[-1].parts:
        if hasattr(part, "text"):
          part.text = "Hello, what services do you provide?"

      break

  # Return None to let Gemini proceed with the sanitized request
  return None
