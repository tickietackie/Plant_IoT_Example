const backToMain = (e) => {
    window.location.href = "/locations";
}

window.addEventListener("load", function () {
    // Add event listener to delte table rows
    const back = document.getElementById("btn_back");
    back.addEventListener("click", backToMain, false);
})

