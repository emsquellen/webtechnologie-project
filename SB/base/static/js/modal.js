function activate_modal(modal) {
    document.getElementById(modal).classList.add("active");
}

document.querySelectorAll('a[aria-label="Close"]').forEach((el) => {
    el.addEventListener('click', () => {
        document.querySelectorAll('.modal ').forEach((modal) => {
            modal.classList.remove('active');
        })
    })
})
