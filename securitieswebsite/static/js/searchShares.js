const searchField = document.querySelector("#searchField");

const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
tableOutput.style.display = "none";
const noResults = document.querySelector(".no-results");
const tbody = document.querySelector(".table-body");

searchField.addEventListener("keyup", (e) => {
  const searchValue = e.target.value;

  if (searchValue.trim().length > 0) {
    paginationContainer.style.display = "none";
    tbody.innerHTML = "";
    fetch("/shares/search_shares", {
      body: JSON.stringify({ searchText: searchValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        appTable.style.display = "none";
        tableOutput.style.display = "block";

        if (data.length === 0) {
          noResults.style.display = "block";
          tableOutput.style.display = "none";
        } else {
          noResults.style.display = "none";
          data.forEach((share) => {
            tbody.innerHTML += `
                <tr>
                <td>${share.name}</td>
                <td>${share.ticker}</td>
                <td>${share.last_price}</td>
                <td>${share.price_change}</td>
                <td>${share.volume}</td>
                <td>${share.last_transaction_time}</td>
                <td>${share.weekly_price_change}</td>
                <td>${share.monthly_price_change}</td>
                <td>${share.annual_price_change}</td>
                <td>${share.capitalization}</td>
                <td>${share.volume_change}</td>
                <td>${share.company_id}</td>
                </tr>`;
          });
        }
      });
  } else {
    tableOutput.style.display = "none";
    appTable.style.display = "block";
    paginationContainer.style.display = "block";
  }
});
