import os
import json
import boto3
from datetime import datetime
from anthropic import Anthropic

# Initialize clients
dynamodb = boto3.resource("dynamodb")
s3 = boto3.client("s3")
anthropic_client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def convert_markdown_to_html(markdown_content):
    """Use Claude to convert markdown resume to ATS-optimized HTML"""
    message = anthropic_client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[{
            "role": "user",
            "content": f"""Convert this markdown resume into a professional, ATS-optimized HTML document.
            
Requirements:
- Clean, semantic HTML5
- Responsive design with inline CSS
- ATS-friendly formatting (no tables for layout, clear headers)
- Professional styling with good readability
- Include proper meta tags

Markdown Resume:
{markdown_content}

Return ONLY the complete HTML document, no explanation."""
        }]
    )
    return message.content[0].text

def analyze_resume(markdown_content):
    """Use Claude to analyze the resume and return structured JSON"""
    message = anthropic_client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": f"""Analyze this resume and return a JSON object with the following metrics:

{{
  "word_count": <number>,
  "ats_score": <number 0-100>,
  "keywords": [<array of key technical terms>],
  "readability_score": <number 0-100>,
  "missing_sections": [<array of recommended sections to add>],
  "strengths": [<array of strong points>],
  "improvements": [<array of suggested improvements>]
}}

Resume:
{markdown_content}

Return ONLY valid JSON, no explanation."""
        }]
    )
    return json.loads(message.content[0].text)

def write_deployment_tracking(commit_sha, environment, status, s3_url):
    """Write deployment metadata to DynamoDB"""
    table = dynamodb.Table("DeploymentTracking")
    table.put_item(Item={
        "commitSha": commit_sha,
        "environment": environment,
        "status": status,
        "s3Url": s3_url,
        "timestamp": datetime.utcnow().isoformat(),
        "model": "claude-sonnet-4-20250514"
    })

def write_resume_analytics(analytics_data, commit_sha):
    """Write resume analysis to DynamoDB"""
    table = dynamodb.Table("ResumeAnalytics")
    table.put_item(Item={
        "id": commit_sha,
        "timestamp": datetime.utcnow().isoformat(),
        **analytics_data
    })

def main():
    print("Starting resume processing pipeline...")
    
    # Read resume markdown
    with open("resume.md", "r", encoding="utf-8") as f:
        markdown_content = f.read()
    
    print("Converting markdown to HTML...")
    html_content = convert_markdown_to_html(markdown_content)
    
    # Save HTML file
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✓ Generated index.html")
    
    print("Analyzing resume...")
    analytics = analyze_resume(markdown_content)
    print(f"✓ Analysis complete - ATS Score: {analytics.get('ats_score')}")
    
    # Get commit info from environment
    commit_sha = os.environ.get("GITHUB_SHA", "local-test")[:8]
    bucket_name = os.environ.get("BUCKET_NAME", "granville-cloudresume-jan2026")
    
    # Write to DynamoDB
    print("Writing to DynamoDB...")
    s3_url = f"s3://{bucket_name}/beta/index.html"
    write_deployment_tracking(commit_sha, "beta", "success", s3_url)
    write_resume_analytics(analytics, commit_sha)
    print("✓ DynamoDB records written")
    
    print("\n✅ Pipeline complete!")
    print(f"   HTML: index.html")
    print(f"   ATS Score: {analytics.get('ats_score')}/100")
    print(f"   Keywords: {len(analytics.get('keywords', []))}")

if __name__ == "__main__":
    main()
