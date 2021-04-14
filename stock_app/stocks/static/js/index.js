function getQuote(data) {
  return new Promise(function(resolve, reject) {
    const request = new XMLHttpRequest();
    request.onload = function() {
      console.log(this.responseText);
      resolve(JSON.parse(this.responseText));
    };
    request.onerror = reject;
    request.open("POST", "get-quote");
    request.send(data);
  });
}

function addPortfolio(data) {
  return new Promise(function(resolve,reject) {
    const request = new XMLHttpRequest();
    request.onload = function() {
      resolve(JSON.parse(this.responseText));
    };
    request.onerror = reject;
    request.open("POST", "add-portfolio");
    request.send(data);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  // adding behaviour for order buttons
  let ticker_form = document.querySelector("#ticker-form");
  var formdata = new FormData();
  ticker_form.onsubmit = (e) => {
    e.preventDefault();
    let data = new FormData(ticker_form);
    // alert(data);
    if (data.get('ticker').length > 6) {
      return false;
    }
    getQuote(data)
      .then(function(result) {
        // delete old text if exist
        var h1 = document.getElementById("msg")
        var ul = document.getElementById("info-list")
        h1.innerHTML = "";
        ul.innerHTML = '';

        // check if quote field is true or false
        if (result["quote"] == false) {
          h1.innerHTML = result["message"]
          return false
        }

        // for key in reponse - add to list
        for (var key in result) {
          if (!(['quantity'].includes(key))) {
            formdata.append(key,result[key])
          } 
          var li = document.createElement("li");
          li.innerHTML = `${key} : ${result[key]}`;
          li.className = "list-group-item"
          ul.appendChild(li);
        }
        const stock_info = document.querySelector("#stock-info");
      });
  }
  let add_portfolio = document.querySelector("#add-portfolio");
  add_portfolio.onclick = (e) => {
    if (!(formdata == "")) {
      let data = formdata;
      addPortfolio(data)
        .then(function(result) {
          var h1 = document.getElementById("msg")
          var ul = document.getElementById("info-list")
          ul.innerHTML = '';

          if (result["quote"] == false) {
            h1.innerHTML = result["message"]
            return false
          }
        })
    }
  }

  
});