def after_agent_callback(
    callback_context: CallbackContext,
) -> Optional[Content]:
  """Attached to the 'Sales' sub-agent.

  Uses a one-time guard to ensure the notice is delivered exactly ONCE.
  """
  # 1. GUARD: If already sent during this session, DO NOT send it again!
  if callback_context.variables.get("qa_disclosure_sent", False):
    return None

  # 2. Mark as sent immediately
  callback_context.variables["qa_disclosure_sent"] = True

  # 3. Deliver the QA notice
  qa_notice = (
      "📞 **Call Concluded**\n\n"
      "Please note: This interaction was recorded and monitored for "
      "quality assurance and compliance purposes. "
      "Thank you for contacting Healthcare Sales Support!"
  )

  try:
    return Content(parts=[Part(text=qa_notice)])
  except Exception:
    return Content(text=qa_notice)
