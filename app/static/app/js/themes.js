const cookie = {
    get(name) {
        let cookieValue = null;

        if (window.document.cookie && window.document.cookie !== '') {
            const cookies = window.document.cookie.split(';');

            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },
    set(name,value,days) {
        var expires = "";
        if(days) {
            var date = new Date();
            date.setTime(date.getTime() + (days*24*60*60*1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "")  + expires + "; path=/";
    }
}

if(cookie.get('theme') == "dark") {
    document.querySelector('.wrapper').setAttribute('data-theme', 'dark');
}
else {  
    document.querySelector('.wrapper').setAttribute('data-theme', 'light');
}

document.querySelector(".wrapper #theme-selector").addEventListener("click", () => {

    const wrapper = document.querySelector('.wrapper');

    if(wrapper.getAttribute('data-theme') == 'dark') {
        wrapper.setAttribute('data-theme', 'light');
        document.querySelector(".wrapper #theme-selector").innerHTML = "🌕";
        cookie.set('theme', 'light', 30);
    }
    else {
        wrapper.setAttribute('data-theme', 'dark');
        document.querySelector(".wrapper #theme-selector").innerHTML = "☀️";
        cookie.set('theme', 'dark', 30);
    }
});