// Function to change the content of t2
function editRow() {
    window.alert("Not yet implemented.")
}

//delete row
function deleteRow() {
    window.alert("Not yet implemented.")
}

//show details page
const showDetails = (e) => {
    const id = e.target.parentNode.parentNode.childNodes[3].innerHTML
    if (!isNaN(id)) {
        window.location.href = "/location/area/sensor_data?area_id=" + id;
    } else {
        window.alert("Failed to get id.")
    }
}

window.addEventListener("load", function () {
    // Add event listener to delte table rows
    const deleteButtons = document.getElementsByClassName("btn_delete");
    for (let index = 0; index < deleteButtons.length; index++) {
        const element = deleteButtons[index];
        element.addEventListener("click", deleteRow, false);
    }
    // Add event listener to table
    const detailsButton = document.getElementsByClassName("btn_details");
    for (let index = 0; index < detailsButton.length; index++) {
        const element = detailsButton[index];
        element.addEventListener("click", showDetails, false);
    }

    // Add event listener to edit table row
    const editButtons = document.getElementsByClassName("btn_edit");
    for (let index = 0; index < editButtons.length; index++) {
        const element = editButtons[index];
        element.addEventListener("click", editRow, false);
    }
})

