# Architecture & Design - OpenAI Client Wrapper

## System Design

```
┌─────────────────────────────────────────────────────────┐
│                   Application Layer                      │
│  (ResearchAgent, FastAPI routes, etc.)                  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│          OpenAI Client Wrapper (Main Module)            │
│                 openai_client.py                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  generate_response(prompt, ...)  [Convenience]   │  │
│  │  get_default_client()            [Singleton]     │  │
│  │  OpenAIClientWrapper             [Class-based]   │  │
│  └───────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│            OpenAI Python SDK (openai)                   │
│          https://github.com/openai/openai-python      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│          OpenAI API (Remote Service)                    │
│  https://api.openai.com/v1/chat/completions           │
└─────────────────────────────────────────────────────────┘
```

## Class Hierarchy

```
OpenAIClientWrapper
├── __init__(api_key, model)
├── generate_response(prompt, temperature, max_tokens, system_prompt)
├── generate_response_with_context(prompt, context, ...)
├── set_model(model)
└── get_model()

Module Functions
├── generate_response(...)       [Wrapper around default client]
├── get_default_client()         [Singleton pattern]
└── main()                       [Demo/testing]
```

## Data Flow

### Request Flow
```
User Input (prompt)
        │
        ▼
generate_response(prompt, ...)
        │
        ▼
OpenAIClientWrapper.generate_response()
        │
        ├─ Validate input (non-empty prompt)
        ├─ Build messages array (system + user prompts)
        │
        ▼
client.chat.completions.create()
        │
        ▼
OpenAI API (HTTP POST to /v1/chat/completions)
        │
        ▼
Response (ChatCompletion object)
        │
        ▼
response.choices[0].message.content
        │
        ▼
Return string to caller
```

### Message Structure
```
messages = [
    {
        "role": "system",
        "content": "You are an expert. Be concise."  # Optional
    },
    {
        "role": "user",
        "content": "Your actual prompt here"
    }
]
```

## Configuration Hierarchy

```
Environment Variables (Highest Priority)
    ↓
Constructor Parameters
    ↓
Hardcoded Defaults (Lowest Priority)

Example: API Key Resolution
─────────────────────────────
1. Constructor api_key parameter: OpenAIClientWrapper(api_key="sk-custom")
2. Environment variable: export OPENAI_API_KEY="sk-env"
3. Error if neither provided
```

## Error Handling Strategy

```
generate_response(prompt)
        │
        ├─ ValueError: prompt is empty/whitespace
        │   └─ Client-side validation
        │
        ├─ ValueError: API key not provided
        │   └─ Configuration validation
        │
        ├─ json.JSONDecodeError: Invalid API response
        │   └─ Response parsing error
        │
        ├─ Exception: Rate limit, quota exceeded, etc.
        │   └─ API error (transient or permanent)
        │
        └─ Return response string on success
```

## Temperature Parameter Effect

```
Temperature Setting     Output Behavior
──────────────────────────────────────
0.0 (Min)        ▁▁▁ Deterministic, focused
0.3              ▂▂▂ Analytical, consistent
0.7 (Default)    ▄▄▄ Balanced approach
1.0              ▅▅▅ More variety
1.5              ▇▇▇ Creative, exploratory
2.0 (Max)        █████ Random, unpredictable
```

## Token Budget Illustration

```
Total Request (max_tokens = 500)
│
├─ Input Tokens
│  └─ System prompt + user prompt = ~50 tokens
│
└─ Output Tokens
   └─ Remaining budget = ~450 tokens for response
   
Cost = (input_tokens + output_tokens) × price_per_token
```

## Concurrency Model

```
Current: Sequential Processing
─────────────────────────────
Request 1 ──→ Process ──→ Response 1
Request 2 ──→ Process ──→ Response 2
Request 3 ──→ Process ──→ Response 3
Total time = T1 + T2 + T3 (serial)

Future: Potential Async Processing
────────────────────────────────
Request 1 ──┐
Request 2 ──┼─→ Process (Concurrent) ──→ Responses
Request 3 ──┘
Total time ≈ max(T1, T2, T3) (parallel)
```

## Caching Strategy (Optional Future Enhancement)

```
User Request
    │
    ├─ Check Cache
    │  ├─ Hit: Return cached response
    │  └─ Miss: Continue to API
    │
    ▼
API Call
    │
    ├─ Get Response
    │
    ▼
Store in Cache
    │
    ▼
Return to User
```

## Usage Patterns

### Pattern A: Fire & Forget
```python
response = generate_response("quick question")
print(response)
# Simple, no special handling
```

### Pattern B: Error-Aware
```python
try:
    response = generate_response(user_input)
except ValueError as e:
    # Handle validation errors
except Exception as e:
    # Handle API errors
```

### Pattern C: Role-Based
```python
analyst = OpenAIClientWrapper(model="gpt-4")
creative = OpenAIClientWrapper(model="gpt-3.5-turbo")

analysis = analyst.generate_response(prompt)
ideas = creative.generate_response(prompt)
```

### Pattern D: Batch Processing
```python
client = OpenAIClientWrapper()
for item in items:
    result = client.generate_response(item)
    process_result(result)
```

## Performance Characteristics

### Time Complexity
- **Per Request**: O(1) - Single API call
- **Batch**: O(n) - n sequential API calls

### Space Complexity
- **Per Request**: O(p + r) - prompt + response size
- **Overhead**: O(1) - Minimal client setup

### Network I/O
```
Latency Components
─────────────────
1. TCP Connection:    ~50-200ms
2. Request Upload:    ~10-100ms
3. API Processing:    ~500-5000ms
4. Response Download: ~10-100ms
────────────────────
Total: ~600-5400ms (typical)
```

## Scalability Considerations

### Current Limitations
- Sequential processing (serial)
- No caching layer
- No retry logic
- Direct API calls (no queue)

### Scaling Options
1. **Rate Limiting**: Implement token bucket algorithm
2. **Batching**: Use OpenAI Batch API for cost savings
3. **Caching**: Cache identical prompts
4. **Queue**: Use message queue (RabbitMQ, Redis)
5. **Async**: Implement async/await
6. **Load Balancing**: Distribute across multiple API keys

## Integration Architecture

```
ResearchAgent          ┐
FastAPI Routes         ├─ Application
Data Pipeline          ┘
        │
        ▼
OpenAI Client Wrapper
        │
        ├─ generate_response()
        ├─ OpenAIClientWrapper class
        └─ Error handling
        │
        ▼
Configuration
        │
        ├─ API Key (env var)
        ├─ Model Selection (gpt-4o-mini default)
        ├─ Temperature (0.7 default)
        └─ Max Tokens (optional)
        │
        ▼
OpenAI API ← HTTP/REST
```

## Security Considerations

### API Key Management
```
✓ Store in environment variables
✓ Never commit to version control
✓ Rotate regularly
✓ Use separate keys per environment
✓ Monitor usage patterns

✗ Don't hardcode
✗ Don't log
✗ Don't share
```

### Input Validation
```
✓ Validate prompt before sending
✓ Check API key exists
✓ Validate temperature range
✓ Limit max_tokens range

✗ No SQL injection (text-only)
✗ No code execution (API-sandboxed)
```

### Rate Limiting
```
Consider implementing per:
- User
- IP Address
- Time window (1s, 1m, 1h)
- Budget (cost-based)
```

## Testing Strategy

```
Unit Tests (test_openai_client.py)
├─ Input validation
├─ API key handling
├─ Model switching
├─ System prompt processing
└─ Error conditions

Integration Tests (integration_examples.py)
├─ Real API calls
├─ Response parsing
├─ Batch processing
└─ Special use cases

Manual Testing
├─ Environment setup
├─ API connectivity
├─ Edge cases
└─ Cost monitoring
```

## Deployment Checklist

- [ ] API key configured (environment variable)
- [ ] Dependencies installed (`pip install openai`)
- [ ] Tests passing (`python test_openai_client.py`)
- [ ] Examples working (`python integration_examples.py`)
- [ ] Documentation reviewed
- [ ] Error handling tested
- [ ] Rate limits understood
- [ ] Cost monitoring enabled
- [ ] Backup plan for API outages
- [ ] Logging/monitoring in place

## Monitoring & Observability

### Key Metrics
```
Counters
├─ Total API calls
├─ Successful responses
├─ Failed requests
├─ Timeout errors
└─ Rate limit hits

Gauges
├─ Average response time
├─ Active requests
├─ Token usage
└─ Cost per request

Histograms
├─ Response time distribution
├─ Token count distribution
├─ Temperature usage patterns
└─ Model usage patterns
```

### Logging Recommendations
```python
import logging

logger = logging.getLogger(__name__)

logger.info(f"API call: model={model}, tokens={tokens}")
logger.error(f"API error: {error}", exc_info=True)
logger.debug(f"Response: {response[:100]}...")
```

## Version History

```
v1.0 (Current)
├─ Core generate_response() function
├─ OpenAIClientWrapper class
├─ gpt-4o-mini default model
├─ Comprehensive error handling
└─ Full documentation

v1.1 (Planned)
├─ Async/await support
├─ Response caching
├─ Retry logic with exponential backoff
└─ Streaming support

v2.0 (Future)
├─ Multi-provider support
├─ Cost tracking
├─ Advanced logging
└─ Performance optimizations
```

---

**Architecture Document for OpenAI Client Wrapper v1.0**
