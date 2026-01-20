# Hugging Face Image Generation - Examples

This project uses **Hugging Face's Stable Diffusion v1.5** model for AI image generation.

## Model Information

- **Model**: `runwayml/stable-diffusion-v1-5`
- **Provider**: Hugging Face Inference API
- **Output**: Base64 encoded PNG images
- **API**: https://api-inference.huggingface.co

---

## How It Works

### 1. User sends a prompt

```json
{
  "prompt": "A beautiful sunset over mountains"
}
```

### 2. API calls Hugging Face

```python
# Behind the scenes (in huggingface_service.py)
headers = {"Authorization": f"Bearer {HF_TOKEN}"}
payload = {"inputs": "A beautiful sunset over mountains"}

response = requests.post(
    "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5",
    headers=headers,
    json=payload
)
```

### 3. Hugging Face returns image bytes

The response contains raw PNG image data (binary)

### 4. We convert to Base64

```python
# Convert binary image to base64 string
image_base64 = base64.b64encode(response.content).decode('utf-8')
image_data = f"data:image/png;base64,{image_base64}"
```

### 5. Store in database & return to user

The base64 string is stored in MongoDB and returned to the user

---

## Example Prompts

### Simple Prompts

```json
{"prompt": "A cat sitting on a windowsill"}
{"prompt": "A sunset over the ocean"}
{"prompt": "A futuristic city"}
```

### Detailed Prompts (Better Results)

```json
{
  "prompt": "A beautiful landscape with mountains, a lake, and colorful sunset sky, highly detailed, 8k"
}
```

```json
{
  "prompt": "A cute robot character with big eyes, colorful, digital art, trending on artstation"
}
```

```json
{
  "prompt": "A cozy coffee shop interior, warm lighting, plants, wooden furniture, photorealistic"
}
```

---

## API Usage

### cURL Example

```bash
# Login first
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "name": "John Doe"
  }'

# Generate image
curl -X POST http://localhost:8000/api/generations/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A beautiful sunset over mountains, vibrant colors"
  }'
```

### Python Example

```python
import requests

token = "your_jwt_token"
url = "http://localhost:8000/api/generations/"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

data = {
    "prompt": "A cute cat sitting on a windowsill"
}

response = requests.post(url, json=data, headers=headers)
result = response.json()

# The image is in base64 format
image_base64 = result['data']['image_url']
print(f"Generated image: {image_base64[:50]}...")
```

### JavaScript Example

```javascript
const token = "your_jwt_token";
const url = "http://localhost:8000/api/generations/";

const data = {
  prompt: "A futuristic cityscape at night"
};

fetch(url, {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${token}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify(data)
})
  .then(res => res.json())
  .then(result => {
    // Display image in HTML
    const img = document.createElement('img');
    img.src = result.data.image_url; // Base64 data URL
    document.body.appendChild(img);
  });
```

---

## Response Format

```json
{
  "success": true,
  "message": "Generation created successfully",
  "data": {
    "id": "65a1b2c3d4e5f6g7h8i9j0k1",
    "user_id": "65a1b2c3d4e5f6g7h8i9j0k2",
    "prompt": "A beautiful sunset over mountains",
    "image_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
    "status": "completed",
    "settings": {
      "width": 512,
      "height": 512,
      "model": "dall-e-3",
      "style": null
    },
    "created_at": "2024-01-19T10:30:00.000Z"
  }
}
```

**Note**: The `image_url` field contains a base64 data URL, not an HTTP URL like with OpenAI.

---

## Using Base64 Images

### In HTML

```html
<img src="data:image/png;base64,iVBORw0KGgoAAAANS..." alt="Generated image" />
```

### Convert to File (Python)

```python
import base64

# Extract base64 data (remove "data:image/png;base64," prefix)
base64_data = image_url.split(',')[1]

# Decode and save
image_bytes = base64.b64decode(base64_data)
with open('image.png', 'wb') as f:
    f.write(image_bytes)
```

### Convert to File (JavaScript)

```javascript
function downloadImage(base64Data, filename) {
  const link = document.createElement('a');
  link.href = base64Data;
  link.download = filename;
  link.click();
}

// Usage
downloadImage(result.data.image_url, 'generated-image.png');
```

---

## Tips for Better Results

### ✅ Good Practices

1. **Be Specific**: "A red sports car on a mountain road at sunset"
2. **Add Quality Tags**: "highly detailed", "8k", "photorealistic"
3. **Mention Art Style**: "digital art", "oil painting", "watercolor"
4. **Include Lighting**: "warm lighting", "dramatic shadows", "golden hour"

### Examples

```json
{"prompt": "A cyberpunk city street at night, neon lights, rain, highly detailed, 8k"}
{"prompt": "A cute robot character, big eyes, colorful, digital art, trending on artstation"}
{"prompt": "A fantasy forest with glowing mushrooms, magical atmosphere, detailed"}
{"prompt": "Portrait of a woman, golden hour lighting, soft focus, photorealistic"}
```

---

## Setup Instructions

### 1. Get Hugging Face API Token

1. Go to https://huggingface.co/settings/tokens
2. Create a new token (select "Read" access)
3. Copy the token (starts with `hf_...`)

### 2. Add to .env file

```bash
HUGGIN_API_KEY=hf_your_token_here
```

### 3. Test the service

```bash
python test_huggingface_service.py
```

---

## Differences from OpenAI DALL-E

| Feature | Hugging Face (Stable Diffusion) | OpenAI (DALL-E) |
|---------|--------------------------------|-----------------|
| **Model** | Stable Diffusion v1.5 | DALL-E 3 |
| **Output** | Base64 PNG | URL to hosted image |
| **Cost** | Free tier available | Paid per image |
| **Speed** | 10-30 seconds (first load) | 10-20 seconds |
| **Quality** | Good | Excellent |
| **Image Size** | 512x512 default | 1024x1024+ |
| **Storage** | You handle it | OpenAI hosts temporarily |

---

## Common Issues

### Model Loading Time

- **First request may take 20-30 seconds** while model loads
- Subsequent requests are faster (5-15 seconds)
- This is normal behavior for Hugging Face Inference API

### Rate Limits

- Free tier has rate limits
- Consider upgrading for production use
- Check: https://huggingface.co/pricing

### Image Quality

- Stable Diffusion v1.5 generates 512x512 images by default
- For higher quality, consider using DALL-E or Stable Diffusion XL
- Quality tags in prompts can help: "highly detailed", "8k"

---

## Next Steps

- Try the test script: `python test_huggingface_service.py`
- Test the API: `python examples/test_api_client.py`
- View API docs: `http://localhost:8000/docs`
- Read about Stable Diffusion: https://huggingface.co/runwayml/stable-diffusion-v1-5
