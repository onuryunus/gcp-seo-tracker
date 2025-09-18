from google.adk.agents.callback_context import CallbackContext
from typing import Optional

from google.adk.models import LlmResponse
from google.genai import types # For types.Content



def modify_output_after_agent(callback_context: CallbackContext) -> Optional[types.Content]:
    """
    Logs exit from an agent and checks 'add_concluding_note' in session state.
    If True, returns new Content to *replace* the agent's original output.
    If False or not present, returns None, allowing the agent's original output to be used.
    """
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    current_state = callback_context.state.to_dict()

    print(f"\n[Callback] Exiting agent: {agent_name} (Inv: {invocation_id})")
    print(f"[Callback] Current State: {current_state}")

    if agent_name == 'content_seo_ruler_agent':

        response = callback_context.state["seo_analyze_json_result"]
        print("SEO ANALYZE STATE IN CALLBACK: ", response)

        # Return Content to *replace* the agent's own output
        return types.Content(
            parts=[types.Part(text=response)],
            role="model", # Assign model role to the overriding response
        )

    return None


def simple_after_model_modifier(
    callback_context: CallbackContext, llm_response: LlmResponse
) -> Optional[LlmResponse]:
    """Inspects/modifies the LLM response after it's received."""
    agent_name = callback_context.agent_name
    print(f"[Callback] After model call for agent: {agent_name}")

    # --- Inspection ---
    original_text = ""
    if llm_response.content and llm_response.content.parts:
        # Assuming simple text response for this example
        if llm_response.content.parts[0].text:
            response = callback_context.state["seo_analyze_json_result"]
            print("SEO ANALYZE STATE IN CALLBACK: ", response)
            llm_response.content.parts[0].text = response
            return llm_response
        elif llm_response.content.parts[0].function_call:
             print(f"[Callback] Inspected response: Contains function call '{llm_response.content.parts[0].function_call.name}'. No text modification.")
             return None # Don't modify tool calls in this example
        else:
             print("[Callback] Inspected response: No text content found.")
             return None
    elif llm_response.error_message:
        print(f"[Callback] Inspected response: Contains error '{llm_response.error_message}'. No modification.")
        return None
    else:
        print("[Callback] Inspected response: Empty LlmResponse.")
        return None # Nothing to modify