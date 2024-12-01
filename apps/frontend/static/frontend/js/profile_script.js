function sendInviteCode() {
    const code = document.getElementById('invite_code').value;
    fetch("/users/invite-code/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken'),
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: new URLSearchParams({ 'invite_code': code })
    })
        .then(response => {
            if (response.ok) {
                return response.json()
            } else {
                console.log(response)
                alert('Ошибка')
                throw new Error();
            }
        })
        .then(data => {
            if (response.ok) {
                document.getElementById('invite_code').setAttribute("disabled", true);
                document.getElementById('send-btn').style.display = 'none';
            } else {
                console.log(response)
                alert('Ошибка')
            }
        });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}