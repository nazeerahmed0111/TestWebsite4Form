from flask import Flask, render_template, request, redirect, url_for
import os
import json
import openai

app = Flask(__name__)
DATA_DIR = "D:\\VSCodes\\test-form\\status-site\\submissions\\"
os.makedirs(DATA_DIR, exist_ok=True)

openai.api_key = 'your-openai-api-key-here'  # Replace with your actual Azure/OpenAI key

def get_next_ref_number(first_name, last_name):
    base_name = f"{first_name.lower()}_{last_name.lower()}"
    files = os.listdir(DATA_DIR)
    matching = [
        int(f.split('_')[-1].split('.')[0])
        for f in files
        if f.startswith(base_name) and f.endswith('.json') and f.split('_')[-1].split('.')[0].isdigit()
    ]
    return max(matching, default=0) + 1


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_name = request.form.get('firstName').strip()
        last_name = request.form.get('lastName').strip()

        data = {
            "firstName": first_name,
            "lastName": last_name,
            "email": request.form.get('email'),
            "phone": request.form.get('phone'),
            "favfood1": request.form.get('favfood1'),
            "favfood2": request.form.get('favfood2'),
            "favfood3": request.form.get('favfood3'),
        }

        ref_num = get_next_ref_number(first_name, last_name)
        safe_name = f"{first_name.lower()}_{last_name.lower()}_{ref_num}.json"
        filepath = os.path.join(DATA_DIR, safe_name)

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)

        return redirect(url_for('index', submitted='true'))

    submitted = request.args.get('submitted') == 'true'
    return render_template('index.html', submitted=submitted)


@app.route('/search', methods=['GET', 'POST'])
def search():
    result = ''
    if request.method == 'POST':
        first = request.form.get('firstName', '').strip()
        last = request.form.get('lastName', '').strip()

        for filename in os.listdir(DATA_DIR):
            if filename.endswith('.json'):
                with open(os.path.join(DATA_DIR, filename)) as f:
                    data = json.load(f)
                    if data.get('firstName') == first and data.get('lastName') == last:
                        favs = [data.get('favfood1', ''), data.get('favfood2', ''), data.get('favfood3', '')]
                        prompt = f"Suggest good restaurants in Chennai for someone who likes: {', '.join(favs)}."
                        try:
                            response = openai.ChatCompletion.create(
                                engine="your-deployment-name",  # Replace with your deployment name
                                messages=[{"role": "user", "content": prompt}],
                                max_tokens=150,
                                temperature=0.7
                            )
                            result = response['choices'][0]['message']['content']
                        except Exception as e:
                            result = f"Error calling GPT API: {e}"
                        break
        if not result:
            result = "No matching submission found."

    return render_template('search.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)