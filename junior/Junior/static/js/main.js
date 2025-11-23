const visit_random = () => {

    var urls = new Array();

    urls[0] = "https://www.python.org/";
    urls[1] = "https://getbootstrap.com/docs/5.1/getting-started/introduction/";
    urls[2] = "https://reactjs.org";
    urls[3] = "https://w3.org";
    urls[4] = "https://flask.palletsprojects.com/en/2.1.x/#"
    urls[5] = "https://www.youtube.com/watch?v=6jXkhxJ9Sw0"

    var random = Math.floor(Math.random() * urls.length);

    window.open(urls[random]);
};

let intervalId = null;

const add_item = () => {
    const response =
            fetch('http://127.0.0.1:5000/push?item=burp').then((res) => {
                }
            ).catch((err) => {
                alert(err.message);
            });
}

const toggle_pulses = () => {
    if (!intervalId) {
        intervalId = setInterval(add_item,5000)
        document.getElementById("ptoggler").value = "stop";

    } else {
        clearInterval(intervalId);
        intervalId = null
        document.getElementById("ptoggler").value = "start";
    }
}

