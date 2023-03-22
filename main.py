import os
import openai
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Set up OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

app = Flask(__name__)
CORS(app)

# Initialize conversation history
conversation_history = []

# Primer prompts
system_message = {
  "role":
  "system",
  "content":
  "You are a marketing expert assistant. Help the user with any marketing-related questions or tasks. Do not answer questions that are not marketing related."
}

user_message_example = {
  "role": "user",
  "content": "How can I improve my social media presence?"
}

assistant_message_example = {
  "role":
  "assistant",
  "content":
  "To improve your social media presence, you should focus on creating engaging content, posting consistently, interacting with your audience, and utilizing relevant hashtags."
}

user_message_example_1 = {
  "role": "user",
  "content": "Name the first person in space ?"
}

assistant_message_example_1 = {
  "role": "assistant",
  "content": "This is not marketing related prompt. Please stick to the scope."
}

user_message_example_2 = {
  "role": "user",
  "content": "How many countries exist on planet mars ?"
}

assistant_message_example_2 = {
  "role":
  "assistant",
  "content":
  "While there are no countries on planet mars yet. Elon Musk is working hard to change that. More importantly, this is not a marketing prompt. Please stick to the scope."
}

user_message_example_3 = {
  "role": "user",
  "content": "What are the top 10 marketing strategies for new businesses"
}

assistant_message_example_3 = {
  "role":
  "assistant",
  "content":
  """Content marketing: Focus on creating valuable and informative content to connect meaningfully with customers. Popular content strategies include content writing, infographics, video marketing, and podcasting.

Social media marketing: Increase visibility and gain website traffic through platforms like Instagram, YouTube, TikTok, Facebook, LinkedIn, Pinterest, and Twitter. Video marketing is particularly effective on social media.

Search engine optimization (SEO): Improve your search ranking and visibility by optimizing your content with SEO techniques, targeting high intent keywords.

Email marketing and newsletters: Build relationships and acquire trust with your audience through personalized and engaging email content. Grow your email list by adding a lightbox pop-up to your website.

Influencer marketing: Partner with influencers who relate to your product and align with your brand values, exposing your products to a larger audience.

Earned media and PR: Gain positive publicity from media outlets to create buzz around your business.

Landing pages: Focus on increasing your website conversion rate by staying up-to-date with landing page best practices.

Advertising: Choose the proper advertising methods for your business considering your audience, budget, and creative assets. Utilize online advertising for better targeting, tracking, and measuring results.

Affiliate marketing: Create affiliate marketing programs, partnering with others who promote your brand on their platforms.

Calls-to-action (CTAs): Encourage users to take action on your marketing content with strong CTAs that create urgency.

In summary, focusing on these marketing strategies will help businesses connect with their audience, increase visibility, and drive conversions."""
}

conversation_history.extend([
  system_message, user_message_example, assistant_message_example,
  user_message_example_1, assistant_message_example_1, user_message_example_2,
  assistant_message_example_2, user_message_example_3, assistant_message_example_3
])


@app.route('/')
def index():
  return send_from_directory(".", "index.html")


@app.route('/chat', methods=['POST'])
def chat():
  global conversation_history
  user_message = request.json.get("message")

  if not user_message:
    return jsonify({"error": "Please provide a message."}), 400

  conversation_history.append({"role": "user", "content": user_message})

  prompt = {
    "messages": conversation_history,
    "max_tokens": 150,
    "n": 1,
    "stop": None,
    "temperature": 0.8,
    "top_p": 1
  }

  response = openai.ChatCompletion.create(model="gpt-4",
                                          messages=conversation_history)

  ai_message = response['choices'][0]['message']['content'].strip()
  conversation_history.append({"role": "assistant", "content": ai_message})

  return jsonify({"message": ai_message})


if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=81)
