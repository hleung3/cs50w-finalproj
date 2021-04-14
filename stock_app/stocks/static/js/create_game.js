function createNewGame(data) {
  return new Promise(function(resolve,reject) {
    const request = new XMLHttpRequest();
    request.onload = function() {
      resolve(JSON.parse(this.responseText));
    };
    request.onerror = reject;
    request.open("POST", "create-newgame");
    request.send(data);
  });
}

document.addEventListener("DOMContentLoaded", () => {
	let game_form = document.querySelector("#game-form");
	game_form.onsubmit = (e) => {
		e.preventDefault();
		let data = new FormData(game_form);
		const msg = document.querySelector("#msg");
		msg.innerHTML = "";
		if (data.get('room-name').length > 50) {
			msg.innerHTML = "name can only have up to 50 char";
		}
		if (parseInt(data.get('room-players'),10) > 50) {
			msg.innerHTML += "<br> rooms can only have up to 50 players";
		}
		if (parseInt(data.get('room-value'),10) < 1000) {
			msg.innerHTML += "<br> starting value must be greater than 1000 dollars"
		}
		if (msg.innerHTML != "") {
			return false;
		}
		createNewGame(data)
			.then(function(result) {
				// print to msg h1
				console.log(result['quote'],result['message']);
				if (result['quote'] == true) {
					// if false
					msg.innerHTML = result['name'] + " created.";	
				}
				else {
					msg.innerHTML = result['message'];
				}
			});	
	};
})