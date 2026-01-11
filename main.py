import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    print("Hello from ai-agent!")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("API Key could not be found.")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Emable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    response = client.models.generate_content(model="gemini-2.5-flash",
                                              contents=messages, 
                                              config=types.GenerateContentConfig(
                                                  system_instruction=system_prompt,
                                                  temperature=0,
                                                  tools=[available_functions]))

    
    if response.usage_metadata == None:
        raise RuntimeError("Usage metadata was not populated. API request likely failed.")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    function_results = []

    if response.function_calls:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, args.verbose)

            if len(function_call_result.parts) == 0:
                raise Exception("Function call result was returned empty.")
            
            if function_call_result.parts[0].function_response == None:
                raise Exception("Function call did not return a FunctionResponse object.")
            
            if function_call_result.parts[0].function_response.response == None:
                raise Exception("First part of function response was returned empty.")
            
            function_results.append(function_call_result.parts[0])

            resp = function_call_result.parts[0].function_response.response

            if args.verbose:
                result_text = resp.get("result") if isinstance(resp, dict) else resp
                print(f"-> {result_text}")

if __name__ == "__main__":
     main()