"use strict"

$(document).ready(function() {


	// Image Preview Logic

	let form=$('.edit-form');
	let uploadbtn=form.find('button.upload');
	let fileInput=form.find('#fileInput');
	let imgParent=form.find('.image-parent');
	let imageTypes=['jpg','jpeg','png','JPEG','PNG','JPG'];

	uploadbtn.click(function() {

		fileInput.click();
	})


	fileInput.change(function() {

		imgParent.removeClass('active');
		previewImage();
	})


	function previewImage() {

		if(fileInput.prop('files').length > 0) {

			if(validateFile(fileInput.prop('files')[0])) {

				imgParent.addClass('active');
				let reader=new FileReader();

				reader.onload= function(e) {

					imgParent.find('.project-img').attr('src', e.target.result);
				}

				reader.readAsDataURL(fileInput.prop('files')[0]);
			}
		}
	}


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


	// validation logic

	let elements=form.find('.elements');
	let imgContainer=$('.img-container');

	form.submit(function(e) {

		form.find('.error-notif').remove();
		if(!validate()) {

			e.preventDefault();
		}
	})


	function validate() {

		return validateInputs();
	}


	function validateInputs() {

		let param=true;

		elements.each(function() {

			let $this=$(this);

			if($this.val().length < 5) {

				param=false;
				$this.after("<p class='error-notif m-0 mt-2'>* Must be at least 5 characters in length</p>");
			}
		})

		return param;
	}
})