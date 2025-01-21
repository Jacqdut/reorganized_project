import openai

# Point to the mock server
openai.api_base = "http://127.0.0.1:5001/v1"
openai.api_key = "mock-api-key"

try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}],
    )
    print(response)
except Exception as e:
    print(f"Error: {e}")
