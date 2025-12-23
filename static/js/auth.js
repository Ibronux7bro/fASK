function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    // Frontend validation
    if (!email || !password) {
        showError("All fields are required");
        return;
    }

    fetch("http://127.0.0.1:5000/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    })
    .then(res => res.json())
    .then(data => {
        if (data.access_token) {
            localStorage.setItem("token", data.access_token);
            window.location.href = "invoices.html";
        } else {
            showError("Invalid login credentials");
        }
    })
    .catch(() => {
        showError("Server error");
    });
}

function showError(msg) {
    document.getElementById("error").innerText = msg;
}
