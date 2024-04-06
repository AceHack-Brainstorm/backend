from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant designed to help system technicians in fixing their issues."},
    {"role": "user", "content": "Where was it played?"}
  ]
)

print(response)