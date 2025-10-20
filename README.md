# 背景說明
- 教授要求我們用 OpenAI API 做一個「有趣又符合真實世界需求」的聊天機器人，還強調 System Prompt 是靈魂。
- 我想說既然要真實世界，那就…越真實越好。
- 於是我打造了
  - 🥁🥁 #巴奈縣長卸責生成器 🥁🥁
  - https://huggingface.co/spaces/petertsengtw/hualien_gov

# System Prompt ：
- 人設：地方首長（擅長開記者會）
- 語氣：第一人稱＋官腔，但情緒控制得很好
- 核心技能：任何問題都能完美推給中央，並優雅收尾：「我也很遺憾，但這完全是 #中央政府的責任 呀！」

# 技術步驟就不贅述（反正就是 API + Gradio + 一點點叛逆 ✌️）
- 金鑰：用Groq api call llama-3.1-8b-instant model。
- 呼叫寫好的ai suite
- 設計System RPOMPT(人設/背景)
- 用Gradio給使用者呈現web app
