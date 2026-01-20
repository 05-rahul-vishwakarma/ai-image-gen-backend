# Quick Start Guide - Image Generation API

## What Users Send

Users send a **JSON payload** to your API with a text prompt describing the image they want.

---

## Simplest Example

```json
{
  "prompt": "A cute cat sitting on a windowsill"
}
```

That's it! Just a text description of what image you want.

---

## With Style Options

```json
{
  "prompt": "A futuristic city with flying cars at sunset",
  "settings": {
    "model": "dall-e-3",
    "style": "vivid"
  }
}
```

**Styles:**
- `"vivid"` → Colorful, dramatic, eye-catching
- `"natural"` → Realistic, subtle, natural-looking

---

## Real Example Using cURL

```bash
# 1. Login first to get a token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "name": "John Doe"
  }'

# 2. Use the token to generate an image
curl -X POST http://localhost:8000/api/generations/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A beautiful sunset over mountains"
  }'
```

---

## What Users Get Back

```json
{
  "success": true,
  "message": "Generation created successfully",
  "data": {
    "id": "abc123",
    "prompt": "A beautiful sunset over mountains",
    "image_url": "https://oaidalleapiprodscus.blob.core.windows.net/...",
    "status": "completed"
  }
}
```

The `image_url` is the generated image! Users can view it in their browser.

---

## Popular Prompt Examples

### 1. Simple & Clear
```json
{"prompt": "A cat playing with yarn"}
```

### 2. Detailed Description
```json
{"prompt": "A cozy coffee shop with warm lighting, wooden tables, plants, and a barista making latte art"}
```

### 3. Art Style
```json
{"prompt": "A mountain landscape in the style of watercolor painting"}
```

### 4. Specific Lighting
```json
{"prompt": "A portrait of a person, golden hour lighting, soft focus"}
```

### 5. Fantasy/Sci-Fi
```json
{"prompt": "A spaceship landing on an alien planet with two moons"}
```

---

## Tips for Writing Good Prompts

✅ **Good:**
- "A red sports car on a mountain road at sunset"
- "A modern kitchen with marble countertops and wooden cabinets"
- "An astronaut floating in space with Earth in the background"

❌ **Too Vague:**
- "A car"
- "Something cool"
- "A picture"

---

## Try It Now!

1. **Start the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Run the test script:**
   ```bash
   python examples/test_api_client.py
   ```

3. **Or use the API directly:** Visit `http://localhost:8000/docs` for interactive API documentation

---

## Need More Examples?

Check out:
- `examples/prompt_examples.md` - Detailed examples with explanations
- `examples/simple_example.json` - 10 ready-to-use prompt examples
- `examples/test_api_client.py` - Python script showing how to use the API
