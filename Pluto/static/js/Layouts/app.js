"use strict"

$(document).ready(function() {


	// configuration options for the scroll-to-top button

    $('body').materialScrollTop({
	    
	    duration:1000,
	    easing:'swing'
	});


	// setting the active class in the sidebar

	let menuOptions=$('ul.menu li');
	let path=window.location.pathname
	let paths=['/','/projects/new', '/ideas/new', '/projects', '/ideas']
	let optionTexts=['Dashboard', 'New Project', 'New Idea', 'Projects', 'Ideas']

	
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


	// toggling the responsive sidebar

	let navtoggle=$('.navtoggle');
	let sidebar=$('.responsive-sidebar');

	navtoggle.click(function() {

		$(this).toggleClass('active');
		sidebar.toggleClass('active');
	})

})