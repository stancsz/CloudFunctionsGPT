import functions_framework
import json
import os
import openai

# Set the OpenAI API key to the value of the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def completions(prompt=""):
    """
    Get completions from OpenAI API for given prompt
    """
    # Make an API call to generate completions
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=4000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # Return the completions
    return response

@functions_framework.http
def get_price_targets(request):
    """HTTP Cloud Function.
    """
    # Get the request JSON object
    request_json = request.get_json(silent=True)
    request_args = request.args

    # Check if the request contains a prompt
    if request_json and 'prompt' in request_json:
        prompt = request_json['prompt']
    else:
        # Return a bad request status code if prompt is not provided
        return 400

    # Return the completions for the given prompt as a JSON object
    return json.dumps(completions(prompt))
