const is_import = document.querySelector("#import");
const file_div = document.querySelector("#file");
const file_input = document.querySelector('[name="file"]');


is_import.addEventListener("click", () => {
    if (is_import.checked) {
        file_div.style.display = "block";
        file_input.required = true;
    } else {
        file_div.style.display = "none";
        file_input.required = false;
    }
});