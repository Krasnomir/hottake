const posts = window.document.querySelectorAll('.wrapper .post');

for (const post of posts) {
    post.querySelector('.post-content').addEventListener('click', () => {
        const postUrl = post.getAttribute('data-url');
        window.location.href = postUrl;
    });
}
