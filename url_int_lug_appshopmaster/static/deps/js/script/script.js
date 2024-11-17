document.addEventListener('DOMContentLoaded', function () {
	let images = Array.from(document.querySelectorAll('.img-thumbnail[data-bs-toggle="modal"]'));
	let currentIndex = 0;
	let myModal = new bootstrap.Modal(document.getElementById('imageModal'));

	images.forEach(function (image, index) {
		image.addEventListener('click', function () {
			currentIndex = index;
			updateModalImage();
			myModal.show();
		});
	});

	document.getElementById('prevImage').addEventListener('click', function () {
		if (currentIndex > 0) {
			currentIndex--;
			updateModalImage();
		}
	});

	document.getElementById('nextImage').addEventListener('click', function () {
		if (currentIndex < images.length - 1) {
			currentIndex++;
			updateModalImage();
		}
	});

	function updateModalImage() {
		let modalImage = document.getElementById('modalImage');
		let newImageUrl = images[currentIndex].src;
		modalImage.src = newImageUrl;
	}
});