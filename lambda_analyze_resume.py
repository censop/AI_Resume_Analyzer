import json
import boto3
import os
import urllib.parse
from urllib import request

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        combined_content = response['Body'].read().decode('utf-8')
        
        api_key = os.environ.get('OPENAI_API_KEY')
        url = "https://api.openai.com/v1/chat/completions"
        
        prompt = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system", 
                    "content": "You are a professional recruiter. Review the provided Job Description and Resume Text. Return ONLY JSON with: match_score (int), key_requirements (list), and improvements (text)."
                },
                {
                    "role": "user", 
                    "content": combined_content[:6000] 
                }
            ],
            "response_format": { "type": "json_object" }
        }

        req = request.Request(url, data=json.dumps(prompt).encode('utf-8'), 
                             headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"})
        
        with request.urlopen(req) as res:
            analysis = json.loads(res.read().decode('utf-8'))['choices'][0]['message']['content']

        result_key = key.replace('uploads/', 'results/') + '.json'
        s3.put_object(
            Bucket=bucket,
            Key=result_key,
            Body=analysis,
            ContentType='application/json'
        )

        return {"status": "success"}

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"status": "error", "message": str(e)}
