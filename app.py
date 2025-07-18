import re
from flask import Flask, render_template, request, jsonify

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
    if re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
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

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check():
    password = request.json.get("password", "")
    result = password_strength_checker(password.strip())
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
