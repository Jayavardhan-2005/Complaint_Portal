function validateLoginForm() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    if (!email || !password) {
        alert('Please fill in all fields');
        return false;
    }
    if (!email.includes('@')) {
        alert('Please enter a valid email');
        return false;
    }
    return true;
}

function validateRegisterForm() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const role = document.getElementById('role').value;
    if (!email || !password || !role) {
        alert('Please fill in all fields');
        return false;
    }
    if (!email.includes('@')) {
        alert('Please enter a valid email');
        return false;
    }
    if (password.length < 6) {
        alert('Password must be at least 6 characters');
        return false;
    }
    return true;
}