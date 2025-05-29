from flask import Flask, request, render_template_string
import hashlib

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Kiểm tra tính toàn vẹn file ảnh bằng SHA512</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f5f8fa;
            padding: 30px;
            max-width: 700px;
            margin: auto;
            color: #333;
        }
        h2 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }
        form {
            background: white;
            padding: 25px 30px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        label {
            font-weight: 600;
            display: block;
            margin-bottom: 8px;
            margin-top: 15px;
        }
        input[type="file"] {
            font-size: 14px;
        }
        textarea {
            width: 100%;
            font-family: monospace;
            font-size: 14px;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            resize: vertical;
        }
        input[type="submit"] {
            margin-top: 20px;
            background-color: #3498db;
            border: none;
            color: white;
            font-size: 16px;
            padding: 12px 25px;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            display: block;
            width: 100%;
        }
        input[type="submit"]:hover {
            background-color: #2980b9;
        }
        .result {
            margin-top: 30px;
            padding: 20px;
            border-radius: 8px;
            background-color: #ecf0f1;
            font-family: monospace;
            word-break: break-all;
        }
        .success {
            color: #27ae60;
            font-weight: 700;
            font-size: 18px;
        }
        .error {
            color: #c0392b;
            font-weight: 700;
            font-size: 18px;
        }
    </style>
</head>
<body>
    <h2>Kiểm tra tính toàn vẹn file ảnh bằng SHA512</h2>
    <form method="POST" enctype="multipart/form-data">
        <label>Chọn file ảnh:</label>
        <input type="file" name="file" required>

        <label>Nhập hash SHA512 tham chiếu:</label>
        <textarea name="expected_hash" rows="4" placeholder="Nhập hash SHA512 của file gốc" required></textarea>

        <input type="submit" value="Kiểm tra">
    </form>

    {% if result is not none %}
        <div class="result">
            <p>Hash tính được: <code>{{ computed_hash }}</code></p>
            <p>Hash tham chiếu: <code>{{ expected_hash }}</code></p>
            {% if result %}
                <p class="success">✔ File hợp lệ! Hash trùng khớp.</p>
            {% else %}
                <p class="error">✘ File không hợp lệ! Hash không trùng.</p>
            {% endif %}
        </div>
    {% endif %}
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        expected_hash = request.form.get("expected_hash").strip().lower()

        if not file:
            return render_template_string(HTML, result=None)

        file_bytes = file.read()
        computed_hash = hashlib.sha512(file_bytes).hexdigest()
        is_valid = (computed_hash == expected_hash)

        return render_template_string(HTML, result=is_valid, computed_hash=computed_hash, expected_hash=expected_hash)

    return render_template_string(HTML, result=None)


if __name__ == "__main__":
    app.run(debug=True)
