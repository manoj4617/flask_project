function thispost() {
    var mytitle = document.querySelector('#title').value;
    var mypos = document.querySelector('#postBody').value;
    var send_post = {
        title: mytitle,
        bdy: mypos
    }

    fetch('/rev_post', {
            method: "POST",
            credentials: "include",
            body: JSON.stringify(send_post),
            cache: "no-cache",
            headers: new Headers({
                'content-type': "application/json"
            })
        })
        .then(function(response) {
            if (response.status !== 200) {
                console.log(`Looks like there was a problem. Status code: ${response.status}`);
                return;
            }
            response.json().then(function(data) {
                d = data;
                console.log(d);
                document.querySelector('#message').innerHTML = "Your post added";
            })
        })
}