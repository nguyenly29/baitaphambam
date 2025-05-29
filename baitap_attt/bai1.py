from flask import Flask, render_template, request
import hashlib

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    hash_result = ''
    if request.method == 'POST':
        data = request.form['data']
        hash_type = request.form['hash_type']
        
        if hash_type == 'sha256':
            hash_result = hashlib.sha256(data.encode()).hexdigest()
        elif hash_type == 'sha512':
            hash_result = hashlib.sha512(data.encode()).hexdigest()
    
    return render_template('index.html', hash_result=hash_result)

if __name__ == '__main__':
    app.run(debug=True)