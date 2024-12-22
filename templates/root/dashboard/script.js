

let T_A = document.getElementById("T_A");
function hide_A() {

    if (!T_A.classList.contains("hidden")) {
        console.log("Hidding T_A");
        T_A.classList.add("hidden");
    } else {
        T_A.classList.remove("hidden");
        console.log("Showing T_A");
    }
}