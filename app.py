import os
import gradio as gr
from groq import Groq

# ====== Configuration ======
MODEL_NAME = "llama-3.1-8b-instant"

SYSTEM_PROMPT = """請用台灣習慣的中文來寫這段 po 文：
請用地方政府官員思考, 也就是任何使用者寫的事情都應該是中央政府負責,
用我的第一人稱、回答記者會問題的口吻說一次,
說為什麼這是一件隸屬中央權責的事, 並且以「我也很遺憾，但這完全是 中央政府的責任 呀!」結尾。
可以適度的加上 emoji。
"""

# Read API key from environment variable for security
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Reuse single client across requests
_client = None
def get_client():
    global _client
    if _client is None:
        if not GROQ_API_KEY:
            raise RuntimeError(
                "Missing GROQ_API_KEY environment variable. "
                "Please set it before running the app."
            )
        _client = Groq(api_key=GROQ_API_KEY)
    return _client


def generate_reply(user_input: str) -> str:
    if not user_input or not user_input.strip():
        return "【縣長回應如下】\n請先輸入你想問的問題或情境。"

    try:
        client = get_client()

        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input.strip()},
            ],
            temperature=0.7,
            max_tokens=800,
        )

        content = completion.choices[0].message.content.strip()
        return f"【縣長回應如下】\n{content}"

    except Exception as e:
        return f"【縣長回應如下】\n系統錯誤：{e}\n\n請確認 GROQ_API_KEY 是否正確，或稍後再試。"

# ====== Gradio UI ======
TITLE = "巴奈縣長卸責生成器（Groq + Llama 3.1 8B Instant）"
DESCRIPTION = (
    "輸入你想問縣長的問題或情境，系統會依照預設的 System Prompt 生成回應。"
    "後端固定使用 Groq 的 Llama 3.1 8B Instant 模型。"
)

with gr.Blocks(title=TITLE) as demo:
    gr.Markdown(f"# {TITLE}")
    gr.Markdown(DESCRIPTION)

    with gr.Row():
        input_box = gr.Textbox(
            label="你想問縣長什麼？",
            placeholder="請輸入記者會提問、民眾陳情內容、或你想讓縣長回應的情境…",
            lines=4,
        )

    output_box = gr.Markdown(label="輸出")

    generate_btn = gr.Button("生成回應")

    generate_btn.click(fn=generate_reply, inputs=input_box, outputs=output_box)
    input_box.submit(fn=generate_reply, inputs=input_box, outputs=output_box)

if __name__ == "__main__":
    # For local debug: demo.launch(share=True)
    demo.launch()
