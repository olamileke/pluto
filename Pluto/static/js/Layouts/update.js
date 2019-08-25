"use strict"

$(document).ready(function() {

	let updateForm=$('.modal form')
	let uploadbtn=updateForm.find('button.upload');
	let fileInput=updateForm.find('.file-input');
	let hiddenInput=updateForm.find('.url');
	let imageParent=$('.modal .image-parent');
	let imageTypes=['jpg','jpeg','png'];


	// setting the value of the hidden input in the update form

	hiddenInput.val(window.location.pathname);


	// previewing the selected image in the browser

	uploadbtn.click(function() {

		fileInput.click();
	})

	fileInput.change(function() {

		imageParent.removeClass('active');
		if(fileInput.prop('files').length > 0) {

			if(validateFile(fileInput.prop('files')[0])) {

				imageParent.addClass('active');
				let reader=new FileReader();

				reader.onload=function(e) {

					imageParent.find('img').attr('src', e.target.result);
				}

				reader.readAsDataURL(fileInput.prop('files')[0]);
			}
		}
	})


	function validateFile(file) {

		let types=file.type.split('/');

		if(types.length == 1) {

			toastr.error("Invalid file format");
			fileInput.val("");
			return false;
		}

		if(imageTypes.indexOf(types[1].toLowerCase()) == -1) {

			toastr.error('Invalid file format');
			fileInput.val("");
			return false;
		}

		if(file.size > 1200000) {

			toastr.error('Selected image is too large');
			fileInput.val("");
			return false;
		}

		return true;
	}


	// validation

	let elements=$('.elements');
	let inputPassword=$('input[type="password"]')

	updateForm.submit(function(e) {

		updateForm.find('.error-notif').remove();
		if(!validate()) {

			e.preventDefault();
		}
	})


	function validate() {

		let param=true;

		param=validate5Chars();

		if(inputPassword.val() != '' && inputPassword.val().length < 8) {

			inputPassword.after("<p class='error-notif mt-2'>* Must be at least 8 characters long</p>");
			imageParent.parent().removeClass('align-items-end').addClass('align-items-center')
			param=false
		}	

		return param;
	}


	function validate5Chars() {

		let param=true;

		elements.each(function() {

			let $this=$(this);

			if($this.val() != '' && $this.val().length < 5) {

				$this.after("<p class='error-notif mt-2'>* Must be at least 5 characters long</p>");
				param=false;
			}
		})

		return param;
	}
})