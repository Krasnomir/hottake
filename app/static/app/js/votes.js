const postUpvoteBtns = window.document.querySelectorAll('.wrapper .body .article .post .upvote');
const postDownvoteBtns = window.document.querySelectorAll('.wrapper .body .article .post .downvote');

const commentUpvoteBtns = window.document.querySelectorAll('.wrapper .body .article .comment .upvote');
const commentDownvoteBtns = window.document.querySelectorAll('.wrapper .body .article .comment .downvote');

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

function sendVoteRequest(id, type, voteElement, commentOrPost) {
    // send POST request to the server using csrf token
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/home/', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    xhr.send(JSON.stringify({
        commentOrPost: commentOrPost,
        id: id,
        vote_type: type
    }));

    // recieving servers response
    xhr.onload = () => {
        const response = JSON.parse(xhr.responseText);  // Parse the response as JSON

        switch(response.msg) {
            case 1: // changed from upvote to downvote
                voteElement.uCounter.innerHTML = voteElement.uCounter.innerHTML - 1; 
                voteElement.dCounter.innerHTML = parseInt(voteElement.dCounter.innerHTML) + 1;
                break; // Prevent falling through to the next case
    
            case 2: // changed from downvote to upvote
                voteElement.uCounter.innerHTML = parseInt(voteElement.uCounter.innerHTML) + 1;
                voteElement.dCounter.innerHTML = parseInt(voteElement.dCounter.innerHTML) - 1;
                break;
    
            case 3: // downvoted for the first time
                voteElement.dCounter.innerHTML = parseInt(voteElement.dCounter.innerHTML) + 1;
                break;
    
            case 4: // upvoted for the first time
                voteElement.uCounter.innerHTML = parseInt(voteElement.uCounter.innerHTML) + 1;
                break;
        }
    };
      
}

// vote elements basically represent the voting panels for each post and allow the script to change the vote count dynamically without having to refresh the page

postUpvoteBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const voteElement = {
            dCounter: btn.parentElement.children[1].children[1],
            uCounter: btn.children[1]
        };

        sendVoteRequest(btn.getAttribute('data-post-id'), 'upvote', voteElement, 'post');
    });
});

postDownvoteBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const voteElement = {
            dCounter: btn.children[1],
            uCounter: btn.parentElement.children[0].children[1]
        };

        sendVoteRequest(btn.getAttribute('data-post-id'), 'downvote', voteElement, 'post');
    });
});

commentUpvoteBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const voteElement = {
            dCounter: btn.parentElement.children[1].children[1],
            uCounter: btn.children[1]
        };

        sendVoteRequest(btn.getAttribute('data-comment-id'), 'upvote', voteElement, 'comment');
    });
});

commentDownvoteBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const voteElement = {
            dCounter: btn.children[1],
            uCounter: btn.parentElement.children[0].children[1]
        };

        sendVoteRequest(btn.getAttribute('data-comment-id'), 'downvote', voteElement, 'comment');
    });
});