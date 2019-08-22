"use strict"

$(document).ready(function() {

	let tabs=$('.tabs a');
	let projectsContainer=$('.projects-container');
	let ideasContainer=$('.ideas-container');

	tabs.click(function() {

		$(this).removeClass('text-muted').siblings().addClass('text-muted');

		if($(this).text().toLowerCase().trim() == 'projects') {

			projectsContainer.removeClass('d-none').addClass('d-flex');
			ideasContainer.removeClass('d-flex').addClass('d-none');
		}
		else if($(this).text().toLowerCase().trim() == 'ideas') {

			ideasContainer.removeClass('d-none').addClass('d-flex');
			projectsContainer.removeClass('d-flex').addClass('d-none');
		}
	})
})