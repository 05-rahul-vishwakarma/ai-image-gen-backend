# OpenAI API - cURL vs Python Comparison

## ⚠️ Important: Correct Model Names

**Your cURL example uses an incorrect model:**
```bash
"model": "gpt-image-1.5"  # ❌ This doesn't exist!
```

**Correct OpenAI image models:**
- `"dall-e-3"` ✅ (latest, best quality)
- `"dall-e-2"` ✅ (older version)

---

## Correct cURL Format

```bash
curl https://api.openai.com/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "dall-e-3",
    "prompt": "A cute baby sea otter",
    "n": 1,
    "size": "1024x1024"
  }'
```

---

## How Our Python Code Translates

### Python Code (openai_service.py)
```python
response = self.client.images.generate(
    model="dall-e-3",
    prompt="A cute baby sea otter",
    size="1024x1024",
    quality="standard",
    n=1
)
```

### Equivalent cURL
```bash
curl https://api.openai.com/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "dall-e-3",
    "prompt": "A cute baby sea otter",
    "size": "1024x1024",
    "quality": "standard",
    "n": 1
  }'
```

**They're identical!** The Python OpenAI library just wraps the HTTP request for you.

---

## Complete Examples Side-by-Side

### Example 1: Basic Image Generation

**cURL:**
```bash
curl https://api.openai.com/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-proj-..." \
  -d '{
    "model": "dall-e-3",
    "prompt": "A sunset over mountains",
    "n": 1,
    "size": "1024x1024"
  }'
```

**Our Python Code:**
```python
# In openai_service.py line 72
response = self.client.images.generate(
    model="dall-e-3",
    prompt="A sunset over mountains",
    size="1024x1024",
    n=1
)
```

---

### Example 2: With Style Parameter (DALL-E 3 only)

**cURL:**
```bash
curl https://api.openai.com/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-proj-..." \
  -d '{
    "model": "dall-e-3",
    "prompt": "A futuristic city at night",
    "n": 1,
    "size": "1024x1024",
    "quality": "standard",
    "style": "vivid"
  }'
```

**Our Python Code:**
```python
response = self.client.images.generate(
    model="dall-e-3",
    prompt="A futuristic city at night",
    size="1024x1024",
    quality="standard",
    n=1,
    style="vivid"
)
```

---

### Example 3: HD Quality

**cURL:**
```bash
curl https://api.openai.com/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-proj-..." \
  -d '{
    "model": "dall-e-3",
    "prompt": "A professional portrait",
    "n": 1,
    "size": "1024x1024",
    "quality": "hd"
  }'
```

**Our Python Code:**
```python
response = self.client.images.generate(
    model="dall-e-3",
    prompt="A professional portrait",
    size="1024x1024",
    quality="hd",  # Higher quality, more expensive
    n=1
)
```

---

## API Response Format

Both cURL and Python return the same JSON response:

```json
{
  "created": 1589478378,
  "data": [
    {
      "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/..."
    }
  ]
}
```

**In our code (line 80):**
```python
image_url = response.data[0].url  # Extract the URL
```

---

## All Available Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | string | Yes | `"dall-e-3"` or `"dall-e-2"` |
| `prompt` | string | Yes | Text description (max 4000 chars for DALL-E 3) |
| `n` | integer | No | Number of images (1-10 for DALL-E 2, must be 1 for DALL-E 3) |
| `size` | string | No | `"1024x1024"`, `"1024x1792"`, `"1792x1024"` for DALL-E 3 |
| `quality` | string | No | `"standard"` or `"hd"` (DALL-E 3 only) |
| `style` | string | No | `"vivid"` or `"natural"` (DALL-E 3 only) |

---

## Test Your API Key with cURL

```bash
# Set your API key
export OPENAI_API_KEY="sk-proj-your-key-here"

# Test image generation
curl https://api.openai.com/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "dall-e-3",
    "prompt": "A cute baby sea otter",
    "n": 1,
    "size": "1024x1024"
  }'
```

**Expected response:**
```json
{
  "created": 1234567890,
  "data": [
    {
      "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-..."
    }
  ]
}
```

---

## Why Our Python Code is Better

### cURL (Manual):
```bash
# You have to manually handle:
# - HTTP headers
# - JSON parsing
# - Error handling
# - Response parsing

curl https://api.openai.com/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{"model": "dall-e-3", "prompt": "test", "n": 1, "size": "1024x1024"}'
```

### Python (Automatic):
```python
# The library handles all of that for you!
response = self.client.images.generate(
    model="dall-e-3",
    prompt="test",
    n=1,
    size="1024x1024"
)

# Clean, type-safe, easy to read
image_url = response.data[0].url
```

---

## Summary

✅ Our Python code in `openai_service.py` is **already correct**

❌ Your cURL example has wrong model name: `"gpt-image-1.5"` doesn't exist

✅ Correct model names: `"dall-e-3"` or `"dall-e-2"`

✅ The Python OpenAI library sends the exact same HTTP request as cURL, just cleaner and easier to use!
