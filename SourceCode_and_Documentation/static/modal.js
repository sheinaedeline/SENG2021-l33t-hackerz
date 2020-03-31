
let op_but = document.getElementById("add_trans");

let modal = document.getElementById("mod");

let clo_but = document.getElementById("close");

op_but.addEventListener('click', e => {
    modal.style.display = "block";
});

clo_but.addEventListener('click', e => {
    modal.style.display = "none";
})

