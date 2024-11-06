// document.addEventListener('DOMContentLoaded', function () {
// 	let images = Array.from(document.querySelectorAll('[data-image]'));
// 	let currentIndex = 0;
// 	let myModal = document.getElementById('imageModal1');
	
// 	myModal.addEventListener('show.bs.modal', function (event) {
// 			let button = event.relatedTarget;
// 			currentIndex = parseInt(button.getAttribute('data-index'));
// 			updateModalImage();
// 	});
	
// 	document.getElementById('prevImage').addEventListener('click', function () {
// 			if (currentIndex > 0) {
// 					currentIndex--;
// 					updateModalImage();
// 			}
// 	});
	
// 	document.getElementById('nextImage').addEventListener('click', function () {
// 			if (currentIndex < images.length - 1) {
// 					currentIndex++;
// 					updateModalImage();
// 			}
// 	});

// 	function updateModalImage() {
// 			let modalImage = myModal.querySelector('#modalImage');
// 			let newImageUrl = images[currentIndex].getAttribute('data-image');
// 			modalImage.src = newImageUrl;
// 	}
// });


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



	// // Получаем ссылку на модальное окно
	// var myModal = document.getElementById('imageModal1');
	// myModal.addEventListener('show.bs.modal', function (event) {
	// 	// Получаем изображение, которое было нажато
	// 	var button = event.relatedTarget; // Кнопка, вызвавшая событие
	// 	var imageUrl = button.getAttribute('data-image'); // Извлекаем URL изображения из data-атрибута
	// 	var modalImage = myModal.querySelector('#modalImage'); // Находим элемент изображения в модале
	// 	modalImage.src = imageUrl; // Устанавливаем src изображения
	// });