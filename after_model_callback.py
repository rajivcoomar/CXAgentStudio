"""
Location: Sales Agent -> Callbacks -> After Model Callback
Scans model output text, masks Date of Birth, and returns the modified llm_response!
"""

import re


def after_model_callback(callback_context, llm_response):
  """Fires immediately after Gemini in the Sales agent produces text."""
  print(
      "[after_model_callback] 🟢 Fired for agent:"
      f" {callback_context.agent_name}"
  )

  # Check if content and parts exist
  if not hasattr(llm_response, "content") or not llm_response.content:
    return None

  # Iterate through the generated parts
  for part in llm_response.content.parts or []:
    if hasattr(part, "text") and part.text:
      original_text = part.text
      print(f"[after_model_callback] Original text: {original_text}")

      # Regex pattern for Date of Birth: YYYY-MM-DD
      dob_pattern = r"(\b\d{4})-(\d{2})-(\d{2}\b)"

      if re.search(dob_pattern, original_text):
        # Mask year and month: 1990-05-18 -> ****-**-18
        masked_text = re.sub(dob_pattern, r"****-**-\3", original_text)
        part.text = masked_text
        print(f"[after_model_callback] ✅ Masked text: {masked_text}")

  # ⚠️ CRITICAL: You MUST return llm_response to apply the changes!
  # If you return None, CX Agent Studio keeps the original unmasked text.
  return llm_response
