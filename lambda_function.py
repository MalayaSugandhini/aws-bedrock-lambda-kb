import boto3
import json

# Initialize Bedrock Agent client
bedrock_agent = boto3.client("bedrock-agent-runtime", region_name="us-east-1")

# Replace with your Knowledge Base ID and Model ARN
KB_ID = "D0PGXK9NG9"   # your knowledge base ID
MODEL_ARN = "arn:aws:bedrock:us-east-1:248189936723:inference-profile/us.anthropic.claude-3-5-haiku-20241022-v1:0"

def lambda_handler(event, context):
    """
    Lambda entry point.
    Expects input as: { "query": "your question here" }
    """

    try:
        # Extract query from event (or use default)
        query = event.get("query", "What is in my knowledge base?")

        # Call Bedrock Knowledge Base
        response = bedrock_agent.retrieve_and_generate(
            input={"text": query},
            retrieveAndGenerateConfiguration={
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": KB_ID,
                    "modelArn": MODEL_ARN
                },
                "type": "KNOWLEDGE_BASE"
            }
        )

        # Extract answer
        output_text = response.get("output", {}).get("text", "No answer found.")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "query": query,
                "answer": output_text,
                "fullResponse": response
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
