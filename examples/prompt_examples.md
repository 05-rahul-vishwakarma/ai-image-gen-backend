# Image Generation API - Prompt Examples

This document shows examples of prompts users can send to generate AI images.

## Basic API Request Format

```bash
POST /api/generations/
Headers:
  Authorization: Bearer <your_jwt_token>
  Content-Type: application/json
```

---

## Example 1: Simple Prompt (Minimal)

**Request Body:**
```json
{
  "prompt": "A cute cat sitting on a windowsill"
}
```

**What happens:**
- Uses default settings (DALL-E 3, standard quality, 1024x1024)
- Generates a basic image of a cat

---

## Example 2: Detailed Prompt with Style

**Request Body:**
```json
{
  "prompt": "A futuristic cityscape at sunset with flying cars and neon lights",
  "settings": {
    "model": "dall-e-3",
    "style": "vivid"
  }
}
```

**What happens:**
- Uses DALL-E 3 model
- Applies "vivid" style (dramatic, hyper-realistic colors)
- Creates a vibrant futuristic city image

---

## Example 3: Natural Style for Realistic Images

**Request Body:**
```json
{
  "prompt": "A professional headshot of a business woman in modern office",
  "settings": {
    "model": "dall-e-3",
    "style": "natural"
  }
}
```

**What happens:**
- Uses "natural" style for more realistic, less dramatic results
- Good for portraits, professional photos, realistic scenes

---

## Example 4: Creative Art Prompt

**Request Body:**
```json
{
  "prompt": "An abstract painting of emotions, using bold brushstrokes and vibrant colors in the style of Kandinsky"
}
```

**What happens:**
- Generates artistic, abstract image
- AI interprets the artistic style reference

---

## Example 5: Landscape Photography

**Request Body:**
```json
{
  "prompt": "A serene mountain lake at dawn with mist rising from the water, surrounded by pine trees, golden hour lighting"
}
```

**What happens:**
- Creates a landscape with specific lighting conditions
- More detailed prompts = more specific results

---

## Example 6: Character Design

**Request Body:**
```json
{
  "prompt": "A friendly robot character with a round body, big expressive eyes, and colorful LED lights, designed for a children's book illustration",
  "settings": {
    "model": "dall-e-3",
    "style": "vivid"
  }
}
```

**What happens:**
- Creates a character suitable for children's content
- Vivid style makes it more colorful and appealing

---

## Example 7: Product Photography

**Request Body:**
```json
{
  "prompt": "A sleek modern smartwatch on a minimalist white background, studio lighting, product photography style"
}
```

**What happens:**
- Generates product-style image
- Good for mockups, presentations

---

## Example 8: Food Photography

**Request Body:**
```json
{
  "prompt": "A gourmet burger with melted cheese, fresh lettuce, and tomatoes on a wooden board, dramatic side lighting, food photography"
}
```

**What happens:**
- Creates appetizing food image
- Detailed lighting description improves quality

---

## Example 9: Fantasy Scene

**Request Body:**
```json
{
  "prompt": "A magical forest with glowing mushrooms, fairy lights floating in the air, and a crystal-clear stream, moonlight filtering through ancient trees",
  "settings": {
    "model": "dall-e-3",
    "style": "vivid"
  }
}
```

**What happens:**
- Creates fantasy/magical atmosphere
- Vivid style enhances the magical feel

---

## Example 10: Architectural Visualization

**Request Body:**
```json
{
  "prompt": "A modern sustainable house with large glass windows, wooden accents, solar panels, surrounded by lush garden, architectural rendering style"
}
```

**What happens:**
- Generates architectural concept
- Useful for design presentations

---

## Tips for Writing Good Prompts

### ✅ DO:
- Be specific and descriptive
- Include lighting details (golden hour, dramatic lighting, soft light)
- Mention the art style or photography type
- Describe the mood or atmosphere
- Specify colors, textures, materials

### ❌ DON'T:
- Be too vague ("make something cool")
- Use copyrighted character names
- Request violent or inappropriate content
- Expect exact replication of specific people

---

## Full cURL Example

```bash
curl -X POST http://localhost:8000/api/generations/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A cozy coffee shop interior with warm lighting, wooden furniture, plants hanging from the ceiling, and a barista making latte art",
    "settings": {
      "model": "dall-e-3",
      "style": "natural"
    }
  }'
```

---

## Python Example (Using requests library)

```python
import requests

# Your JWT token from login
token = "your_jwt_token_here"

# API endpoint
url = "http://localhost:8000/api/generations/"

# Request headers
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Request body
data = {
    "prompt": "A beautiful sunset over mountains with colorful sky",
    "settings": {
        "model": "dall-e-3",
        "style": "vivid"
    }
}

# Send request
response = requests.post(url, json=data, headers=headers)

# Get result
if response.status_code == 200:
    result = response.json()
    print(f"Image URL: {result['data']['image_url']}")
    print(f"Generation ID: {result['data']['id']}")
else:
    print(f"Error: {response.text}")
```

---

## JavaScript Example (Using fetch)

```javascript
// Your JWT token from login
const token = "your_jwt_token_here";

// API endpoint
const url = "http://localhost:8000/api/generations/";

// Request data
const data = {
  prompt: "A cyberpunk street scene with neon signs and rain",
  settings: {
    model: "dall-e-3",
    style: "vivid"
  }
};

// Send request
fetch(url, {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${token}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify(data)
})
  .then(response => response.json())
  .then(result => {
    console.log("Image URL:", result.data.image_url);
    console.log("Generation ID:", result.data.id);
  })
  .catch(error => {
    console.error("Error:", error);
  });
```

---

## Response Format

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Generation created successfully",
  "data": {
    "id": "65a1b2c3d4e5f6g7h8i9j0k1",
    "user_id": "65a1b2c3d4e5f6g7h8i9j0k2",
    "prompt": "A cute cat sitting on a windowsill",
    "image_url": "https://oaidalleapiprodscus.blob.core.windows.net/private/...",
    "status": "completed",
    "settings": {
      "width": 512,
      "height": 512,
      "model": "dall-e-3",
      "style": null
    },
    "created_at": "2024-01-18T10:30:00.000Z"
  }
}
```

**Error Response (500 Internal Server Error):**
```json
{
  "detail": "Failed to generate image: Invalid API key provided"
}
```

---

## Available Settings

### Model Options:
- `"dall-e-3"` - Latest and highest quality (recommended)
- `"dall-e-2"` - Older version, faster but lower quality

### Style Options (DALL-E 3 only):
- `"vivid"` - Hyper-realistic, dramatic colors, eye-catching
- `"natural"` - More realistic, subtle, natural-looking

### Quality Options:
- `"standard"` - Default quality (faster, cheaper)
- `"hd"` - Higher quality (slower, more expensive)

### Size Options:
- `"1024x1024"` - Square (default)
- `"1024x1792"` - Portrait/vertical
- `"1792x1024"` - Landscape/horizontal

**Note:** Size is currently hardcoded to 1024x1024 in the service. You can modify the code to make it configurable.
