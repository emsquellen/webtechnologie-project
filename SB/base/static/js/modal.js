function activate_modal(modal) {
    document.getElementById(modal).classList.add("active");
}

// After DOM is loaded
// function () { is the same thing as () => {
// Just some aesthethic y'know 
window.onload = () => {
    document.querySelectorAll('a[aria-label="Close"]').forEach(el => {
        el.addEventListener('click', () => {
            document.querySelectorAll('.modal').forEach(modal => {
                modal.classList.remove('active');
            })
        })
    })
}