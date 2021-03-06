"use strict"

$(document).ready(function() {

	let form=$('.idea-form');
	let formElements=form.find('.elements');

	form.submit(function(e) {

		form.find('.error-notif').remove();
		if(!validate()) {

			e.preventDefault();
		}
	})


	function validate() {

		let param=true;

		formElements.each(function() {

			let $this=$(this);

			if($this.val().length < 5) {

				$this.after("<p class='error-notif m-0 mt-2'>* Must be at least 5 characters in length</p>");
				param=false;
			}
		})

		return param;
	}
})