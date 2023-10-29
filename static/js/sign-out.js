function signOut() {
    const confirmed = confirm('Are you sure you want to log out?');
    if (!confirmed) {
        return false;
    }
    fetch('/auth/jwt/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(function (response) {
            if (response.ok) {
                window.location.href = 'http://' + window.location.host;
            } else {
                console.error('Error logging out user');
            }
        })
}
