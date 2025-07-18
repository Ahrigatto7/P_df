import os
from openai import OpenAI

def run_prompt_template(template_str, variables: dict, model="gpt-4", max_tokens=512, temperature=0):
    prompt = template_str.format(**variables)
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return response.choices[0].message.content.strip()