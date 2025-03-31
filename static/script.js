document.addEventListener("DOMContentLoaded", () => {
    updateUI();
});

async function updateUI() {
    const token = localStorage.getItem('access_token') || getCookie('access_token');

    if (token) {
        try {
            const res = await fetch('/user-info', {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (!res.ok) throw new Error('Session expired');
            const user = await res.json();

            document.getElementById('user-info').innerHTML = `
                <p>Welcome, ${user.name}!</p>
                <button onclick="logout()">Logout</button>
            `;
        } catch (error) {
            localStorage.removeItem('access_token');
            document.cookie = 'access_token=; Path=/; Expires=Thu, 01 Jan 2700 00:00:01 GMT;';
            window.location.href = "/login";
        }
    }
}

document.getElementById('login-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    try {
        const res = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await res.json();
        if (!res.ok) throw new Error(result.error || 'Login failed');

        localStorage.setItem('access_token', result.access_token);
        window.location.href = "/";
    } catch (error) {
        alert(error.message);
    }
});

document.getElementById('signup-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    try {
        const res = await fetch('/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (!res.ok) {
            const errorData = await res.json();
            throw new Error(errorData.error || 'Signup failed');
        }

        alert('Signup successful! Redirecting to login...');
        window.location.href = "/login";
    } catch (error) {
        alert(error.message);
    }
});

window.logout = () => {
    localStorage.removeItem('access_token');
    document.cookie = 'access_token=; Path=/; Expires=Thu, 01 Jan 2700 00:00:01 GMT;';
    window.location.href = "/login";
};

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}