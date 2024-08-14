from flask import Flask, request, jsonify, render_template
import openai
import os

app = Flask(__name__)


def is_response_relevant(response):
    # Kontrollera om svaret innehåller nyckelord relaterade till patent
    patent_keywords = ["patent", "uppfinning", "registrering", "PRV", "immateriella rättigheter", "varumärke"]
    return any(keyword in response.lower() for keyword in patent_keywords)

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
        response = openai.Completion.create(
            model="ft:davinci-002:personal::9oodlELn",
            prompt=prompt,
            max_tokens=100,
            temperature=0.5,
            stop=["\n", " Användare:", " PatentGPT:", "END"]
        )
        generated_text = response.choices[0].text.strip()

        # Kontrollera om svaret är relevant och giltigt
        if not is_response_relevant(generated_text):
            generated_text = (
                "Det verkar som att din fråga inte direkt handlar om patent och registrering. "
                "För mer detaljerad och specifik information, vänligen kontakta Patent- och registreringsverket (PRV). "
                "Du kan besöka deras hemsida på [www.prv.se](http://www.prv.se) för att läsa mer eller använda deras online-tjänster. "
                "Om du föredrar personlig kontakt, ring 08-782 28 00 eller skicka ett mejl till kundsupport@prv.se."
            )

        improvement_prompt = f"Förbättra följande svar så att det är mer informativt och användarvänligt och håll det kort och använd radbrytningar:\n\n{generated_text}"
        improvement_response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Du är en hjälpsam assistent och förbättrar svar för att göra dem mer informativa och användarvänliga."},
                {"role": "user", "content": improvement_prompt}
            ],
            max_tokens=400,
            temperature=0.6,
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