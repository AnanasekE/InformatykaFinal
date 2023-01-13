import hashlib
import itertools
import string

from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/hash', methods=['POST'])
def hash_message():
    message = request.form['message']
    hash = custom_hash(message)
    return render_template('results.html', message=message, hash=hash)


def custom_hash(message):
    ascii_values = [ord(c) for c in message]
    combined = sum(ascii_values)
    key = combined % 24
    encrypted = ""
    for c in message:
        encrypted += chr((ord(c) + key) % 24 + 97)
    return encrypted


def crack_hash_brute_force(hash, max_length):
    for length in range(1, max_length + 1):
        for message in itertools.product(string.ascii_letters + string.digits, repeat=length):
            message_str = "".join(message)
            message_hash = custom_hash(message_str)
            if message_hash == hash:
                return message_str
    return "Hash not found"


def crack_hash_wordlist(hash, wordlist):
    for word in wordlist:
        word = word.strip()
        message_hash = custom_hash(word)
        if message_hash == hash:
            return word
    return "Hash not found"


@app.route('/crack', methods=['POST'])
def crack_hash():
    hash = request.form['hash']
    cracking_method = request.form['cracking_method']
    if cracking_method == 'wordlist':
        wordlist_path = request.form['wordlist']
        print(wordlist_path)
        with open(wordlist_path, 'r') as f:
            wordlist = f.read().splitlines()
        message = crack_hash_wordlist(hash, wordlist)
    else:
        max_length = int(request.form['max_length'])
        message = crack_hash_brute_force(hash, max_length)
    return render_template('results.html', message=message, hash=hash)


if __name__ == '__main__':
    app.run()
