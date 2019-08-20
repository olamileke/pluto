"use strict"

$(document).ready(function() {

	let deletebtn=$('a.delete');

	deletebtn.click(function(e) {

		let param=confirm('Are you sure you want to delete?');

		if(!param) {

			e.preventDefault()
		}
	})
})