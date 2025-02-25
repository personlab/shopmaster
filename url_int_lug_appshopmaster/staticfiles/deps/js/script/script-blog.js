// Получаем необходимые элементы
const modal = document.getElementById('imageModal');
const modalImg = document.getElementById('modalImg');
const closeModal = document.querySelector('.close');
const images = document.querySelectorAll('.zoomable-img');

// Клик по картинке для её увеличения
images.forEach(img => {
		img.addEventListener('click', () => {
				modal.style.display = 'block';
				modalImg.src = img.src;
		});
});

// Закрытие модального окна при клике на кнопку закрытия
closeModal.addEventListener('click', () => {
		modal.style.display = 'none';
});

// Закрытие модального окна при клике на любое место за пределами изображения
modal.addEventListener('click', (e) => {
		if (e.target === modal) {
				modal.style.display = 'none';
		}
});