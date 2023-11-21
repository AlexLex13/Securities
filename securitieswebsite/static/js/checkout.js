const bondsTable = document.querySelector("#bonds_table");
const sharesTable = document.querySelector("#shares_table");

function show_bonds() {
    bondsTable.style.display = "block";
    sharesTable.style.display = "none";
}

function show_shares() {
    bondsTable.style.display = "none";
    sharesTable.style.display = "block";
}