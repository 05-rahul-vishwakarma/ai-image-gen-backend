#!/bin/bash

# Test script to verify OpenAI API works with correct model name
# This demonstrates the exact cURL equivalent of our Python code

echo "======================================================"
echo "OpenAI Image Generation - cURL Test"
echo "======================================================"
echo ""

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ Error: OPENAI_API_KEY environment variable is not set"
    echo ""
    echo "Please set it first:"
    echo "export OPENAI_API_KEY='sk-proj-your-key-here'"
    exit 1
fi

echo "✅ API Key found: ${OPENAI_API_KEY:0:20}..."
echo ""

echo "Test 1: Basic Image Generation (Correct Model)"
echo "------------------------------------------------------"
echo "Model: dall-e-3"
echo "Prompt: A cute baby sea otter"
echo ""
echo "Sending request to OpenAI..."
echo ""

# This is the CORRECT cURL format
curl https://api.openai.com/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "dall-e-3",
    "prompt": "A cute baby sea otter",
    "n": 1,
    "size": "1024x1024"
  }' | jq '.'

echo ""
echo ""
echo "======================================================"
echo "Test 2: With Style Parameter"
echo "======================================================"
echo ""

curl https://api.openai.com/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "dall-e-3",
    "prompt": "A futuristic city at night",
    "n": 1,
    "size": "1024x1024",
    "quality": "standard",
    "style": "vivid"
  }' | jq '.'

echo ""
echo ""
echo "======================================================"
echo "Note: The Python code does EXACTLY the same thing!"
echo "======================================================"
echo ""
echo "Our openai_service.py sends identical requests."
echo "The OpenAI Python library just wraps the HTTP calls."
echo ""
