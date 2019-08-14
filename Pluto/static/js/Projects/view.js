"use strict"

$(document).ready(function() {

	let host=location.hostname;
	let protocol=location.protocol;
	let id=location.pathname.slice(10,11);
	let taskForm=$('.task-form');
	let taskBtn=taskForm.find('button');
	let taskInput=taskForm.find('input');


	taskBtn.click(function() {

		$('.error-notif').remove();

		if(validate()) {

			$(this).find('div').removeClass('d-none').addClass('d-block').prop('disabled', 'disabled');

			$.ajax(`${protocol}//${host}:5000/tasks/add`, {
				type:'POST',
				dataType:'text',
				data:{
					'task':taskInput.val(),
					'project_id':id
				},
				error:function(data) {

					toastr.error('Problem adding new task');
				},
				success:function(data) {

					if(data == 'success') {

						$(this).find('div').removeClass('d-block').addClass('d-none');
						toastr.success('New Task Added');
						taskInput.val("");
						$('#newTaskModal').modal('hide');
					}
					else {

						toastr.error('Problem adding new task');
					}
				}
			})
		}
	})


	function validate() {

		if(taskInput.val().length < 5) {

			taskInput.after("<p class='mt-2 mb-0 error-notif'>* Must be at least 5 characters</p>");
			return false;
		}

		return true;
	}
})
