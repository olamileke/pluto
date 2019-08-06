"use strict"

$(document).ready(function() {

	// setting the active class in the sidebar

	let menuOptions=$('ul.menu li');
	let path=window.location.pathname
	let paths=['/','/projects/new']
	let optionTexts=['Dashboard', 'New Project']

	
	for(let i=0; i < paths.length; i++) {

		if(path == paths[i]) {

			menuOptions.each(function() {

				let $this=$(this);

				if($this.text().trim() == optionTexts[i]) {

					$this.addClass('active');
				}
			})

			break;
		}
	}

})