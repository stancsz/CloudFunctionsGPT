import functions_framework
import json
import os
import openai

# Set the OpenAI API key to the value of the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")


def completions(model="text-davinci-003",
                prompt="",
                temperature=0.7,
                max_tokens=4000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0):
    """
    Get completions from OpenAI API for given prompt
    """
    # Make an API call to generate completions
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )
    # Return the completions
    return response


@functions_framework.http
def model_basic(request):
    """
    HTTP Cloud Function. Example deployment command:
    gcloud functions deploy cf-gpt --source=$(pwd) --trigger-http --runtime=python310 \
    --allow-unauthenticated --gen2 --region=us-central1 --entry-point=cf_gpt --set-env-vars OPENAI_API_KEY={your_key}
    """
    # Set CORS headers for the preflight request https://cloud.google.com/functions/docs/samples/functions-http-cors
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for a 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, PUT, DELETE, HEAD',
            'Access-Control-Allow-Headers': 'custId, appId, Origin, Content-Type, Cookie, X-CSRF-TOKEN, Accept, '
                                            'Authorization, X-XSRF-TOKEN, Access-Control-Allow-Origin',
            'Access-Control-Max-Age': '3600'
        }

        return '', 204, headers

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    # Get the request JSON object
    request_json = request.get_json(silent=True)
    # request_args = request.args

    # Check if the request contains a prompt
    # if request_json and 'prompt' in request_json:
    try:
        assert request_json['api_token'] and request_json['api_key'] == os.getenv(
            "CUSTOM_API_KEY")
        # CUSTOM_API_KEY is a custom key set by the user, can set up integration with KMS and
        # other auth mechanism.
        assert request_json and 'prompt' in request_json
        prompt = request_json['prompt']
        response = completions('Reply in Chinese. Be verbose. prompt is: ' + prompt)
    # else:
    except Exception as e:
        # Return a bad request status code if prompt is not provided
        return e, 400, headers

    # Return the completions for the given prompt as a JSON object
    return json.dumps(response), 200, headers
