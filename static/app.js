// Handle when a user clicks the star icon on articles
$(".fa-star").click(async function(evt){
    const url = $(evt.target).siblings("a")[0].href
    const name = $(evt.target).siblings("a").text()
    
    const resp = await axios.post("http://127.0.0.1:5000/article/save", {
        "url": url,
        "name": name
    })
    
    if (resp.data !== "fail") {
        $(evt.target).toggleClass("far fas")
    }
})

// Handle when a user clicks the trash can icon on their favorited articles
$(".fa-trash-alt").click(async function(evt){
    const url = $(evt.target).siblings("a")[0].href
    
    const resp = await axios.post("http://127.0.0.1:5000/article/delete", {
        "url": url,
    })

    if (resp.data === "success") {
        window.location.reload()
    }
})
