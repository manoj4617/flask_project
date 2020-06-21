function like_it(r) {
    //console.log(r);
    var likes = {

        like_rev: r
    };
    console.log(likes)
    fetch('/post_like', {
            method: "POST",
            Credentials: "include",
            body: JSON.stringify(likes),
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
                //console.log("ID " + data.postid);
                //console.log("Likes " + data.likes);
                document.getElementById("post" + r).innerHTML = data.likes;

            });
        })
        .catch(function(error) {
            console.log("Fetch error: " + error);
        });
}