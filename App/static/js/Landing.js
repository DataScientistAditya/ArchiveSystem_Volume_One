function openNav() {
    var open = document.getElementById("Sidebarid");
    var openanavbutton = document.getElementById("Opennavid");
    open.style.width = "40%";
    openanavbutton.style.display = "none";
}

/* Set the width of the sidebar to 0 and the left margin of the page content to 0 */
function closeNav() {
    document.getElementById("Sidebarid").style.width = "0";
    document.getElementById("Opennavid").style.display = "block"
}