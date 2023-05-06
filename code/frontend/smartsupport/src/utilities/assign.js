import config from "@/config.js";


function assign_ticket_to_user(username, object) {
    console.log(object.ticket_id_to_assign, username)
    let assignment_data = {
        ticket_id: object.ticket_id_to_assign,
        username: username
    }

    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Authorization: localStorage.getItem("access_key"),
        },
        body: JSON.stringify(assignment_data)
    };

    fetch(`${config.BASE_API_URL}/tickets/assign`, options)
        .then(response => response.json())
        .then(
            swal({
                title: "Success",
                text: "Ticket with ticket_id - " + object.ticket_id_to_assign + " assigned to user - " + username + " successfully via Email.",
                icon: "success",
                button: "Okay"
            }))
        .catch(err => console.error(err));
}

function get_admin_and_support_user(ticket_id, object) {
    object.ticket_id_to_assign = ticket_id
    console.log(object.ticket_id_to_assign)
    console.log('gettng users')
    const options = {
        method: 'GET',
        headers: {
            Authorization: localStorage.getItem("access_key")

        }
    };

    fetch(`${config.BASE_API_URL}/user/admin-and-support`, options)
        .then(response => response.json())
        .then(response => object.admin_and_support_user_list = response)
        .then(response => console.log(object.admin_and_support_user_list))
        .catch(err => console.error(err));
}

export {assign_ticket_to_user, get_admin_and_support_user}