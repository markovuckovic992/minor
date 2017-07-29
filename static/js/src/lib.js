const getCookie = (name) => {
    var cookieValue = null, cookies, i, cookie
    if (document.cookie && document.cookie != '') {
        cookies = document.cookie.split(';')
        for (i = 0; i < cookies.length; i++) {
            cookie = cookies[i].trim()
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
                break
            }
        }
    }
    return cookieValue
}

const csrftoken = getCookie('csrftoken')

export const myFetch = (url, post_data) => (
    fetch(url, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(post_data),
        credentials:"include"
    }).then(response => response.json())
)