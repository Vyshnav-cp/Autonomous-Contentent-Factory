# EditorAgent - Quick Start

Get the EditorAgent validation system running in 3 minutes.

## 1️⃣ Setup

```bash
cd backend
pip install -r requirements.txt
export OPENAI_API_KEY="sk-your-key-here"
```

## 2️⃣ Basic Validation

```python
from editor_agent import EditorAgent

agent = EditorAgent()

# Create factsheet and content
factsheet = {
    "product_name": "CloudVault Pro",
    "key_features": ["Storage", "Encryption", "Collaboration"],
    "technical_specs": {"storage": "Unlimited"},
    "target_audience": "Enterprise teams",
    "value_proposition": "Secure cloud storage for teams"
}

generated_content = {
    "blog_post": "CloudVault Pro is a secure cloud storage...",
    "tweet_thread": ["1/ Tweet...", "2/ Tweet...", ...],
    "email_teaser": "Discover CloudVault Pro..."
}

# Validate
result = agent.validate_content(factsheet, generated_content)

# Check status
print(f"Status: {result['validation']['overall_status']}")
print(f"Confidence: {result['validation']['confidence_score']}%")
```

## 3️⃣ What You Get

**Status**: APPROVED or REJECTED

**For Each Content Type**:
- Accuracy score (0-100)
- Quality rating (EXCELLENT/GOOD/ADEQUATE/POOR)
- Specific issues found
- Improvement suggestions

**Overall Validation**:
- Hallucinations detected
- Confidence score
- Recommendations

## 4️⃣ Approval Criteria

**APPROVED** if:
- ✅ Average accuracy > 70%
- ✅ Less than 3 hallucinations
- ✅ No more than 1 "POOR" rating
- ✅ Value proposition clear

**REJECTED** if:
- ❌ More than 3 hallucinations
- ❌ Average accuracy < 70%
- ❌ Multiple "POOR" ratings
- ❌ Critical compliance issues

## 5️⃣ Common Tasks

### Check Overall Status
```python
status = result["validation"]["overall_status"]
if status == "APPROVED":
    print("Ready for publication")
else:
    print("Needs revision")
```

### Review Hallucinations
```python
hallucinations = result["validation"]["hallucinations_detected"]
for h in hallucinations:
    print(f"Hallucination: {h}")
```

### Get Recommendations
```python
recommendations = result["recommendations"]
for rec in recommendations:
    print(f"→ {rec}")
```

### Check Accuracy Scores
```python
blog_acc = result["validation"]["blog_post_review"]["accuracy_score"]
tweet_acc = result["validation"]["tweet_thread_review"]["accuracy_score"]
email_acc = result["validation"]["email_teaser_review"]["accuracy_score"]

print(f"Blog: {blog_acc}%, Tweets: {tweet_acc}%, Email: {email_acc}%")
```

### Batch Validate Multiple
```python
validations = [
    {"factsheet": fs1, "generated_content": gc1},
    {"factsheet": fs2, "generated_content": gc2}
]

results = agent.batch_validate(validations)

for result in results:
    print(f"Status: {result['validation']['overall_status']}")
```

## 6️⃣ With CopywriterAgent

```python
from copywriter_agent import CopywriterAgent
from editor_agent import EditorAgent

# Generate content
copywriter = CopywriterAgent()
content_result = copywriter.generate_content(factsheet)

# Validate content
editor = EditorAgent()
validation = editor.validate_content(
    factsheet,
    content_result["content"]
)

print(f"Validation: {validation['validation']['overall_status']}")
```

## 7️⃣ Full Pipeline Example

```python
from research_agent import ResearchAgent
from copywriter_agent import CopywriterAgent
from editor_agent import EditorAgent

# Step 1: Analyze
researcher = ResearchAgent()
analysis = researcher.analyze(raw_text)
factsheet = {...}

# Step 2: Generate
copywriter = CopywriterAgent()
content = copywriter.generate_content(factsheet)

# Step 3: Validate
editor = EditorAgent()
validation = editor.validate_content(factsheet, content["content"])

if validation["validation"]["overall_status"] == "APPROVED":
    print("✓ Ready to publish")
else:
    print("✗ Need revision")
```

## 🧪 Test It

```bash
cd backend/agents
python test_editor_agent.py
```

## ⚙️ Configuration

```python
# Use different model
agent = EditorAgent(model="gpt-4")

# Custom API key
agent = EditorAgent(api_key="sk-...")
```

## 📊 Validation Metrics

| Score | Meaning |
|-------|---------|
| 90-100 | Excellent, no issues |
| 70-89 | Good, minor issues |
| 50-69 | Adequate, needs work |
| 0-49 | Poor, major revision needed |

## 💡 Tips

- Provide accurate factsheets (validation quality depends on this)
- Review recommendations if rejected
- Use confidence score to gauge reliability
- Aim for > 90% accuracy across all content types
- Batch validate to save time

## 📖 Full Documentation

See **EDITOR_README.md** for:
- Complete API reference
- All validation metrics
- Integration patterns
- Troubleshooting guide
- Performance details

## ❓ Troubleshooting

**All content rejected?**
- Check factsheet accuracy
- Ensure all fields are filled

**Low confidence?**
- Factsheet may be incomplete
- Generated content may have issues

**API errors?**
- Verify API key
- Check internet connection

---

**Next**: Run `python test_editor_agent.py` to get started!
