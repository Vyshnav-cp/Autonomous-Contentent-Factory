# CopywriterAgent - Quick Start Guide

Get up and running with the CopywriterAgent in 5 minutes.

## 1️⃣ Setup (1 minute)

### Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Set API Key
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

## 2️⃣ Basic Usage (2 minutes)

### Generate Content from Factsheet

```python
from copywriter_agent import CopywriterAgent

# Initialize agent
agent = CopywriterAgent()

# Create a factsheet
factsheet = {
    "product_name": "CloudVault Pro",
    "key_features": [
        "Unlimited cloud storage",
        "Military-grade encryption",
        "Real-time team collaboration",
        "AI-powered file organization"
    ],
    "technical_specs": {
        "storage": "Unlimited",
        "encryption": "AES-256",
        "team_members": "Up to 1000",
        "integrations": "50+"
    },
    "target_audience": "Enterprise teams seeking secure cloud storage",
    "value_proposition": "Secure, scalable cloud storage that enables seamless team collaboration"
}

# Generate all content
result = agent.generate_content(factsheet)

# Access the generated content
print("Blog Post:", result["content"]["blog_post"])
print("\nTweets:", result["content"]["tweet_thread"])
print("\nEmail Teaser:", result["content"]["email_teaser"])
```

## 3️⃣ Try It Now

### Run the Test
```bash
cd backend/agents
python test_copywriter_agent.py
```

### Run Integration Example
```bash
python integration_example.py
```

## 4️⃣ Common Tasks

### Generate Just a Blog Post
```python
result = agent.generate_content(factsheet)
blog = result["content"]["blog_post"]
```

### Generate Just Tweets
```python
result = agent.generate_content(factsheet)
tweets = result["content"]["tweet_thread"]

# Print the tweet thread
for i, tweet in enumerate(tweets, 1):
    print(f"{i}/ {tweet}")
```

### Generate Just Email Teaser
```python
result = agent.generate_content(factsheet)
email = result["content"]["email_teaser"]
```

### Batch Generate for Multiple Products
```python
factsheets = [
    factsheet1,
    factsheet2,
    factsheet3
]

results = agent.generate_batch(factsheets)

for result in results:
    if result["status"] == "success":
        print(f"Generated content for {result['product_name']}")
```

### Combine with ResearchAgent
```python
from research_agent import ResearchAgent
from copywriter_agent import CopywriterAgent

# Analyze raw text
researcher = ResearchAgent()
raw_text = "CloudVault Pro is a secure cloud storage solution..."
research = researcher.analyze(raw_text)

# Generate marketing content
copywriter = CopywriterAgent()
factsheet = {
    "product_name": research["analysis"]["product_name"],
    "key_features": research["analysis"]["key_features"],
    "technical_specs": research["analysis"]["technical_specs"],
    "target_audience": research["analysis"]["target_audience"],
    "value_proposition": research["analysis"]["value_proposition"]
}

content = copywriter.generate_content(factsheet)
```

## 5️⃣ Output Format

The `generate_content()` method returns a dictionary:

```json
{
  "status": "success",
  "timestamp": "2026-04-09T10:30:45.123456",
  "product_name": "CloudVault Pro",
  "content": {
    "blog_post": "500-word professional blog post...",
    "tweet_thread": [
      "1/ Hook tweet...",
      "2/ Value prop tweet...",
      "3/ Features tweet...",
      "4/ Audience tweet...",
      "5/ CTA tweet..."
    ],
    "email_teaser": "Compelling email teaser..."
  },
  "metadata": {
    "model_used": "gpt-4o-mini",
    "blog_word_count": 487,
    "tweet_count": 5,
    "value_proposition": "..."
  }
}
```

## 🎯 Required Factsheet Fields

| Field | Type | Required | Example |
|-------|------|----------|---------|
| `product_name` | string | Yes | "CloudVault Pro" |
| `key_features` | array | Yes | ["Storage", "Encryption"] |
| `target_audience` | string | Yes | "Enterprise teams" |
| `value_proposition` | string | Yes | "Secure cloud storage" |
| `technical_specs` | object | No | {"storage": "Unlimited"} |

## ⚙️ Configuration Options

### Use Different Model
```python
# Use GPT-4 (more capable, slower, more expensive)
agent = CopywriterAgent(model="gpt-4")

# Use GPT-4o Mini (default - faster, cheaper)
agent = CopywriterAgent(model="gpt-4o-mini")
```

### Use Custom API Key
```python
agent = CopywriterAgent(api_key="sk-your-custom-key")
```

## 🐛 Troubleshooting

### Error: "API key not provided"
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

### Error: "Factsheet missing required fields"
Ensure your factsheet has all 4 required fields:
- `product_name`
- `key_features`
- `target_audience`
- `value_proposition`

### Low-Quality Content
Improve your factsheet:
- Make value_proposition more specific
- Add more details to key_features
- Be more specific about target_audience
- Include technical_specs if available

## 📚 Full Documentation

For detailed documentation, see:
- **COPYWRITER_README.md** - Complete guide with all options
- **AGENTS_OVERVIEW.md** - System architecture and integration
- **integration_example.py** - End-to-end example

## 🚀 Next Steps

1. ✅ Run `python test_copywriter_agent.py` to verify setup
2. ✅ Try basic example above
3. ✅ Read COPYWRITER_README.md for advanced options
4. ✅ Integrate into your application
5. ✅ Customize for your use case

## 💡 Tips

- **Start with the test script** to verify everything works
- **Keep value_proposition focused** on customer benefit, not features
- **Use batch_generate** for multiple products to save time
- **Cache factsheets** if you generate content multiple times
- **Monitor costs** - each factsheet uses ~1000 tokens ($0.05-0.10)

## ✅ Checklist

- [ ] API key is set
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Test runs successfully (`python test_copywriter_agent.py`)
- [ ] Can import CopywriterAgent
- [ ] Generated content looks good
- [ ] Integration with ResearchAgent works (optional)

---

**Ready?** Run this now:

```bash
cd backend/agents
python test_copywriter_agent.py
```

Then customize the factsheet above for your product and generate your own content!

---

For questions or issues, check COPYWRITER_README.md or AGENTS_OVERVIEW.md.
