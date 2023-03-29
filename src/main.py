from dotenv import load_dotenv
import os
from facebook_webhook import (
    FlaskServer,
    FacebookWebhook,
    make_quick_reply,
    make_text_message,
    make_payload,
)
import openai

# Load các biến môi trường từ file .env
load_dotenv()

# Lấy API key của OpenAI từ biến môi trường
api_key = os.getenv("OPENAI_API_KEY")

# Khởi tạo OpenAI API client
openai.api_key = api_key

# Khởi tạo Facebook Webhook
webhook = FacebookWebhook()
app = FlaskServer(webhook)

# Định nghĩa một hàm để xử lý tin nhắn và trả lời bằng OpenAI API
def handle_message(sender_id, text):
    # Gửi câu hỏi đến OpenAI API và nhận lại câu trả lời
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Q: {text}\nA:",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    answer = response.choices[0].text.strip()
    
    # Trả lời tin nhắn với câu trả lời của OpenAI
    quick_replies = [
        make_quick_reply("Yes", make_payload("yes")),
        make_quick_reply("No", make_payload("no")),
    ]
    message = make_text_message(answer, quick_replies=quick_replies)
    webhook.send(sender_id, message)

# Đăng ký một handler cho tin nhắn
@webhook.default_message
def handle_default(sender_id, message):
    handle_message(sender_id, message.text)

# Chạy ứng dụng Flask
if __name__ == "__main__":
    app.run()
