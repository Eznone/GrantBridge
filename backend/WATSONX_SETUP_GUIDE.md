# IBM watsonx.ai Setup Guide for GrantBridge

Complete guide for integrating IBM watsonx.ai with GrantBridge for AI-powered features.

## 📋 Overview

GrantBridge uses IBM watsonx.ai for:

- **Grant Matching**: Semantic similarity between organizations and grants
- **Proposal Generation**: AI-assisted proposal writing
- **Text Improvement**: Rewriting, tone adjustment, expansion, summarization
- **Embeddings**: Vector representations for semantic search

## 🚀 Getting Started

### 1. Create IBM Cloud Account

1. Go to [cloud.ibm.com](https://cloud.ibm.com)
2. Click "Create an account" (or sign in)
3. Complete registration
4. Verify email address

### 2. Access watsonx.ai

1. Log in to IBM Cloud
2. Navigate to **Catalog**
3. Search for "watsonx.ai"
4. Click on **watsonx.ai** service
5. Click "Launch watsonx.ai"

### 3. Create Project

1. In watsonx.ai, click "Projects"
2. Click "New project"
3. Fill in details:
   - **Name**: GrantBridge Production
   - **Description**: AI services for grant matching and proposal generation
   - **Storage**: Select or create Cloud Object Storage
4. Click "Create"
5. **Save the Project ID** (you'll need this)

### 4. Get API Credentials

#### Option A: API Key (Recommended)

1. Go to [cloud.ibm.com/iam/apikeys](https://cloud.ibm.com/iam/apikeys)
2. Click "Create"
3. Name: "GrantBridge watsonx.ai"
4. Description: "API key for GrantBridge backend"
5. Click "Create"
6. **Copy and save the API key** (shown only once!)

#### Option B: Service Credentials

1. Go to IBM Cloud Dashboard
2. Find your watsonx.ai service
3. Click "Service credentials"
4. Click "New credential"
5. Copy the `apikey` from the JSON

### 5. Configure GrantBridge

Add to your `.env` file:

```bash
WATSONX_API_KEY=your-api-key-here
WATSONX_PROJECT_ID=your-project-id-here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

**Region URLs:**

- US South: `https://us-south.ml.cloud.ibm.com`
- EU Germany: `https://eu-de.ml.cloud.ibm.com`
- Japan Tokyo: `https://jp-tok.ml.cloud.ibm.com`

## 🧪 Testing the Connection

Create a test script `test_watsonx.py`:

```python
import os
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams

# Configuration
api_key = os.getenv('WATSONX_API_KEY')
project_id = os.getenv('WATSONX_PROJECT_ID')
url = os.getenv('WATSONX_URL')

# Initialize model
model = Model(
    model_id='ibm/granite-13b-chat-v2',
    params={
        GenParams.MAX_NEW_TOKENS: 100,
        GenParams.TEMPERATURE: 0.7,
    },
    credentials={
        'apikey': api_key,
        'url': url
    },
    project_id=project_id
)

# Test generation
prompt = "Write a brief introduction for a grant proposal:"
response = model.generate_text(prompt=prompt)
print("Response:", response)
print("\n✓ watsonx.ai connection successful!")
```

Run the test:

```bash
python test_watsonx.py
```

## 🤖 Available Models

### Foundation Models

| Model                         | Best For                | Max Tokens |
| ----------------------------- | ----------------------- | ---------- |
| `ibm/granite-13b-chat-v2`     | General text generation | 8192       |
| `ibm/granite-13b-instruct-v2` | Instruction following   | 8192       |
| `meta-llama/llama-2-70b-chat` | Complex reasoning       | 4096       |
| `google/flan-ul2`             | Question answering      | 2048       |

### Embedding Models

| Model                                    | Dimensions | Best For                   |
| ---------------------------------------- | ---------- | -------------------------- |
| `ibm/slate-125m-english-rtrvr`           | 768        | English text retrieval     |
| `ibm/slate-30m-english-rtrvr`            | 384        | Faster, smaller embeddings |
| `sentence-transformers/all-MiniLM-L6-v2` | 384        | General purpose            |

## 💡 Implementation Examples

### 1. Grant Matching with Embeddings

```python
from ibm_watson_machine_learning.foundation_models import Embeddings

# Initialize embeddings model
embeddings = Embeddings(
    model_id='ibm/slate-125m-english-rtrvr',
    credentials={'apikey': api_key, 'url': url},
    project_id=project_id
)

# Generate embeddings
org_text = "Education nonprofit serving rural communities"
grant_text = "Funding for education programs in underserved areas"

org_embedding = embeddings.embed_query(org_text)
grant_embedding = embeddings.embed_query(grant_text)

# Calculate similarity (cosine similarity)
from numpy import dot
from numpy.linalg import norm

similarity = dot(org_embedding, grant_embedding) / (
    norm(org_embedding) * norm(grant_embedding)
)
print(f"Match score: {similarity * 100:.1f}%")
```

### 2. Proposal Generation

```python
from ibm_watson_machine_learning.foundation_models import Model

model = Model(
    model_id='ibm/granite-13b-chat-v2',
    params={
        GenParams.MAX_NEW_TOKENS: 500,
        GenParams.TEMPERATURE: 0.7,
        GenParams.TOP_P: 0.9,
    },
    credentials={'apikey': api_key, 'url': url},
    project_id=project_id
)

prompt = """
Write an executive summary for a grant proposal with these details:
- Organization: Education for All Foundation
- Grant: Community Education Grant 2026
- Amount: $50,000
- Focus: Literacy programs in rural areas
- Impact: Serve 500 students

Executive Summary:
"""

summary = model.generate_text(prompt=prompt)
print(summary)
```

### 3. Text Improvement

```python
def improve_text(text, instruction):
    """Improve text based on instruction."""
    prompt = f"""
{instruction}

Original text:
{text}

Improved text:
"""

    model = Model(
        model_id='ibm/granite-13b-instruct-v2',
        params={
            GenParams.MAX_NEW_TOKENS: 300,
            GenParams.TEMPERATURE: 0.5,
        },
        credentials={'apikey': api_key, 'url': url},
        project_id=project_id
    )

    return model.generate_text(prompt=prompt)

# Examples
text = "We need money for our program."

# Make more professional
improved = improve_text(
    text,
    "Rewrite this in a professional, grant-appropriate tone:"
)

# Expand
expanded = improve_text(
    text,
    "Expand this into a detailed paragraph:"
)

# Summarize
summary = improve_text(
    "Long text here...",
    "Summarize this in 2-3 sentences:"
)
```

## 📊 Usage & Pricing

### Free Tier

- **Lite Plan**: Free forever
- **Limits**:
  - 25,000 tokens/month
  - 5 API calls/minute
  - Good for development/testing

### Paid Plans

- **Essentials**: $0.0005 per 1K tokens
- **Standard**: Volume discounts available
- **Enterprise**: Custom pricing

### Token Estimation

- 1 token ≈ 4 characters
- 1 token ≈ 0.75 words
- Average grant description: ~500 tokens
- Average proposal: ~2000 tokens

### Cost Examples

```
Grant matching (100 grants/day):
- 100 grants × 500 tokens = 50K tokens/day
- 50K × 30 days = 1.5M tokens/month
- Cost: ~$0.75/month

Proposal generation (10 proposals/day):
- 10 proposals × 2000 tokens = 20K tokens/day
- 20K × 30 days = 600K tokens/month
- Cost: ~$0.30/month

Total estimated: ~$1-2/month for typical usage
```

## 🔒 Security Best Practices

### API Key Management

```bash
# ✓ DO: Use environment variables
WATSONX_API_KEY=your-key

# ✗ DON'T: Hardcode in code
api_key = "your-key-here"  # NEVER DO THIS
```

### Rate Limiting

```python
import time
from functools import wraps

def rate_limit(calls_per_minute=5):
    """Rate limit decorator for watsonx.ai calls."""
    min_interval = 60.0 / calls_per_minute
    last_called = [0.0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        return wrapper
    return decorator

@rate_limit(calls_per_minute=5)
def generate_text(prompt):
    # Your watsonx.ai call here
    pass
```

### Error Handling

```python
from ibm_watson_machine_learning.wml_client_error import WMLClientError

try:
    response = model.generate_text(prompt)
except WMLClientError as e:
    if 'rate limit' in str(e).lower():
        # Handle rate limit
        time.sleep(60)
        response = model.generate_text(prompt)
    elif 'authentication' in str(e).lower():
        # Handle auth error
        logger.error("Invalid API key")
        raise
    else:
        # Handle other errors
        logger.error(f"watsonx.ai error: {e}")
        raise
```

## 🐛 Troubleshooting

### Common Issues

**Issue**: `Authentication failed`

```bash
# Solution: Check API key
# Verify in IBM Cloud → IAM → API keys
# Regenerate if necessary
```

**Issue**: `Project not found`

```bash
# Solution: Verify project ID
# Go to watsonx.ai → Projects → Your Project
# Copy ID from URL or project settings
```

**Issue**: `Rate limit exceeded`

```bash
# Solution: Implement rate limiting
# Or upgrade to paid plan
# Free tier: 5 calls/minute
```

**Issue**: `Model not available`

```bash
# Solution: Check model ID spelling
# Verify model is available in your region
# Some models require paid plan
```

## 📈 Monitoring

### Track Usage

```python
import logging

logger = logging.getLogger('watsonx')

def log_usage(model_id, tokens_used):
    """Log watsonx.ai usage for monitoring."""
    logger.info(f"Model: {model_id}, Tokens: {tokens_used}")

    # Optional: Send to monitoring service
    # metrics.increment('watsonx.tokens', tokens_used)
```

### Cost Tracking

```python
class WatsonxUsageTracker:
    """Track watsonx.ai usage and costs."""

    def __init__(self):
        self.total_tokens = 0
        self.cost_per_1k_tokens = 0.0005

    def track(self, tokens):
        self.total_tokens += tokens

    @property
    def estimated_cost(self):
        return (self.total_tokens / 1000) * self.cost_per_1k_tokens

    def reset_monthly(self):
        self.total_tokens = 0

tracker = WatsonxUsageTracker()
```

## 🔗 Resources

- **Documentation**: [ibm.com/docs/watsonx](https://www.ibm.com/docs/en/watsonx-as-a-service)
- **API Reference**: [ibm.github.io/watson-machine-learning-sdk](https://ibm.github.io/watson-machine-learning-sdk/)
- **Model Cards**: [dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/fm-models.html](https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/fm-models.html)
- **Pricing**: [ibm.com/products/watsonx-ai/pricing](https://www.ibm.com/products/watsonx-ai/pricing)
- **Support**: [ibm.com/mysupport](https://www.ibm.com/mysupport)

## ✅ Checklist

- [ ] IBM Cloud account created
- [ ] watsonx.ai service accessed
- [ ] Project created and ID saved
- [ ] API key generated and saved
- [ ] Environment variables configured
- [ ] Connection tested successfully
- [ ] Rate limiting implemented
- [ ] Error handling added
- [ ] Usage monitoring set up
- [ ] Cost tracking enabled

---

**Setup Time**: ~15 minutes
**Free Tier**: 25K tokens/month
**Estimated Cost**: $1-5/month for typical usage
