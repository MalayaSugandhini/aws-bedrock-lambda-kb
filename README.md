# AWS Bedrock + Lambda + Knowledge Base (Vector Store)  

This project demonstrates how to connect **Amazon Bedrock Knowledge Base** (with S3 Vectors) to an **AWS Lambda function**, allowing you to query your documents with RAG (Retrieval-Augmented Generation).  

---

## Project Overview  
1. Upload documents to an **S3 bucket**.  
2. Create an **S3 Vector Bucket** with an index.  
3. Set up a **Knowledge Base** in Amazon Bedrock.  
4. Create an **IAM Role** with required permissions.  
5. Build an **AWS Lambda function** that queries the Knowledge Base.  
6. Test everything end-to-end.  

---

## 🛠️ Steps to Reproduce  

### 1. Create an S3 Bucket for Documents  
- Go to **Amazon S3** console.  
- Create a **general purpose bucket** (e.g., `my-doc-bucket`).  
- Upload your PDF/Docs (e.g., *Why Bedrock.pdf*).  

📸 *Screenshot:*  

![Screenshot: S3 Bucket with documents](images/s3_docs.png)

## 2. Create a Vector Store  

- Create a new **S3 Vector Bucket** (example: `my-s3-vector-bucket`).  
- Inside it, add a **Vector Index** (example: `test-vector1`).  
- Use the default **dimension size: 1024**.  

📸 Screenshot:  
![Screenshot: Vector bucket with index](images/vector_index.png)


## 3. Create a Knowledge Base  

- In **Amazon Bedrock > Knowledge Bases**, create a new Knowledge Base (example: `vectorkbtest2`).  
- Connect it to the **S3 Vector Store** and the **Vector Index** you created earlier.  
- Select **Titan Text Embeddings v2** for embeddings.  
- Choose your **retrieval model** (example: `Claude 3.5 Haiku`).  
- Sync the documents → you should see a **success ✅** message.  

📸 Screenshot:  
![Screenshot: Knowledge Base setup](images/kb_setup.png)


## 4. Create IAM Role for Lambda  

- Go to **IAM > Roles** in the AWS Console.  
- Create a new role for **Lambda**.  
- Attach the following policies:  
  - `AWSLambdaBasicExecutionRole`  
  - `AmazonBedrockFullAccess`  
  - `AmazonS3ReadOnlyAccess`  

This allows Lambda to:  
- Write logs to **CloudWatch**  
- Read documents from **S3**  
- Query **Amazon Bedrock**  

📸 Screenshot:  
![Screenshot: IAM role with policies](images/iam_role.png)


## 5. Create AWS Lambda Function  

- Go to **AWS Lambda** in the AWS Console.  
- Create a new function.  
- Set **Runtime** to **Python 3.11**.  
- Assign the **IAM role** you created in the previous step.  

📸 Screenshot:  
![Screenshot: Lambda function created](images/lambda_created.png)

### Paste the Lambda Code  

Inside your new Lambda function, replace the default handler with the following code:  

```python
import boto3
import json

# Initialize Bedrock Agent client
bedrock_agent = boto3.client("bedrock-agent-runtime", region_name="us-east-1")

# Replace with your Knowledge Base ID and Model ARN
KB_ID = "YOUR_KNOWLEDGE_BASE_ID"
MODEL_ARN = "YOUR_MODEL_ARN"

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

```

## 6. Test the Lambda  

- In the **Lambda Console**, go to your function.  
- Click **Test** and create a new event.  
- Use the following JSON as the test input:  

```json
{
  "query": "What is Bedrock?"
}
```

## 🧾 Requirements  

- Python 3.11+  
- `boto3` (`pip install boto3`) if testing locally  

---

## ⚡ Deployment Notes  

- No need to package `boto3`, it is already included in AWS Lambda.  
- Use **IAM roles** for security instead of hardcoding access keys.  

---

## 🧹 Clean Up (Avoid Charges 💰)  

After testing, delete the following resources to avoid unnecessary charges:  
- **S3 buckets** (`my-doc-bucket`, `my-s3-vector-bucket`)  
- **Knowledge Base** (`vectorkbtest2`)  
- **Lambda function** (`vectorlambdasearch1`)  
- **IAM role** created for Lambda  

📸 Screenshot:  
![Screenshot: Deleting resources](images/cleanup.png)

---

## 🙌 Credits  

This project was built step-by-step while learning **Amazon Bedrock, S3 Vectors, IAM, and Lambda integration**.
