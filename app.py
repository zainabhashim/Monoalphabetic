from flask import Flask, render_template, request
import os
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'

# توليد مفتاح عشوائي عند كل تشغيل
def generate_key():
    letters = list("abcdefghijklmnopqrstuvwxyz")
    shuffled = letters.copy()
    random.shuffle(shuffled)
    return dict(zip(letters, shuffled))

def parse_key_string(key_str):
    key_map = {}
    pairs = key_str.lower().split(',')
    for pair in pairs:
        if ':' in pair:
            k, v = pair.split(':')
            key_map[k.strip()] = v.strip()
    return key_map

def mono_encrypt(text, key_map):
    result = ""
    for char in text:
        if char.isalpha():
            if char.islower():
                result += key_map.get(char, char)
            else:
                result += key_map.get(char.lower(), char).upper()
        else:
            result += char
    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    plaintext = ''
    result = ''
    keymap = ''

    if request.method == 'POST':
        plaintext = request.form.get('plaintext', '')
        keymap = request.form.get('keymap', '')

        try:
            key_dict = parse_key_string(keymap)
            result = mono_encrypt(plaintext, key_dict)
        except Exception as e:
            result = f"⚠️ Error in key: {e}"

    else:
        # عند أول تحميل، يولد مفتاح جديد
        generated_key = generate_key()
        keymap = ', '.join(f'{k}:{v}' for k, v in generated_key.items())

    return render_template('index.html', plaintext=plaintext, result=result, keymap=keymap)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
