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
	let completebtn=$('a.complete');

	taskBtn.click(function() {

		$('.error-notif').remove();

		if(validate()) {

			$(this).find('div').removeClass('d-none').addClass('d-block').prop('disabled', 'disabled');
			addTask();
		}
	})


	taskForm.submit(function(e) {

		e.preventDefault();
	})


	function addTask() {

	return 	$.ajax(`${protocol}//${host}:5000/tasks/add`, {type:'POST',dataType:'text',data:{'task':taskInput.val(),
				'project_id':id
				},
				error:function(data) {
					toastr.error('Problem adding new task');
				},
				success:function(data) {
					if(data != 'error') {

						$(this).find('div').removeClass('d-block').addClass('d-none');
						toastr.success('New Task Added');
						taskcontainer.append(newTaskText(taskInput.val(), data));
						taskInput.val("");
						$('#newTaskModal').modal('hide');
						tasks=$('input[type="checkbox"]');
						taskIDs=$('.task-id'); 
						tasks.off();
						taskClick();
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


	function newTaskText(task, id) {

		initialTasksStatus[id]=0;
		tasksStatus[id]=0;

		return `<div class='custom-control custom-checkbox col-sm-6 mb-1 p-0 d-flex align-items-center align-items-sm-start flex-column mr-1 mr-sm-0 checkbox-parent'>
						 <div class="custom-control custom-checkbox my-1 mr-sm-2">
							<input type="checkbox" class='custom-control-input' id="${task}">
							<span class='task-id' hidden>${id}</span>
							<label class="custom-control-label" for="${task}">${task}</label>
						</div>
						<p class='m-0 ml-4 small text-muted'>Created ${getTime()}</p>
					</div>`	
	}


	function getTime() {

		let date=new Date();

		let minutes=String(date.getMinutes());

		if(String(date.getMinutes()).length == 1) {

			minutes='0'+String(date.getMinutes());
		}

		return `${months[date.getMonth()]} ${ date.getDate()}, ${date.getFullYear()} ${date.getHours()}:${minutes}`;
	}


	// setting the loader initially when the page loads

	let loadBar = $('.loaded');

	function setLoader() {

		let totalTasks=$(".checkbox-parent").length
		let completedTasks=$('.checked').length

		let percent=(completedTasks/totalTasks) * 100;

		if(percent > 0) {

			loadBar.css({ width: percent+'%' , border:'1px solid #29AB87'});
		}
		else if(percent == 0) {

			loadBar.css({ width: percent+'%', border:'0px solid transparent'});
		}
	}

	setLoader(); 

	let tasksStatus={};
	let initialTasksStatus={};
	let updatedTasks={};
	var tasks=$('input[type="checkbox"]');
	var taskIDs=$('.task-id'); 
	let updatebtn=$('button.update-project');

	function getTaskStatus(param=false) {

		tasksStatus={};
		tasks.each(function() {

			let id=$(this).parent().find('.task-id').text();
			if($(this).hasClass('checked')) {

				tasksStatus[id]=1;
			}
			else {

				tasksStatus[id]=0;
			}
		})

		if(param) {

			initialTasksStatus=tasksStatus
		}	
	}


	function checkTaskStatus() {

		let keys=Object.keys(initialTasksStatus);
		updatedTasks={};
		let count=0;

		for(let i=0; i < keys.length; i++) {

			if(initialTasksStatus[keys[i]] != tasksStatus[keys[i]]) {

				updatedTasks[keys[i]]=tasksStatus[keys[i]]
				count++;
			}
		}

		if(count > 0) {

			updatebtn.addClass('d-flex');
			return false;
		}

		updatebtn.removeClass('d-flex');
		return true;
	}


	// getting the checked tasks

	getTaskStatus(true);


	function taskClick() {

		tasks.click(function() {

			const statuses=tasksStatus;

			if($(this).hasClass('checked')) {

				$(this).removeClass('checked');
			}
			else {

				$(this).addClass('checked');
			}

			getTaskStatus();
			checkTaskStatus();
		})

	}

	if(!completebtn.hasClass('completed')) {

		taskClick();
	}

	// updating the tasks

	updatebtn.click(function() {

		$(this).addClass('active');
		$(this).find('p').hide()
		$(this).find('div').show();
		updateTasks($(this));		
	})


	function updateTasks(button) {

		return 	$.ajax(`${protocol}//${host}:5000/tasks/update`, {type:'POST',dataType:'text',data:{'tasks':JSON.stringify(updatedTasks)},
			success:function(data) { 
				initialTasksStatus=tasksStatus;
				setLoader();
				toastr.success('Tasks updated!');
				resetButton(button);
				updateTaskDetails()
			},
			error:function(data) {
				toastr.error('There was a problem updating tasks');
			},
		})
		
	}


	// setting the completed at details for just updated tasks

	function updateTaskDetails() {

		let updatedIDs=Object.keys(updatedTasks);

		taskIDs.each(function() {

			let $this=$(this);

			if(updatedIDs.indexOf($this.text()) != -1) {

				let parent=$(this).parent().parent();

				if(updatedTasks[$this.text()]) {

					parent.find('.completed-at').css('visibility','visible').text('Completed ' + getTime());
				}
				else {
					parent.find('.completed-at').css('visibility','hidden');
				}
			}
		})
	}


	function resetButton(button) {

		button.removeClass('active').removeClass('d-flex');
		button.find('p').show();
		button.find('div').hide();
	}


	// deleting a project

	let deletebtn=$('a.delete');

	deletebtn.click(function(e) {

		let param=confirm('Are you sure you want to delete ?')

		if(!param) {

			e.preventDefault();
		}
	})


	// toggling the completed state of a project

	completebtn.click(function(e) {

		if($(this).hasClass('completed')) {
			
			let param=confirm('Work on Project ?');
		}
		else {

			let param=confirm('Complete Project ?');
		}


		if(!param) {

			e.preventDefault();
		}
	})
})
