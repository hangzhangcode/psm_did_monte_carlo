from openai import OpenAI
from dotenv import load_dotenv
import os
from datetime import datetime

# API 配置
API_KEY = "sk-wmcphnwnklfzbupquslywxiqzghnaxbmfttdesgebimferkw"
BASE_URL = "https://api.siliconflow.cn/v1"
MODEL = "deepseek-ai/DeepSeek-V4-Flash"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# 文件处理
def read_text_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        with open(file_path, "r", encoding="gbk") as f:
            return f.read()

# 聊天记录保存
def save_chat_log(log_content):
    output_file = "/Users/zhanghang/Documents/GitHub/psm_did_monte_carlo/ai_usage_record.md"
    with open(output_file, "a", encoding="utf-8") as f:
        f.write(log_content + "\n\n")

# 主聊天函数
def chat_with_file(file_path):
    file_content = read_text_file(file_path)
    print(f"\n✅ 已读取输入文件：{file_path}")
    print("💬 开始连续对话（输入 exit 退出）")
    print("📝 所有对话会自动保存到 ai_usage_record.md\n")

    messages = [
        {"role": "system", "content": "你现在是我的机器学习与因果分析课程作业专业辅导助手。我会先上传作业文档/代码文件，请你严格按照以下固定步骤帮我分析：1. 先完整通读文件，提炼本次作业的全部任务要求、评分标准与核心研究问题；2. 把作业任务分点拆解，梳理清楚必须完成的每一项子任务；3. 结合文件里的模型、代码、场景设定，给出整体解题与写作的大致思路框架；4. 后续我会一步步向你提问，请基于文件内容、学术规范和因果推断专业知识，严谨、条理清晰地回答，不要随意编造内容。"},
        {"role": "user", "content": f"作业文件内容：\n{file_content}"}
    ]

    # 记录开头时间
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_chat_log(f"--- 对话开始于 {start_time} ---\n")

    while True:
        question = input("我：")
        if question.lower() == "exit":
            print("👋 对话结束，记录已保存！")
            break

        messages.append({"role": "user", "content": question})
        save_chat_log(f"我：{question}")

        try:
            res = client.chat.completions.create(model=MODEL, messages=messages)
            reply = res.choices[0].message.content.strip()

            print(f"AI：{reply}\n")
            save_chat_log(f"AI：{reply}")
            messages.append({"role": "assistant", "content": reply})

        except Exception as e:
            print(f"❌ 错误：{e}\n")

# 主程序入口
if __name__ == "__main__":
    INPUT_FILE = "/Users/zhanghang/Documents/GitHub/psm_did_monte_carlo/assignment01_psm_did_monte_carlo.qmd"

    # 开始对话
    chat_with_file(INPUT_FILE)