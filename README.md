# CloudFunctionsGPT README
CloudFunctionsGPT is a wrapper framework that has been developed to work in conjunction with OpenAI's GPT-3 technology. This framework allows for the deployment of API services on Google Cloud Functions, providing a seamless integration between these two powerful tools. With CloudFunctionsGPT, developers can take advantage of the advanced natural language processing capabilities of GPT-3 and the scalability and flexibility of Google Cloud Functions to build robust, highly available and efficient API services.

### Deploy
```
gcloud functions deploy model_basic --source=$(pwd) --trigger-http --runtime=python310 --gen2 --region=us-central1 --entry-point=model_basic --set-env-vars OPENAI_API_KEY=key 
```
use `--allow-unauthenticated` if public api is desired.

# Notes
### Permission Issues
https://cloud.google.com/functions/docs/concepts/iam#troubleshooting_permission_errors
