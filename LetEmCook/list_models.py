from google import genai

API_KEY = 'AQ.Ab8RN6K_CHiQgtqt0wQZqBOJFX9e0wqPNEBqmCvgQSJIvHi8lg'
client = genai.Client(api_key=API_KEY)

for model in client.models.list():
    print(model.name)