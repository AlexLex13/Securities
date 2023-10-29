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
    fetch("/bonds/search_bonds", {
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
          data.forEach((bond) => {
            tbody.innerHTML += `
                <tr>
                <td>${bond.name}</td>
                <td>${bond.maturity_years}</td>
                <td>${bond.profitability}</td>
                <td>${bond.coupon_yield}</td>
                <td>${bond.coupon_yield_last}</td>
                <td>${bond.rating}</td>
                <td>${bond.volume}</td>
                <td>${bond.coupon}</td>
                <td>${bond.coupon_payments_frequency}</td>
                <td>${bond.accumulated_income}</td>
                <td>${bond.duration}</td>
                <td>${bond.price}</td>
                <td>${bond.next_coupon_date}</td>
                <td>${bond.issue_date}</td>
                <td>${bond.maturity_date}</td>
                <td>${bond.offer_date}</td>
                <td>${bond.company_id}</td>
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
