'use strict'

$(document).ready(function() {

	// form validation

	let signupForm=$('form');
	let eightCharInputs=$('.eightchars');
	let devInput=$('.form-control.dev');
	let email=$('.form-control.email');

	signupForm.submit(function(e) {

		$('.error-notif').remove();

		if(!validate()) {

			e.preventDefault()
		}
	})

	function validate() {

		let param=true;

		if(!validateEightChars()) {

			param=false;
		}

		if(devInput.val().length < 5) {

			devInput.after('<p class="error-notif">* Must be at least 5 characters long</p>');
			param=false;
		}

		return param;
	}


	// validating the name and password fields

	function validateEightChars() {

		let param=true;

		eightCharInputs.each(function() {

			let $this=$(this);

			if($this.val().length < 8) {

				$this.after('<p class="error-notif">* Must be at least 8 characters long</p>');
				param=false;
			}
		})

		return param;
	}


	// toggling the visibility of the password input text

	let togglePassword=$('.toggle');
	let inputPassword=$('input[type="password"]');

	inputPassword.keyup(function() {

		let $this=$(this);

		if($this.val().length > 0) {

			togglePassword.addClass('active');
		}
		else {

			togglePassword.removeClass('active');
		}
	})

	togglePassword.click(function() {

		if(inputPassword.attr('type') === 'password') {

			inputPassword.attr('type', 'text');
			togglePassword.removeClass('fa-eye').addClass('fa-eye-slash');
		}
		else {

			inputPassword.attr('type', 'password');
			togglePassword.removeClass('fa-eye-slash').addClass('fa-eye');
		}
	})
})