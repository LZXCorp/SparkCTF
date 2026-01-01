<?php
$right_username = "tom";
$right_password = "sparky";
$login_success = false;

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST['Username'];
    $password = $_POST['Password'];

    if ($username === $right_username && $password === $right_password) {
        $login_success = true;
    } else {
        echo "<script>alert('Wrong Credentials, try again!');</script>";
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Mango Company</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        body {
            font-family: Georgia, sans-serif;
            background: linear-gradient(135deg, #ffecd2, #fcb69f);
            margin: 0;
            padding: 0;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .container {
            background: #fff;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
            width: 100%;
            max-width: 400px;
            text-align: center;
        }

        h1 {
            color: orangered;
        }

        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 10px;
            margin-top: 0.3rem;
            border: 1px solid #ccc;
            border-radius: 6px;
            box-sizing: border-box;
            transition: border-color 0.2s;
        }

        input[type="submit"] {
            margin-top: 1.5rem;
            background: orangered;
            color: #fff;
            font-weight: bold;
            border: none;
            padding: 12px;
            width: 100%;
            border-radius: 6px;
            cursor: pointer;
        }

        input[type="submit"]:hover {
            background: darkorange;
        }

        .footer {
            margin-top: 1rem;
            font-size: 0.9rem;
            color: #777;
        }

        .popup-overlay {
            position: fixed;
            top: 0; left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.6);
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            z-index: 999;
        }

        .popup {
            background: #fff;
            padding: 2rem 3rem;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            text-align: center;
            animation: pop 0.5s ease-out;
        }

        @keyframes pop {
            from { transform: scale(0.8); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }

        .flag {
            display: inline-block;
            background: #222;
            color: #00ff99;
            font-family: monospace;
            font-size: 1.2rem;
            padding: 10px 15px;
            margin-top: 1rem;
            border-radius: 8px;
        }

        .confetti {
            position: fixed;
            top: 0; left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            overflow: hidden;
            z-index: 1;
        }

        .confetti div {
            position: absolute;
            width: 10px;
            height: 10px;
            background: hsl(var(--hue), 70%, 50%);
            top: -10px;
            animation: fall linear forwards;
        }

        @keyframes fall {
            to { transform: translateY(110vh) rotate(720deg); }
        }
    </style>
</head>

<body>
    <div class="container">
        <h1>Mango Company</h1>
        <h2>Login</h2>
        <form method="POST" action="">
            <label for="Username">Username:</label>
            <input type="text" id="Username" name="Username" required>

            <label for="Password">Password:</label>
            <input type="password" id="Password" name="Password" required>

            <input type="submit" value="Login">
        </form>
        <div class="footer">© 2025 Mango Company</div>
    </div>

    <?php if ($login_success): ?>
        <div class="popup-overlay">
            <div class="confetti" id="confetti"></div>
            <div class="popup">
                <h1>🎉 Mango Company</h1>
                <h4>Thanks for helping me find my password! Here's the flag:</h4>
                <div class="flag">SPARK{s3t_g0od_p5wd5}</div>
            </div>
        </div>
        <script>
            const confetti = document.getElementById('confetti');
            for (let i = 0; i < 80; i++) {
                const piece = document.createElement('div');
                piece.style.setProperty('--hue', Math.floor(Math.random() * 360));
                piece.style.left = Math.random() * 100 + 'vw';
                piece.style.animationDuration = (2 + Math.random() * 3) + 's';
                piece.style.animationDelay = Math.random() * 2 + 's';
                confetti.appendChild(piece);
            }
        </script>
    <?php endif; ?>
</body>
</html>
