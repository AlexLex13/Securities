function load(name) {
    const title = document.querySelector("#title_" + name);
    const select = document.querySelector("#sel_" + name);
    const submit = document.querySelector("#submit_" + name);

    if (select.innerHTML === "") {
      fetch("/preferences/show", {
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