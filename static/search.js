// On load function to set name of file upload area
function onLoad() {
	// Find input area
	var inputs = document.querySelectorAll('.inputfile');
	Array.prototype.forEach.call(inputs, function (input) {

		// Get labe and label value for input area
		var label = document.getElementById("file-label");

		// Listener for when files are uploaded
		input.addEventListener('change', function (e) {
			var fileName = '';

			// Create comma separated string for files to update label HTML
			if (this.files) {
				for (let i = 0; i < this.files.length; i++) {
					val = this.files[i]["name"];
					fileName = fileName + val + ", ";
                }
            }

			label.innerHTML = fileName;

		});

	});
};

// Attach event listener for when page is loaded
document.addEventListener("DOMContentLoaded", onLoad);