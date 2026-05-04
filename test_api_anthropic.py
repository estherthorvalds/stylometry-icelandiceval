import anthropic
import os

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

prompt_text = open("/Users/esther/Documents/GitHub/stylometry-icelandiceval/data/experiment/prompts/academic_prompt_001.txt").read()

message = client.messages.create(
    model="claude-sonnet-4-6",  # eða claude-opus-4-6
    max_tokens=1024,
    messages=[
        {"role": "user", "content": prompt_text}
    ]
)

print(message.content[0].text)