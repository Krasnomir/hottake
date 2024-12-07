const upvoteBtns = window.document.querySelectorAll('.upvote');
const downvoteBtns = window.document.querySelectorAll('.downvote');

// get cookie vaue
function getCookie(name) {
    let cookieValue = null;

    if (window.document.cookie && window.document.cookie !== '') {
        const cookies = window.document.cookie.split(';');

        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function sendVoteRequest(postId, type) {
    // send POST request to the server using csrf token
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/home/', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    xhr.send(JSON.stringify({
        post_id: postId,
        vote_type: type
    }));

    // recieving servers response
    xhr.onload = function () {
        if (xhr.status >= 200 && xhr.status < 300) {
            // Successful response (status code 200-299)
            const response = JSON.parse(xhr.responseText);  // Parse the response as JSON
            console.log(response.message);  // Log the response message
        } else {
            // Handle error responses (status code 400-599)
            console.error('Request failed with status:', xhr.status);
        }
    };
}

upvoteBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        sendVoteRequest(btn.getAttribute('data-post-id'), 'upvote');
    });
});

downvoteBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        sendVoteRequest(btn.getAttribute('data-post-id'), 'downvote');
    });
});