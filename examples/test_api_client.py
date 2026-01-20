"""
Simple test client to demonstrate how users send prompts to the API

Usage:
1. Start your FastAPI server: uvicorn app.main:app --reload
2. Run this script: python examples/test_api_client.py
"""

import requests
import json


# Configuration
API_BASE_URL = "http://localhost:8000/api"
EMAIL = "test@example.com"
PASSWORD = "password123"
NAME = "Test User"


def login_or_register(email: str, password: str, name: str) -> str:
    """Login or register and get JWT token"""
    print(f"\n{'='*60}")
    print("STEP 1: Login/Register")
    print(f"{'='*60}")

    url = f"{API_BASE_URL}/auth/login"
    data = {
        "email": email,
        "password": password,
        "name": name
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        result = response.json()
        token = result["data"]["access_token"]
        print(f"✅ Logged in successfully!")
        print(f"User: {result['data']['user']['name']}")
        print(f"Email: {result['data']['user']['email']}")
        print(f"Token: {token[:50]}...")
        return token
    else:
        print(f"❌ Login failed: {response.text}")
        return None


def generate_image(token: str, prompt: str, style: str = None):
    """Generate an image with a prompt"""
    print(f"\n{'='*60}")
    print("STEP 2: Generate Image")
    print(f"{'='*60}")
    print(f"Prompt: {prompt}")
    if style:
        print(f"Style: {style}")

    url = f"{API_BASE_URL}/generations/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Build request data
    data = {"prompt": prompt}
    if style:
        data["settings"] = {
            "model": "dall-e-3",
            "style": style
        }

    print(f"\nSending request to: {url}")
    print(f"Request body: {json.dumps(data, indent=2)}")
    print("\n⏳ Generating image (this may take 10-30 seconds)...\n")

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        result = response.json()
        generation = result["data"]

        print("✅ Image generated successfully!")
        print(f"\nGeneration ID: {generation['id']}")
        print(f"Status: {generation['status']}")
        print(f"Prompt: {generation['prompt']}")
        print(f"\n🖼️  Image URL:")
        print(f"{generation['image_url']}")
        print(f"\n💡 Copy the URL above and paste it in your browser to view the image!")

        return generation
    else:
        print(f"❌ Generation failed: {response.text}")
        return None


def get_all_generations(token: str):
    """Get all user's generations"""
    print(f"\n{'='*60}")
    print("STEP 3: Get All Generations")
    print(f"{'='*60}")

    url = f"{API_BASE_URL}/generations/"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        result = response.json()
        generations = result["data"]

        print(f"✅ Found {len(generations)} generation(s)")
        for i, gen in enumerate(generations, 1):
            print(f"\n{i}. ID: {gen['id']}")
            print(f"   Prompt: {gen['prompt'][:60]}...")
            print(f"   Status: {gen['status']}")
            print(f"   Created: {gen['created_at']}")

        return generations
    else:
        print(f"❌ Failed to fetch generations: {response.text}")
        return []


def main():
    """Main function demonstrating the complete flow"""
    print("\n" + "="*60)
    print("AI IMAGE GENERATOR API - TEST CLIENT")
    print("="*60)

    # Step 1: Login and get token
    token = login_or_register(EMAIL, PASSWORD, NAME)
    if not token:
        print("\n❌ Cannot proceed without authentication")
        return

    # Step 2: Generate an image with a simple prompt
    print("\n\n")
    generation = generate_image(
        token=token,
        prompt="A cute robot sitting in a colorful garden with butterflies",
        style="vivid"
    )

    if not generation:
        print("\n❌ Image generation failed")
        return

    # Step 3: Get all generations
    print("\n\n")
    generations = get_all_generations(token)

    print("\n" + "="*60)
    print("TEST COMPLETED SUCCESSFULLY! 🎉")
    print("="*60)


if __name__ == "__main__":
    # Example prompts you can try:
    example_prompts = [
        "A cute cat sitting on a windowsill",
        "A futuristic cityscape at sunset with flying cars",
        "A cozy coffee shop with warm lighting and plants",
        "An astronaut riding a horse on the moon",
        "A magical forest with glowing mushrooms",
        "A professional headshot of a business person",
        "A delicious burger with fries on a wooden table",
        "An abstract painting with vibrant colors",
        "A serene mountain lake at dawn",
        "A cyberpunk street scene with neon lights and rain"
    ]

    print("\n💡 TIP: You can modify this script to try different prompts!")
    print("Example prompts you can use:")
    for i, prompt in enumerate(example_prompts[:5], 1):
        print(f"{i}. {prompt}")

    # Run the main test
    main()
