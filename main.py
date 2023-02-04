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
def cf_gpt(request):
    """HTTP Cloud Function.
    example deployment command:
    gcloud functions deploy cf-gpt --source=$(pwd) --trigger-http --runtime=python310 --allow-unauthenticated --gen2 --region=us-central1 --entry-point=cf_gpt --set-env-vars OPENAI_API_KEY={your_key}
    """
    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, PUT, DELETE, HEAD',
            'Access-Control-Allow-Headers': 'custId, appId, Origin, Content-Type, Cookie, X-CSRF-TOKEN, Accept, Authorization, X-XSRF-TOKEN, Access-Control-Allow-Origin',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    # Get the request JSON object
    request_json = request.get_json(silent=True)
    # request_args = request.args

    # Check if the request contains a prompt
    if request_json and 'prompt' in request_json:
        prompt = request_json['prompt']
        response = completions(prompt)
    else:
        # Return a bad request status code if prompt is not provided
        return ('Error no request_json or prompt', 400, headers)

    # Return the completions for the given prompt as a JSON object
    return (json.dumps(response), 200, headers)

