from groq import Groq

class LLMClient:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)

    def query(self, prompt: str, model: str, temperature=0.3, max_tokens=1024):
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
