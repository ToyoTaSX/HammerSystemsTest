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

function sendCode() {
    const number = document.getElementById('phone_number').value;
    document.getElementById('error-container').style.display = 'none';
    fetch("/auth/send-code/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: new URLSearchParams({ 'number': number })
    })
    .then(response => {
            if (response.ok) {
                return response.json()
            }
            showErrorMessage(response)
            throw new Error();
        })
    .then(data => {
        localStorage.setItem('verification_code', data.code);
        localStorage.setItem('phone_number', number);
        document.getElementById('code-span').innerText= 'code: ' + data.code;
        document.getElementById('step-1').style.display = 'none';
        document.getElementById('step-2').style.display = 'flex';
    });
}

function verifyCode() {
    const number = localStorage.getItem('phone_number');;
    const code = document.getElementById('verify_code').value;
    document.getElementById('error-container').style.display = 'none';
    fetch("/auth/verification-code/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: new URLSearchParams({'number': number, 'code': code})
    })
        .then(response => {
            if (response.ok) {
                return response.json()
            }
            showErrorMessage(response)
            throw new Error();
        })
        .then(data => {
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('refresh_token', data.refresh_token);
            redirectToPageWithToken('/')
        });
}

function redirectToPageWithToken(url) {
    fetch(url, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
    })
    .then(response => {
        if (response.ok) {
            window.location.href = url;
        } else {
            console.error('Ошибка при передаче токена');
        }
    })
    .catch(error => {
        console.error('Ошибка сети', error);
    });
}

function showErrorMessage(response) {
    console.log(response.text())
    document.getElementById('error-container').style.display = 'flex';
    const errorMessageElement = document.getElementById('error-text');
    errorMessageElement.innerHTML = 'Ошибка ' + response.status;
}