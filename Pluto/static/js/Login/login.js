'use strict'

$(document).ready(function() {

	// form validation

	let loginForm=$('form');
	let inputs=$('input')

	loginForm.submit(function(e) {

		$('.error-notif').remove();

		if(!validate()) {
			
			e.preventDefault();
		}
	})


	function validate() {

		let param=true;

		inputs.each(function() {

			let $this=$(this);

			if($this.hasClass('password')) {

				param=validatePassword($this);
			}
			else {

				if($this.val().length < 5) {

					param=false;
					$this.after('<p class="error-notif">* Enter a valid identifier</p>')
				}
			}
		})

		return param;
	}


	function validatePassword(elem) {

		if(elem.val().length < 8) {

			elem.after('<p class="error-notif">* Password must be at least 8 characters long</p>')
			return false;
		}

		return true;
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


	
	// validating the email address

	function validateEmail(email) {

		 let re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  		 return re.test(email);
	}


	// forgot password

	let fpasswordbtn=$('a.forgot-password');
	let email=$('.email');
	let loadContainer=$('.loader-container');
	let host=location.hostname;
	let protocol=location.protocol;


	fpasswordbtn.click(function() {

		$('.error-notif.mail').remove();

		if(!validateEmail(email.val())) {

			email.after('<p class="error-notif mail">* Please enter a valid email</p>');
		}
		else {

			loadContainer.toggleClass('active');
			sendPasswordResetMail();
		}
	})


	function sendPasswordResetMail() {

		return $.ajax(`${protocol}//${host}:5000/user/send_password_reset_mail`, {type:'POST', dataType:'text', data:{
			'email':email.val()
		},
		error:function() {

			toastr.error("An error occurred");
			loadContainer.toggleClass('active');
		},
		success:function(data) {

			if(data == 'error') {

				toastr.error("Invalid email!")
			}
			else {
				
				toastr.success("Check your email to complete the process");
			}

			loadContainer.toggleClass('active');
		}})
	}
}) 