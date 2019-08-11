"use strict"

$(document).ready(function() {


	// Image Preview Logic

	let uploadbtn=$('button.upload');
	let fileInput=$('#fileInput');
	let imgParent=$('.image-parent');
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

		let type=file.type.split('/')[1];

		if(imageTypes.indexOf(type) == -1) {

			toastr.error('File format is not accepted');
			return false;
		}

		if(file.size > 1200000) {

			toastr.error('Selected image is too large');
			return false;
		}

		return true;
	}


	// validation logic

	let form=$('form');
	let elements=$('.elements');
	let imgContainer=$('.img-container');

	form.submit(function(e) {

		$('.error-notif').remove();
		if(!validate()) {

			e.preventDefault();
		}
	})


	function validate() {

		let param=true;

		param=validateInputs();

		if(fileInput.prop('files').length == 0) {

			imgContainer.after("<p class='error-notif m-0 mt-2'>* Image is required</p>");
			param=false;
		}

		return param;
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