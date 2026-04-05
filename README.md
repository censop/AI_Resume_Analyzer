# Serverless AI Resume Analyzer

A fully serverless web application that securely accepts resume text, evaluates it against a target job description using OpenAI's GPT-4o mini, and returns actionable metrics and a match score.

## Architecture

This project was built to explore event-driven, serverless architecture on AWS. By utilizing S3 Presigned URLs, the application bypasses the need for a traditional backend server to handle file uploads.

1. **Frontend (HTML/JS):** A lightweight, client-side UI.
2. **Lambda 1 (Upload Auth):** Generates secure, short-lived S3 Presigned URLs for direct browser-to-bucket uploads.
3. **Amazon S3:** Acts as the storage layer and the event bus. Uploading a file automatically triggers the next step.
4. **Lambda 2 (AI Analysis):** Wakes up via S3 Event Notifications, reads the combined text file, and sends the payload to the OpenAI API for structured JSON evaluation.

## Technical Features
* **Direct-to-S3 Uploads:** Implemented presigned URLs and S3 CORS configurations to allow the frontend to safely `PUT` files directly into a private bucket.
* **Event-Driven Triggers:** Configured S3 to invoke Lambda functions automatically upon object creation, creating a decoupled, low-latency pipeline.
* **Secure Cloud Polling:** The frontend uses a secondary presigned `GET` URL to securely poll S3 for the final JSON result without exposing the bucket to the public internet.

## Code Structure
* `index.html`: The frontend UI and API polling logic.
* `lambda_generate_url.py`: Generates secure S3 upload and download URLs.
* `lambda_analyze_resume.py`: The S3-triggered function that integrates with OpenAI.
