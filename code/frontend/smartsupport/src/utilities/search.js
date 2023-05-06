import config from "@/config.js";


async function search_tickets(search_string, object) {
    object.show_search_spinner = true
    if (search_string.length > 3) {
        object.openOffcanvas()
        fetch(`${config.BASE_API_URL}/tickets/search?q=${search_string}`, {
            headers: { Authorization: localStorage.getItem("access_key") },
        })
            .then((res) => res.json())
            .then((res) => {
                object.searched_ticket_list = res
                console.log("got searched ticket list")
                console.log(object.searched_ticket_list)
                object.show_search_spinner = false
            });
    } else{
        object.closeOffcanvas()
    }
}

export {search_tickets}