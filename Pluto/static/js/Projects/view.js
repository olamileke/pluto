"use strict"

$(document).ready(function() {

	let host=location.hostname;
	let protocol=location.protocol;
	let id=location.pathname.slice(10,11);
	let taskForm=$('.task-form');
	let taskBtn=taskForm.find('button');
	let taskInput=taskForm.find('input');
	let months=['January', 'February', 'March', 'April', 'May','June', 'July', 'August', 'September', 'October', 'November', 'December'];
	let taskcontainer=$('.task-container');

	taskBtn.click(function() {

		$('.error-notif').remove();

		if(validate()) {

			$(this).find('div').removeClass('d-none').addClass('d-block').prop('disabled', 'disabled');
			addTask();
		}
	})


	function addTask() {

	return 	$.ajax(`${protocol}//${host}:5000/tasks/add`, {
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
						taskcontainer.append(newTaskText(taskInput.val()));
						taskInput.val("");
						$('#newTaskModal').modal('hide');
					}
					else {

						toastr.error('Problem adding new task');
					}
				}
			})
	}


	function validate() {

		if(taskInput.val().length < 5) {

			taskInput.after("<p class='mt-2 mb-0 error-notif'>* Must be at least 5 characters</p>");
			return false;
		}

		return true;
	}


	function newTaskText(task) {

		return `<div class='custom-control custom-checkbox mx-5 mx-sm-0 mb-3 col-sm-6 p-0 pl-1 d-flex flex-column'>
						 <div class="custom-control custom-checkbox my-1 mr-sm-2">
							<input type="checkbox" class='custom-control-input' id="${task}">
							<label class="custom-control-label" for="${task}">${task}</label>
						</div>
						<p class='m-0 ml-4 small text-muted'>Created ${getTime()}</p>
					</div>`	
	}


	function getTime() {

		let date=new Date();

		return `${months[date.getMonth()]} ${ date.getDate()}, ${date.getFullYear()} ${date.getHours()}:${date.getMinutes()}`;
	}


	// setting the loader initially when the page loads

	let totalTasks = $('.tasks-count').text();
	let numCompletedTasks = $('.completed-tasks-count').text();
	let loadBar = $('.loaded');

	function setLoader(totalTasks, completedTasks) {

		let percent=(completedTasks/totalTasks) * 100;
		loadBar.css({ width: percent });
	}

	setLoader(totalTasks, numCompletedTasks);


	// getting the checked tasks

	let tasksStatus={};
	let altTaskStatus={};
	let tasks=$('input[type="checkbox"]');

	function getTaskStatus() {

		tasksStatus={};
		tasks.each(function() {

			let id=$(this).next().text();
			if($(this).hasClass('checked')) {

				tasksStatus[id]=1;
			}
			else {

				tasksStatus[id]=0;
			}
		})

		checkTaskStatus(tasksStatus);
		alert(JSON.stringify(tasksStatus));
	}


	function checkTaskStatus(tasksObject) {

		if(tasks)
	}

	getTaskStatus();


	tasks.click(function() {

		if($(this).hasClass('checked')) {

			$(this).removeClass('checked');
		}
		else {

			$(this).addClass('checked');
		}


		getTaskStatus();
	})

})
