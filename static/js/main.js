function login(e) {
    e.preventDefault();
    $.ajax({
        url: '/auth/login',
        method: "POST",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({
            email: this.email.value,
            password: this.password.value
        }),
        success: function (data) {
            localStorage.setItem(
                "access_token", data.access_token
            );
            localStorage.setItem(
                "refresh_token", data.refresh_token
            );
            localStorage.setItem(
                "token_type", data.token_type
            );
            document.location.replace("/")
        },
        error: function (data) {
            if (data.responseJSON.detail === "user not found") {
                let loginForm = document.getElementById("loginForm")
                let emailLabel = document.getElementById("emailLabel")
                emailLabel.innerHTML = "User Not Found";
                loginForm.email.className = "form-control border-warning"
            }
        }
    })
}

function refreshToken(callback) {
    axios.post(
        "/auth/refresh",
        {
            refresh_token: localStorage.getItem("refresh_token")
        }
    )
        .then(function (response) {
            localStorage.setItem(
                "access_token", response.data.access_token
            );
            localStorage.setItem(
                "refresh_token", response.data.refresh_token
            );
            localStorage.setItem(
                "token_type", response.data.token_type
            );
            callback()
        })
        .catch(function (response) {
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
            localStorage.removeItem("token_type");
            document.location.replace("/login");
        })
    // let response = fetch(
    //     "/auth/refresh",
    //     {
    //         method: "post",
    //         headers: {
    //             "Content-Type": "application/json",
    //         },
    //         body: JSON.stringify({refresh_token: localStorage.getItem("refresh_token")}),
    //     }
    // )
    // response.then(function (response) {
    //     console.log(response)
    //     if (response.ok) {
    //         response.json().then(function (data) {
    //             localStorage.setItem(
    //                 "access_token", data.access_token
    //             );
    //             localStorage.setItem(
    //                 "refresh_token", data.refresh_token
    //             );
    //             localStorage.setItem(
    //                 "token_type", data.token_type
    //             );
    //         })
    //         callback()
    //     } else {
    //         localStorage.removeItem("access_token");
    //         localStorage.removeItem("refresh_token");
    //         localStorage.removeItem("token_type");
    //         document.location.replace("/login");
    //     }
    // })

    // $.ajax({
    //     url: "/auth/refresh",
    //     method: "POST",
    //     dataType: "json",
    //     contentType: "application/json",
    //     data: JSON.stringify({refresh_token: localStorage.getItem("refresh_token")}),
    //     error: function (data) {
    //         localStorage.removeItem("access_token");
    //         localStorage.removeItem("refresh_token");
    //         localStorage.removeItem("token_type");
    //         document.location.replace("/login");
    //     },
    //     success: function (data) {
    //         localStorage.setItem(
    //             "access_token", data.access_token
    //         );
    //         localStorage.setItem(
    //             "refresh_token", data.refresh_token
    //         );
    //         localStorage.setItem(
    //             "token_type", data.token_type
    //         );
    //         callback();
    //     }
    // })
}


function loadFinanceList() {
    $.ajax({
        url: "/api/v1/finance",
        method: "GET",
        dataType: "json",
        headers: {
            Authorization: `${localStorage.getItem("token_type")} ${localStorage.getItem("access_token")}`
        },
        success: function (data) {
            let financeList = document.getElementById("financeList");
            financeList.innerHTML = ""
            data.map(function (item, index, array) {
                financeList.innerHTML += `<tr>
                          <td>
                            ${item.amount}
                          </td>
                          <td>
                            ${item.type}
                          </td>
                          <td>
                            ${item.date_created}
                          </td>
                        </tr>`
            })
        },
        error: function (data) {
            refreshToken(loadFinanceList)
        }
    })
}

function loadExpenseTypes() {
    $.ajax({
        method: "GET",
        url: "/api/v1/expense_types",
        dataType: "json",
        success: function (data) {
            let expenseTypeSelect = document.getElementById("expenseType");
            expenseTypeSelect.innerHTML = ""
            data.map(function (item, index, array) {
                expenseTypeSelect.innerHTML += `<option value="${item}">${item}</option>`
            })
        }
    })
}

$(document).ready(function () {
    let accessToken = localStorage.getItem("access_token");
    let tokenType = localStorage.getItem("token_type");
    console.log(accessToken, tokenType)

    if ((accessToken === null || tokenType == null) && document.location.pathname !== "/login") {
        document.location.replace("/login")
    } else if (document.location.pathname !== "/login") {
        loadFinanceList();
        loadExpenseTypes();
        refreshToken(function (){})
    }
})

$("#loginForm").on("submit", login)

function createFinance(e) {
    e.preventDefault();
    $.ajax({
        url: "/api/v1/finance",
        method: "POST",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({
            amount: this.amount.value,
            type: this.expenseType.value
        }),
        headers: {
            Authorization: `${localStorage.getItem("token_type")} ${localStorage.getItem("access_token")}`
        },
        success: function (data) {
            let financeList = document.getElementById("financeList");
            financeList.innerHTML = `<tr>
                          <td>
                            ${data.amount}
                          </td>
                          <td>
                            ${data.type}
                          </td>
                          <td>
                            ${data.date_created}
                          </td>
                        </tr>` + financeList.innerHTML
        },
        error: function (data) {
            refreshToken(createFinance)
        }
    })
}

$("#createFinance").on("submit", createFinance)
