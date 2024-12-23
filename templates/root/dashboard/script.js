
/*
T_A -> PANEL WHILE PLAYER ON BIDDING
T_B -> STARTING OF THE AUCTION
*/



let T_A = document.getElementById("T_A");
let T_B = document.getElementById("T_B");
let T_C = document.getElementById("T_C");

async function pause(sec) {
    await new Promise((res)=> setTimeout(res,sec*1000))    
}
async function hide_A() {

    if (!T_A.classList.contains("hidden")) {
        console.log("Hidding T_A");
        T_A.classList.add("animate__zoomOutDown")
        await pause(1)
        T_A.classList.add("hidden");
    } else {
        T_A.classList.remove("animate__zoomOutDown")
        T_A.classList.remove("hidden");
        console.log("Showing T_A");
    }
}

async function hide_B() {

    if (!T_B.classList.contains("hidden")) {
        console.log("Hidding T_B");
        T_B.classList.add("animate__flipOutY")
        await pause(1)
        T_B.classList.add("hidden");
    } else {
        T_B.classList.remove("animate__flipOutY")
        T_B.classList.remove("hidden");
        console.log("Showing T_B");
    }
}

async function hide_C() {

    if (!T_C.classList.contains("hidden")) {
        console.log("Hidding T_C");
        T_C.classList.add("animate__zoomOutRight")
        await pause(1)
        T_C.classList.add("hidden");
    } else {
        T_C.classList.remove("animate__zoomOutRight")
        T_C.classList.remove("hidden");
        console.log("Showing T_C");
    }
}