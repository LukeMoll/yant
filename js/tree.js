async function get_tree() {
    // let api_path = window.location.pathname
    //     .replace(/^\/notes/, "/api/tree")
    //     .replace(/\/[a-z]+$/,"/");
    // let req = new Request(api_path);
    let req = new Request("/api/tree");
    let res = await fetch(req);
    return res.json();
}

function make_tree(tree, path="/") {
    let ul = document.createElement("ul");
    for(f of tree) {
        let current = document.createElement("li");
        if(f.hasOwnProperty("contents")) {
            current.innerHTML = f.path;
            current.appendChild(make_tree(f.contents, path + f.path + "/"));
        }
        else {
            let a = document.createElement("a");
            a.textContent = f.replace(/\.md$/,"");
            a.href = `/notes${path}${a.textContent}`;
            current.appendChild(a);
        }
        ul.appendChild(current);
    }
    return ul;
}

function render_tree(id) {
    let parent = document.getElementById(id);
    get_tree()
        .then(tree => make_tree(tree))
        .then(ul => parent.appendChild(ul));
}