function updatethispost(pid) {
    var newpost = {
        postid: pid,
        newtitle: document.querySelector('#title').value,
        newbdy: document.querySelector('#bdy').value
    }
    console.log(newpost);

    fetch('/updatedpost', {
            method: "POST",
            credentials: "include",
            body: JSON.stringify(newpost),
            cache: "no-cache",
            headers: new Headers({
                'content-type': "application/json"
            })
        })
        .then(function(response) {
            if (response.status !== 200) {
                console.log("Something wen badly wrong")
                return;
            }
            response.json().then(function(data) {
                rev = data;
                console.log(rev);
                document.querySelector('#message').innerHTML = rev["message"];
            })
        })
}