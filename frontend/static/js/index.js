// Function to change the content of t2
function modifyText() {
    const t2 = document.getElementById("t2");
    if (t2.firstChild.nodeValue == "three") {
        t2.firstChild.nodeValue = "two";
    } else {
        t2.firstChild.nodeValue = "three";
    }
}

// Add event listener to table
const el = document.getElementsByClassName("edit");
el.addEventListener("click", modifyText, false);

const showDetails = (e) => {
    const id = this.parentNode.childNodes
    window.open("/plantDetails?id=");
}

// Add event listener to table
const el = document.getElementsByClassName("details");
el.addEventListener("click", modifyText, false);