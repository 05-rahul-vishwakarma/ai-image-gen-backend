# Examples Directory

This directory contains examples showing how users send prompts to generate AI images.

## Files Overview

### 📘 [QUICK_START.md](QUICK_START.md)
**Start here!** Simple, beginner-friendly guide with:
- Simplest prompt example
- How to use the API
- Quick reference

### 📖 [prompt_examples.md](prompt_examples.md)
Comprehensive guide with:
- 10 detailed prompt examples
- Tips for writing good prompts
- Full API request/response formats
- Code examples in Python and JavaScript

### 📄 [simple_example.json](simple_example.json)
10 ready-to-use JSON payloads:
- Basic prompts
- Art styles
- Photography
- Product design
- Character design
- And more!

### 🐍 [test_api_client.py](test_api_client.py)
Working Python script that demonstrates:
- Login/authentication
- Generating an image
- Retrieving generation history
- Full end-to-end flow

## Usage

### Run the Test Script
```bash
# Make sure your server is running first
uvicorn app.main:app --reload

# In another terminal, run the test
python examples/test_api_client.py
```

### Try Manual Requests
```bash
# Example 1: Simple prompt
curl -X POST http://localhost:8000/api/generations/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A sunset over mountains"}'

# Example 2: With style
curl -X POST http://localhost:8000/api/generations/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A futuristic city at night",
    "settings": {"model": "dall-e-3", "style": "vivid"}
  }'
```

## What Users Need to Send

At minimum, users only need to send:
```json
{
  "prompt": "description of the image"
}
```

Optionally, they can customize:
```json
{
  "prompt": "description of the image",
  "settings": {
    "model": "dall-e-3",
    "style": "vivid"
  }
}
```

## Quick Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `prompt` | string | ✅ Yes | Text description of the image to generate |
| `settings` | object | ❌ No | Optional customization settings |
| `settings.model` | string | ❌ No | AI model: "dall-e-3" (default) or "dall-e-2" |
| `settings.style` | string | ❌ No | "vivid" (dramatic) or "natural" (realistic) |

## Response Format

Users receive:
```json
{
  "success": true,
  "data": {
    "id": "generation_id",
    "image_url": "https://...",
    "prompt": "original prompt",
    "status": "completed"
  }
}
```

The `image_url` can be opened in any browser to view the generated image!
