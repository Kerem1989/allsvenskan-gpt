from flask import Flask, request, jsonify, render_template
import openai
import os
import re

app = Flask(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY')
def is_response_relevant(response):
    allsvenskan_keywords = ["allsvenskan", "lag", "spelare", "vinst", "säsong", "match", "AIK", "Göteborg", "Malmö"]
    return any(keyword in response.lower() for keyword in allsvenskan_keywords)

def remove_formatting(text):
    text = re.sub(r'\*\*', '', text)
    text = re.sub(r'\*', '', text)
    return text.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    try:

        response = openai.ChatCompletion.create(
            model="ft:gpt-4o-mini-2024-07-18:personal::AZNVqy0Y",
            messages=[{"role": "system", "content": "Du är en expert på Allsvenskan och kan svara på frågor om lag, resultat, spelare och säsonger."},
                      {"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.5
        )

        generated_text = response.choices[0].message['content'].strip()

        formatted_text = remove_formatting(generated_text)

        if not is_response_relevant(formatted_text):
            formatted_text = (
                "Jag tror att din fråga inte handlar om Allsvenskan. Kan du ge mig mer specifik information eller ställa en fråga om något lag, resultat eller spelare?"
            )

        improvement_prompt = f"Förbättra följande svar så att det är mer informativt och användarvänligt utan att använda någon formatering. Var kort och direkt om det handlar om statistik, och ge mer information om det efterfrågas:\n\n{formatted_text}"
        improvement_response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": "Du är en hjälpsam assistent och förbättrar svar för att göra dem mer informativa och användarvänliga."},
                      {"role": "user", "content": improvement_prompt}],
            max_tokens=400,
            temperature=0.5
        )

        improved_text = improvement_response.choices[0].message['content'].strip()

        return jsonify({'response': improved_text})

    except openai.error.OpenAIError as e:
        return jsonify({'error': f'OpenAI API error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
