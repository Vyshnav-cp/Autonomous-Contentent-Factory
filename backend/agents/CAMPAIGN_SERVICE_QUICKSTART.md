# CampaignService Quick Start (5 minutes)

Get your first campaign running in 5 minutes.

## Step 1: Setup (1 minute)

```bash
# Set your API key
export OPENAI_API_KEY="sk-your-key-here"
```

## Step 2: Create Your First Campaign (2 minutes)

```python
from campaign_service import CampaignService

# Initialize the service
service = CampaignService()

# Your product text
product_text = """
CloudVault Pro is an enterprise cloud storage solution.
Features: 500GB storage, AES-256 encryption, real-time collaboration
Tech: AWS-backed, 99.99% uptime SLA
Target: Mid-market teams (10-100 people)
Value: Secure, affordable, reliable team storage
"""

# Create campaign
campaign = service.create_campaign(product_text)
```

## Step 3: Check Results (1 minute)

```python
# Status
print(f"Status: {campaign['campaign_status']}")
print(f"Confidence: {campaign['validation']['confidence_score']}%")

# Access content
blog = campaign['content']['blog_post']
tweets = campaign['content']['tweet_thread']
email = campaign['content']['email_teaser']

print(f"\n📝 Blog ({len(blog)} chars)")
print(f"🐦 Tweets ({len(tweets)} tweets)")
print(f"📧 Email ({len(email)} chars)")
```

## Step 4: Export (1 minute)

```python
# Export as JSON (for APIs)
json_data = service.export_campaign(campaign, format="json")

# Export as Markdown (for docs)
md_data = service.export_campaign(campaign, format="markdown")

# Export as Plain Text (for email)
txt_data = service.export_campaign(campaign, format="plain")

# Save to file
with open("campaign.md", "w") as f:
    f.write(md_data)
```

## That's It! 🎉

Your campaign is ready to use.

### What You Got
- ✅ 500-word blog post (professional tone)
- ✅ 5-tweet thread (engaging tone)
- ✅ 1-paragraph email teaser
- ✅ Quality validation feedback
- ✅ Actionable recommendations

### Next Steps
- Review the campaign output
- Make any edits as recommended
- Publish to your platforms
- Track performance

## Common Tasks

### Process Multiple Products
```python
products = [
    {"name": "Product A", "text": "Description A..."},
    {"name": "Product B", "text": "Description B..."}
]

campaigns = service.create_campaign_batch(products)
```

### Check Campaign Status
```python
# APPROVED = ready to publish
# NEEDS_REVISION = minor fixes needed
# REJECTED = major rework needed

status = campaign['campaign_status']
```

### Get Recommendations
```python
for rec in campaign['recommendations']:
    print(f"• {rec}")
```

## Troubleshooting

**API Key Error?**
```bash
export OPENAI_API_KEY="sk-..."
```

**Campaign Failed?**
```python
if campaign['status'] != 'success':
    print(campaign.get('error'))
```

**Want More Details?**
See [CAMPAIGN_SERVICE_README.md](./CAMPAIGN_SERVICE_README.md) for complete documentation.

---

That's all you need to get started! 🚀
