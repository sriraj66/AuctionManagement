// Panels
let T_A = document.getElementById("T_A");
let T_B = document.getElementById("T_B");
let T_C = document.getElementById("T_C");
let T_D = document.getElementById("T_D");

let visiblePanel = null;

async function pause(sec) {
    await new Promise((res) => setTimeout(res, sec * 1000));
}

async function hidePanel(panel, animation) {
    if (!panel.classList.contains("hidden")) {
        console.log(`Hiding ${panel.id}`);
        panel.classList.add(animation);
        await pause(1); // Wait for animation to complete
        panel.classList.add("hidden");
        panel.classList.remove(animation);
        visiblePanel = null;
    }
}

async function showPanel(panel) {
    console.log(`Showing ${panel.id}`);
    panel.classList.remove("hidden");
    visiblePanel = panel;
}

async function hide_A() {
    if (visiblePanel && visiblePanel !== T_A) {
        await hidePanel(visiblePanel, visiblePanel.animation);
    }
    if (T_A.classList.contains("hidden")) {
        await showPanel(T_A);
    } else {
        await hidePanel(T_A, "animate__zoomOutDown");
    }
}

async function hide_B() {
    if (visiblePanel && visiblePanel !== T_B) {
        await hidePanel(visiblePanel, visiblePanel.animation);
    }
    if (T_B.classList.contains("hidden")) {
        await showPanel(T_B);
    } else {
        await hidePanel(T_B, "animate__flipOutY");
    }
}

async function hide_C() {
    if (visiblePanel && visiblePanel !== T_C) {
        await hidePanel(visiblePanel, visiblePanel.animation);
    }
    if (T_C.classList.contains("hidden")) {
        await showPanel(T_C);
    } else {
        await hidePanel(T_C, "animate__zoomOutRight");
    }
}

async function hide_D() {
    if (visiblePanel && visiblePanel !== T_D) {
        await hidePanel(visiblePanel, visiblePanel.animation);
    }
    if (T_D.classList.contains("hidden")) {
        await showPanel(T_D);
    } else {
        await hidePanel(T_D, "animate__zoomOutLeft");
    }
}


T_A.animation = "animate__zoomOutDown";
T_B.animation = "animate__flipOutY";
T_C.animation = "animate__zoomOutRight";
T_D.animation = "animate__zoomOutLeft";
