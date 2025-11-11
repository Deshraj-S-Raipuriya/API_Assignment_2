# chat_test.py
import os, time
import openai

openai.api_key = openai.api_key = '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'


def test_chat(prompt):
    t0 = time.time()
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":"You are a helpful customer support assistant."},
            {"role":"user","content": prompt}
        ],
        max_tokens=200
    )
    dt = time.time() - t0
    answer = resp["choices"][0]["message"]["content"]
    return answer, dt

if __name__ == "__main__":
    a, latency = test_chat("I was charged twice for my order 12345. What should I do?")
    print("Latency(s):", round(latency,3))
    print("Answer:\n", a)
