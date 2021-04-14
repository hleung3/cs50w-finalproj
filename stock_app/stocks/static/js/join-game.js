function user_join(room) {
	// get data
	// run xml request 
	return new Promise(function(resolve,reject) {
    const request = new XMLHttpRequest();
    request.onload = function() {
      resolve(JSON.parse(this.responseText));
    };
    request.onerror = reject;
    request.open("POST", "user-join");
    const data = new FormData();
    data.append("room", room);
    request.send(data);
  });
}


document.addEventListener("DOMContentLoaded", () => {
	// if no openings --> grey out button
	document.querySelectorAll(".openings").forEach((el) => {
		// if no openings in el.innerhtml 
		// el.closest button is grey out

	});
	document.querySelectorAll(".join-game").forEach((el) => {
		el.onclick = (e) => {
			const room_name = e.target.dataset.room;
			user_join(room_name)
				.then(function(result) {
					console.log(result['msg'],result['quote']);
					const msg = document.querySelector("#msg");
					msg.innerHTML =  result['msg'];
					// if user in room - button becomes go to page link
					const room = document.getElementById(result['room']);
					// get nearest button
					if (result['quote']) {
						console.log("enable button");
						const goto = document.querySelector("#goto-"+result['room']);
						goto.classList.remove("disabled");
						console.log("removed")
					}
					// turn button to link to page
				});			 
		};
	});
});