from flask import Flask, request, jsonify, render_template
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY')  # Hämta API-nyckeln från miljövariablerna

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data['prompt']

    response = openai.Completion.create(
        model="ft:davinci-002:personal::9oodlELn",
        prompt=prompt,
        max_tokens=100,  # Öka antalet tokens för att få längre svar
        temperature=0.1,  # Justera temperaturen för att påverka svarens variation
        stop=["\n", " Användare:", " PatentGPT:"]  # Lägg till stoppsekvenser
    )

    text = response.choices[0].text.strip()

    # Kontrollera om svaret är fullständigt
    if not text.endswith("."):
        response = openai.Completion.create(
            model="ft:davinci-002:personal::9ntOjhpW",  # Ersätt med rätt modell-ID
            prompt=prompt + text,
            max_tokens=100,  # Fler tokens för att avsluta svaret
            temperature=0.7,
            stop=["\n", " Användare:", " PatentGPT:"]
        )
        text += response.choices[0].text.strip()

    return jsonify(text)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
