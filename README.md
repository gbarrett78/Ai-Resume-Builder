# AI-Powered Resume Builder & Pipeline

**Project 20 - Level Up in Tech (LUIT) Program**

An automated CI/CD pipeline that uses Claude AI to convert markdown resumes into ATS-optimized HTML, analyze resume quality, and deploy to AWS S3 with comprehensive tracking.

## 🎯 Project Overview

This project demonstrates end-to-end cloud infrastructure automation with AI integration, combining Infrastructure as Code (IaC), serverless architecture, and AI-powered document processing.

## 🏗️ Architecture
```
resume.md → GitHub Actions → Claude AI → S3 (beta/) → DynamoDB
                ↓
         AI Analysis (ATS Score, Keywords, Readability)
                ↓
         Merge to Main → S3 (prod/)
```

## 🚀 Features

- **AI-Powered Conversion**: Claude Sonnet 4 converts markdown to professional, ATS-optimized HTML
- **Resume Analysis**: Automated ATS scoring, keyword extraction, and readability metrics
- **Beta/Prod Workflow**: Pull requests deploy to beta, merges promote to production
- **Infrastructure as Code**: Complete AWS stack defined in CloudFormation
- **Analytics Tracking**: DynamoDB stores deployment metadata and resume insights

## 🛠️ Technologies Used

- **Cloud**: AWS (S3, DynamoDB, CloudFormation, IAM)
- **CI/CD**: GitHub Actions
- **AI**: Anthropic Claude API (claude-sonnet-4-20250514)
- **Languages**: Python 3.11, YAML
- **IaC**: AWS CloudFormation

## 📋 Infrastructure Components

### CloudFormation Stack (`ResumeStack`)
- **S3 Bucket**: Versioned, public website hosting with beta/prod prefixes
- **DynamoDB Tables**:
  - `cloud-resume-visitors`: Visitor tracking
  - `DeploymentTracking`: CI/CD metadata (commit SHA, environment, model used)
  - `ResumeAnalytics`: ATS scores, keywords, readability metrics
- **IAM Roles/Policies**: Automated deployment permissions

## 📊 Results

**Resume Analysis Metrics:**
- ATS Score: **75/100**
- Readability Score: **82/100**
- Keywords: Technical terms extracted and tracked
- Missing Sections: Identified for improvement

## 🔄 Workflow

### On Pull Request (Beta Deployment)
1. Deploy CloudFormation infrastructure
2. Install Python dependencies (boto3, anthropic)
3. **AI Processing**:
   - Convert `resume.md` → HTML using Claude API
   - Analyze resume quality and generate metrics
4. Upload HTML to `s3://bucket/beta/index.html`
5. Write deployment tracking to DynamoDB
6. Store analytics in DynamoDB

### On Merge to Main (Production Promotion)
1. Copy `beta/index.html` → `prod/index.html`
2. Update deployment status to 'prod'
3. Preserve analytics results

## 🎓 Skills Demonstrated

- Infrastructure as Code (CloudFormation)
- CI/CD Pipeline Design (GitHub Actions)
- AI/ML Integration (Claude API)
- Cloud Architecture (AWS Services)
- Python Scripting & Automation
- DynamoDB Data Modeling
- S3 Website Hosting
- Security & IAM Configuration

## 📝 Setup Instructions

### Prerequisites
- AWS Account with appropriate permissions
- GitHub repository
- Anthropic API key

### GitHub Secrets Required
```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
ANTHROPIC_API_KEY
```

### Deployment
1. Clone repository
2. Add GitHub Secrets
3. Update `resume.md` with your content
4. Create pull request to trigger pipeline
5. Merge to main to promote to production

## Project Timeline

- **Duration**: 3 days (12+ hours)
- **Challenges Overcome**: 
  - S3 bucket naming conflicts
  - CloudFormation template validation
  - API authentication and credit configuration
  - JSON parsing and markdown handling
  - Workflow trigger management

##  Outcomes

-  Fully automated AI-powered resume pipeline
-  Production-grade infrastructure deployment
-  Real-time resume quality analytics
-  Scalable, maintainable architecture
-  Complete documentation and tracking

##  LUIT Program

**Project Number**: 20  
**Cohort**: August 2025  
**Target Completion**: April 2026  
**Status**: Complete 

---

*Built as part of the Level Up in Tech DevOps/Cloud Engineering program*
EOF
