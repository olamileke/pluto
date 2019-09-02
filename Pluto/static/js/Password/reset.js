"use strict"

$(document).ready(function() {

	let form=$('form');
	let password=form.find('.form-control');

	form.submit(function(e) {

		if(!validate()) {

			e.preventDefault()
		}
	})


	function validate() {

		let param=true;

		if(password.val().length < 8) {

			password.after("<p class='error-notif mt-2'>* Must be at least 8 characters long</p>");
			return false;
		}

		return param;
	}
})