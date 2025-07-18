import re
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

def password_strength_checker(password):
    score = 0
    feedback = []

    # Check password length
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Increase the password length to at least 8 characters.")

    # Check for uppercase letter
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Add at least one uppercase letter.")

    # Check for lowercase letter
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Add at least one lowercase letter.")

    # Check for numeral
    if re.search(r'[0-9]', password):
        score += 1
    else:
        feedback.append("Include at least one numeral.")

    # Check for special character
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    else:
        feedback.append("Include at least one special character (e.g., @, #, $).")

    # Check for repeated characters or common patterns
    if len(password) > 0 and len(set(password)) / len(password) < 0.5:
        feedback.append("Avoid repeated characters or predictable patterns.")

    # Check for common words or patterns like 'password', '12345', etc.
    if re.search(r'(password|12345|qwerty|admin)', password, re.IGNORECASE):
        feedback.append("Avoid using common words or patterns like 'password' or '12345'.")

    # Assign strength based on score
    if score >= 6:
        strength = "Strong"
    elif score >= 4:
        strength = "Moderate"
    else:
        strength = "Weak"
        feedback.append("Consider combining suggestions above for a stronger password.")

    return {
        "strength": strength,
        "score": score,
        "feedback": feedback
    }

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Password Strength Checker</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f4f4; margin: 0; padding: 0; }
        .container { max-width: 400px; margin: 60px auto; background: #fff; padding: 30px 40px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);}
        h2 { text-align: center; color: #333; }
        label { font-weight: bold; }
        input[type="password"] { width: 100%; padding: 10px; margin: 10px 0 20px 0; border: 1px solid #ccc; border-radius: 4px; }
        button { width: 100%; padding: 10px; background: #0078d7; color: #fff; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; }
        button:hover { background: #005fa3; }
        .result { margin-top: 20px; }
        .strength { font-weight: bold; }
        .score { color: #555; }
        ul { margin-top: 10px; padding-left: 20px; }
        li { color: #b00; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Password Strength Checker</h2>
        <form id="passwordForm">
            <label for="password">Enter your password:</label>
            <input type="password" id="password" name="password" required>
            <button type="submit">Check Strength</button>
        </form>
        <div class="result" id="result" style="display:none;">
            <div class="strength" id="strength"></div>
            <div class="score" id="score"></div>
            <ul id="feedback"></ul>
        </div>
    </div>
    <script>
        document.getElementById('passwordForm').onsubmit = async function(e) {
            e.preventDefault();
            const password = document.getElementById('password').value;
            const res = await fetch('/check', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({password})
            });
            const data = await res.json();
            document.getElementById('result').style.display = 'block';
            document.getElementById('strength').textContent = "Password Strength: " + data.strength;
            document.getElementById('score').textContent = "Score: " + data.score + "/6";
            const feedback = document.getElementById('feedback');
            feedback.innerHTML = "";
            data.feedback.forEach(function(msg) {
                const li = document.createElement('li');
                li.textContent = msg;
                feedback.appendChild(li);
            });
        }
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML)

@app.route("/check", methods=["POST"])
def check():
    password = request.json.get("password", "")
    result = password_strength_checker(password.strip())
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
