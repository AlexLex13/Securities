const title = document.querySelector("#title");
const select = document.querySelector("#sel");
const submit = document.querySelector("#submit");

function load() {
    if (select.innerHTML == "") {
      fetch("/preferences/show_user_pref", {
        method: "GET",
      })
      .then((res) => res.json())
      .then((data) => {
        if (data.length === 0) {
          select.style.visibility = "hidden";
          submit.style.visibility = "hidden";
          title.innerText = "You don't have a single set.\nCreate it in your profile!";
        } else {
          data.forEach((ref) => {
            select.innerHTML += `
                <option value="${ref.name}">${ref.name}</option>`;
          });
        }
      });
    }
}