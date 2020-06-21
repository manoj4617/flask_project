function show() {
    var temp = document.getElementById("pass");
    if (temp.type === "password") {
        temp.type = "text";
    } else {
        temp.type = "password";
    }
}


function update() {
    console.log(document.querySelector('#name').value);
    console.log(document.querySelector('#username').value);
    console.log(document.querySelector('#email').value);
    console.log(document.querySelector('#pass').value);

    var details = {
        name: document.querySelector('#name').value,
        username: document.querySelector('#username').value,
        email: document.querySelector('#email').value,
        pass: document.querySelector('#pass').value
    }

    fetch('/update', {
            method: "POST",
            credentials: "include",
            body: JSON.stringify(details),
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
                console.log(d.message)
                document.querySelector('#message').innerHTML = d.message;
                document.querySelector('#name').value = d.name;
                document.querySelector('#username').value = d.username;
                document.querySelector('#email').value = d.email
                document.querySelector('#pass').value = d.password;
            });
        })
}

function like(id) {
    console.log(id);
    var postid = {
        post_id: id
    }
    fetch('/liked_by', {
            method: "POST",
            credentials: "include",
            body: JSON.stringify(postid),
            cache: "no-cache",
            headers: new Headers({
                'content-type': "application/json"
            })
        })
        .then(function(response) {
            if (response.status !== 200) {
                console.log('Looks something is wrong . Status code: ${response.status}');
                return;
            }
            response.json().then(function(data) {
                d = data;
                console.log(d)
                var n = JSON.parse(d["name"]);
                if (n) {
                    var nid = "liked" + id;
                    var h = document.createElement('h4');
                    h.innerHTML = "People who liked your post";
                    document.getElementById(nid).append(h);
                    for (i in n) {
                        console.log(n[i]);
                        var h4 = document.createElement('h4');
                        h4.innerHTML = n[i];

                        document.getElementById(nid).append(h4);
                    }
                }


            })
        })
}

function deleteit(postid, userid) {
    var pid = postid;
    console.log(postid, userid)
    var del = {
        pid: postid,
        uid: userid
    }

    fetch('/delete', {
            method: "POST",
            credentials: "include",
            body: JSON.stringify(del),
            cache: "no-cache",
            headers: new Headers({
                'content-type': "applicaiton/json"
            })
        })
        .then(function(response) {
            if (response.status !== 200) {
                console.log('Looks something is wrong . Status code: ${response.status}')
                return;
            }
            response.json().then(function(data) {
                d = data;
                console.log(d);
                id = "mes" + pid;
                console.log(id);
                document.getElementById(id).innerHTML = "DELETED";
            })
        })

}