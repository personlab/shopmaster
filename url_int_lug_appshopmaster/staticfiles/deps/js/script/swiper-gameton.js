document.addEventListener('DOMContentLoaded', function() {
		// 1. Получаем элементы слайдера
		const sliderWrapper = document.querySelector('.testimonial-wrapper');
		const sliderContainer = document.querySelector('.testimonial-container');
		const sliderItems = document.querySelectorAll('.testimonial-item');
		const prevBtn = document.querySelector('[data-testimonial-prev]');
		const nextBtn = document.querySelector('[data-testimonial-next]');

		// 2. Проверяем, что все элементы существуют
		if (!sliderWrapper || !sliderContainer || sliderItems.length === 0 || !prevBtn || !nextBtn) {
				console.error('Не найдены необходимые элементы слайдера');
				return;
		}

		console.log('Найдено слайдов:', sliderItems.length);

		// 3. Настройки слайдера
		let currentIndex = 0;
		let isDragging = false;
		let startPosX = 0;
		let autoSlideInterval;
		const slideWidth = sliderItems[0].offsetWidth;

		// 4. Функция обновления позиции слайдера
		function updateSliderPosition() {
				const offset = currentIndex * slideWidth;
				sliderContainer.style.transform = `translateX(-${offset}px)`;
				console.log(`Текущий слайд: ${currentIndex}, смещение: ${offset}px`);
		}

		// 5. Переход к следующему слайду
		function nextSlide() {
				currentIndex = (currentIndex >= sliderItems.length - 1) ? 0 : currentIndex + 1;
				sliderContainer.style.transition = 'transform 0.5s ease';
				updateSliderPosition();
		}

		// 6. Переход к предыдущему слайду
		function prevSlide() {
				currentIndex = (currentIndex <= 0) ? sliderItems.length - 1 : currentIndex - 1;
				sliderContainer.style.transition = 'transform 0.5s ease';
				updateSliderPosition();
		}

		// 7. Автопрокрутка
		function startAutoSlide() {
				stopAutoSlide();
				autoSlideInterval = setInterval(nextSlide, 5000);
		}

		function stopAutoSlide() {
				if (autoSlideInterval) {
						clearInterval(autoSlideInterval);
				}
		}

		// 8. Обработчики кнопок
		prevBtn.addEventListener('click', function() {
				stopAutoSlide();
				prevSlide();
				startAutoSlide();
		});

		nextBtn.addEventListener('click', function() {
				stopAutoSlide();
				nextSlide();
				startAutoSlide();
		});

		// 9. Инициализация слайдера
		function initSlider() {
				// Устанавливаем ширину контейнера
				sliderContainer.style.width = `${sliderItems.length * 100}%`;
				
				// Устанавливаем ширину для каждого слайда
				sliderItems.forEach(item => {
						item.style.width = `${100 / sliderItems.length}%`;
				});

				// Показываем первый слайд
				updateSliderPosition();
				
				// Запускаем автопрокрутку
				startAutoSlide();
				
				// Пауза при наведении
				sliderWrapper.addEventListener('mouseenter', stopAutoSlide);
				sliderWrapper.addEventListener('mouseleave', startAutoSlide);
		}

		// 10. Запускаем слайдер
		initSlider();

		// 11. Обработка ресайза окна
		window.addEventListener('resize', function() {
				updateSliderPosition();
		});
});

