function toggle(source) {
  checkboxes = document.getElementsByName('stock');
  for(var i=0, n=checkboxes.length;i<n;i++) {
    checkboxes[i].checked = source.checked;
  }
}
function remove_all(source,userid) {
	checkboxes = document.getElementsByName('stock');
	select_all = document.getElementById('checkAll');
	for(var i = 0, n=checkboxes.length; i<n; i++) {
		// parent row
		if (checkboxes[i].checked) {
			tr = checkboxes[i].closest("tr");
			ticker = tr.id;
			remove_saved(userid,ticker);
			// remove row animation
			const tbody = tr.closest("tbody");
			const table = tbody.closest("table");
			const header = table.previousElementSibling;
			tr.style.animationPlayState = 'running';
			tr.addEventListener('animationend', () =>  {
				tr.remove();
			    // Remove table and h3 if needed
			    if (tbody.childElementCount == 0) {
			      table.remove();
			      header.remove();
			    }
			});
		}
	}
	if (select_all.checked) {
		select_all.checked = !(select_all.checked);
	}
}

function remove_saved(userid,ticker) {
	return new Promise(function(resolve,reject) {
    const request = new XMLHttpRequest();
    request.onload = function() {
      resolve(JSON.parse(this.responseText));
    };
    request.onerror = reject;
    request.open("POST", "remove-saved");
    const data = new FormData();
    data.append("userid", userid);
    data.append("ticker", ticker);
    request.send(data);
  });
}

document.addEventListener("DOMContentLoaded", () => {
	document.querySelectorAll(".remove-item").forEach((el) => {
		el.onclick = (e) => {
			console.log("remove_saved")
			const userid = e.target.dataset.userid;
			const ticker = e.target.dataset.ticker;
			remove_saved(userid,ticker)
				.then(function(result) {
					// take result and remove table row from html page
					if (result["user"] != userid ) {
						console.log("false")
						return false
					}
					const tr = e.target.closest("tr");
					
					// need animation to remove 

					const tbody = tr.closest("tbody");
					const table = tbody.closest("table");
					const header = table.previousElementSibling;
					tr.style.animationPlayState = 'running';
					tr.addEventListener('animationend', () =>  {
						tr.remove();
					    // Remove table and h3 if needed
					    if (tbody.childElementCount == 0) {
					      table.remove();
					      header.remove();
					    }
					});
					// then update the html table with animation 
			});
		};
	});
});