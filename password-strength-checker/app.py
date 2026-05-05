# app.py

from flask import Flask, render_template_string, request, jsonify
import random
import string
import re

app = Flask(__name__)

HTML = """

<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Password Security Toolkit</title>

    <link rel="preconnect" href="https://fonts.googleapis.com">

    <style>

        *{
            margin:0;
            padding:0;
            box-sizing:border-box;
            font-family:'Segoe UI',sans-serif;
        }

        body{
            min-height:100vh;
            background:
            linear-gradient(135deg,#0f172a,#111827,#1e293b);
            display:flex;
            justify-content:center;
            align-items:center;
            padding:40px 20px;
            color:white;
        }

        .wrapper{
            width:100%;
            max-width:1200px;
        }

        .main-title{
            text-align:center;
            margin-bottom:40px;
        }

        .main-title h1{
            font-size:42px;
            margin-bottom:10px;
            font-weight:700;
        }

        .main-title p{
            color:#cbd5e1;
            font-size:17px;
        }

        .container{
            display:grid;
            grid-template-columns:1fr 1fr;
            gap:30px;
        }

        .card{
            background:rgba(255,255,255,0.08);
            backdrop-filter:blur(12px);
            border:1px solid rgba(255,255,255,0.1);
            border-radius:24px;
            padding:35px;
            box-shadow:0 10px 30px rgba(0,0,0,0.35);
        }

        .card h2{
            font-size:28px;
            margin-bottom:25px;
        }

        .input-wrapper{
            position:relative;
            margin-bottom:20px;
        }

        .input-box{
            width:100%;
            padding:16px 55px 16px 18px;
            border:none;
            border-radius:14px;
            background:rgba(255,255,255,0.12);
            color:white;
            font-size:16px;
            outline:none;
            transition:0.3s;
        }

        .input-box::placeholder{
            color:#cbd5e1;
        }

        .input-box:focus{
            background:rgba(255,255,255,0.18);
            border:1px solid #60a5fa;
        }

        .toggle-btn{
            position:absolute;
            right:15px;
            top:50%;
            transform:translateY(-50%);
            background:none;
            border:none;
            color:#cbd5e1;
            cursor:pointer;
            font-size:14px;
        }

        .strength-header{
            display:flex;
            justify-content:space-between;
            margin-bottom:10px;
            font-size:16px;
        }

        .progress{
            width:100%;
            height:12px;
            background:rgba(255,255,255,0.1);
            border-radius:20px;
            overflow:hidden;
            margin-bottom:25px;
        }

        .progress-bar{
            height:100%;
            width:0%;
            transition:0.4s ease;
            border-radius:20px;
        }

        .features{
            display:grid;
            grid-template-columns:1fr 1fr;
            gap:12px;
        }

        .feature{
            background:rgba(255,255,255,0.06);
            padding:12px;
            border-radius:12px;
            font-size:14px;
        }

        .btn{
            width:100%;
            padding:16px;
            border:none;
            border-radius:14px;
            background:linear-gradient(135deg,#2563eb,#3b82f6);
            color:white;
            font-size:16px;
            font-weight:600;
            cursor:pointer;
            transition:0.3s;
            margin-top:20px;
        }

        .btn:hover{
            transform:translateY(-2px);
            opacity:0.95;
        }

        .copy-btn{
            background:
            linear-gradient(135deg,#059669,#10b981);
        }

        .generated-password{
            margin-top:20px;
        }

        .copy-message{
            margin-top:15px;
            text-align:center;
            color:#4ade80;
            display:none;
            font-weight:600;
        }

        .info-text{
            color:#cbd5e1;
            line-height:1.7;
            margin-bottom:10px;
        }

        .footer{
            text-align:center;
            margin-top:35px;
            color:#94a3b8;
            font-size:14px;
        }

        @media(max-width:900px){

            .container{
                grid-template-columns:1fr;
            }

            .main-title h1{
                font-size:34px;
            }

        }

    </style>

</head>

<body>

<div class="wrapper">

    <div class="main-title">

        <h1>Password Security Toolkit</h1>

        <p>
            Analyze password strength and generate secure passwords instantly
        </p>

    </div>

    <div class="container">

        <!-- Password Checker -->

        <div class="card">

            <h2>Password Strength Checker</h2>

            <div class="input-wrapper">

                <input
                    type="password"
                    id="password"
                    class="input-box"
                    placeholder="Enter your password"
                >

                <button
                    class="toggle-btn"
                    onclick="togglePassword('password', this)"
                >
                    Show
                </button>

            </div>

            <div class="strength-header">

                <span>Password Strength</span>

                <span id="strengthText">None</span>

            </div>

            <div class="progress">

                <div class="progress-bar" id="progressBar"></div>

            </div>

            <div class="features">

                <div class="feature" id="length">
                     Minimum 8 Characters
                </div>

                <div class="feature" id="upper">
                     Uppercase Letter
                </div>

                <div class="feature" id="lower">
                     Lowercase Letter
                </div>

                <div class="feature" id="number">
                     Number
                </div>

                <div class="feature" id="special">
                     Special Character
                </div>

            </div>

        </div>

        <!-- Password Generator -->

        <div class="card">

            <h2>Password Generator</h2>

            <p class="info-text">

                Generate strong random passwords using uppercase,
                lowercase, numbers, and symbols.

            </p>

            <button class="btn" onclick="generatePassword()">

                Generate Secure Password

            </button>

            <div class="generated-password">

                <input
                    type="text"
                    id="generatedPassword"
                    class="input-box"
                    readonly
                >

            </div>

            <button class="btn copy-btn" onclick="copyPassword()">

                Copy Password

            </button>

            <div class="copy-message" id="copyMessage">

                ✅ Password copied successfully

            </div>

        </div>

    </div>

    <div class="footer">

        Developed using Python Flask

    </div>

</div>

<script>

    const passwordInput =
        document.getElementById("password");

    passwordInput.addEventListener("input", function(){

        fetch("/check_password", {

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                password:passwordInput.value
            })

        })

        .then(response => response.json())

        .then(data => {

            document.getElementById("strengthText").innerHTML =
                data.strength;

            const bar =
                document.getElementById("progressBar");

            bar.style.width =
                data.percent + "%";

            bar.style.background =
                data.color;

            updateFeature("length", data.length);
            updateFeature("upper", data.upper);
            updateFeature("lower", data.lower);
            updateFeature("number", data.number);
            updateFeature("special", data.special);

        });

    });

    function updateFeature(id, status){

        const element =
            document.getElementById(id);

        const text =
            element.innerHTML.substring(2);

        if(status){

            element.innerHTML =
                "✅ " + text;

            element.style.color =
                "#4ade80";

        }
        else{

            element.innerHTML =
                "❌ " + text;

            element.style.color =
                "#f87171";

        }

    }

    function generatePassword(){

        fetch("/generate_password")

        .then(response => response.json())

        .then(data => {

            document.getElementById(
                "generatedPassword"
            ).value = data.password;

            document.getElementById(
                "copyMessage"
            ).style.display = "none";

        });

    }

    function copyPassword(){

        const passwordField =
            document.getElementById("generatedPassword");

        navigator.clipboard.writeText(
            passwordField.value
        );

        const copyMessage =
            document.getElementById("copyMessage");

        copyMessage.style.display = "block";

        setTimeout(() => {

            copyMessage.style.display = "none";

        }, 2500);

    }

    function togglePassword(id, button){

        const input =
            document.getElementById(id);

        if(input.type === "password"){

            input.type = "text";

            button.innerHTML = "Hide";

        }
        else{

            input.type = "password";

            button.innerHTML = "Show";

        }

    }

</script>

</body>
</html>

"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/check_password", methods=["POST"])
def check_password():

    data = request.get_json()

    password = data["password"]

    length = len(password) >= 8
    upper = re.search(r"[A-Z]", password)
    lower = re.search(r"[a-z]", password)
    number = re.search(r"[0-9]", password)
    special = re.search(r"[^A-Za-z0-9]", password)

    checks = [length, upper, lower, number, special]

    score = sum(bool(x) for x in checks)

    if score <= 2:

        strength = "Weak"
        color = "#ef4444"
        percent = 33

    elif score <= 4:

        strength = "Medium"
        color = "#f59e0b"
        percent = 66

    else:

        strength = "Strong"
        color = "#22c55e"
        percent = 100

    return jsonify({

        "strength": strength,
        "color": color,
        "percent": percent,

        "length": bool(length),
        "upper": bool(upper),
        "lower": bool(lower),
        "number": bool(number),
        "special": bool(special)

    })

@app.route("/generate_password")
def generate_password():

    characters = (

        string.ascii_letters +
        string.digits +
        "!@#$%^&*()_+-="

    )

    password = "".join(

        random.choice(characters)

        for _ in range(16)

    )

    return jsonify({
        "password": password
    })

if __name__ == "__main__":
    app.run(debug=True)