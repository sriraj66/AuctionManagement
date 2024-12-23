export function showPopup(message) {
    const popup = document.createElement('div');
    popup.className = 'popup';
    popup.textContent = message;
    
    document.body.appendChild(popup);
    
    // Remove popup after 3 seconds
    setTimeout(() => {
        popup.classList.add('fade-out');
        setTimeout(() => popup.remove(), 300);
    }, 3000);
}