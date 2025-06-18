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




// document.addEventListener('DOMContentLoaded', function() {
// 		// Основные элементы
// 		console.log(sliderItems)
// 		const sliderWrapper = document.querySelector('.slider-wrapper');
// 		const sliderContainer = document.querySelector('.slider-container');
// 		const sliderItems = document.querySelectorAll('.slider-item');
// 		const prevBtn = document.querySelector('[data-slider-prev-two]');
// 		const nextBtn = document.querySelector('[data-slider-next-two]');
		
// 		let currentIndex = 0;
// 		let isDragging = false;
// 		let startPosX = 0;
// 		let currentTranslate = 0;
// 		let prevTranslate = 0;
// 		let animationId;
// 		let autoSlideInterval;
		
// 		// Инициализация слайдера
// 		function initSlider() {
// 				// Создаем точки пагинации
// 				sliderItems.forEach((_, index) => {
// 						const dot = document.createElement('div');
// 						dot.classList.add('slider-dot');
// 						dot.dataset.index = index;
						
// 						dot.addEventListener('click', () => {
// 								goToSlide(index);
// 						});
// 				});
				
// 				startAutoSlide();
				
// 				// Обработчики событий
// 				prevBtn.addEventListener('click', goToPrevSlide);
// 				nextBtn.addEventListener('click', goToNextSlide);
				
// 				// Touch события
// 				sliderContainer.addEventListener('touchstart', touchStart, {passive: false});
// 				sliderContainer.addEventListener('touchmove', touchMove, {passive: false});
// 				sliderContainer.addEventListener('touchend', touchEnd);
				
// 				// Mouse события
// 				sliderContainer.addEventListener('mousedown', mouseDown);
				
// 				// Ресайз окна
// 				window.addEventListener('resize', handleResize);
				
// 				// Пауза при наведении
// 				sliderWrapper.addEventListener('mouseenter', stopAutoSlide);
// 				sliderWrapper.addEventListener('mouseleave', startAutoSlide);
// 		}
		
// 		// Переход к конкретному слайду
// 		function goToSlide(index) {
// 				stopAutoSlide();
// 				currentIndex = index;
// 				updateSliderPosition();
// 				startAutoSlide();
// 		}
		
// 		// Следующий слайд
// 		function goToNextSlide() {
// 				stopAutoSlide();
// 				currentIndex = (currentIndex >= sliderItems.length - 1) ? 0 : currentIndex + 1;
// 				updateSliderPosition();
// 				startAutoSlide();
// 		}
		
// 		// Предыдущий слайд
// 		function goToPrevSlide() {
// 				stopAutoSlide();
// 				currentIndex = (currentIndex <= 0) ? sliderItems.length - 1 : currentIndex - 1;
// 				updateSliderPosition();
// 				startAutoSlide();
// 		}
		
// 		// Обновление позиции слайдера
// 		function updateSliderPosition() {
// 				sliderContainer.style.transition = 'transform 0.5s ease-out';
// 				sliderContainer.style.transform = `translateX(-${currentIndex * 100}%)`;
// 		}
		
// 		// Автопрокрутка
// 		function startAutoSlide() {
// 				autoSlideInterval = setInterval(goToNextSlide, 10000);
// 		}
		
// 		function stopAutoSlide() {
// 				clearInterval(autoSlideInterval);
// 		}
		
// 		// Обработчики touch событий
// 		function touchStart(e) {
// 				isDragging = true;
// 				startPosX = e.touches[0].clientX;
// 				sliderContainer.style.transition = 'none';
// 				prevTranslate = -currentIndex * sliderContainer.offsetWidth;
// 				stopAutoSlide();
// 		}
		
// 		function touchMove(e) {
// 				if (!isDragging) return;
// 				const currentPosX = e.touches[0].clientX;
// 				currentTranslate = prevTranslate + (currentPosX - startPosX);
// 				sliderContainer.style.transform = `translateX(${currentTranslate}px)`;
// 		}
		
// 		function touchEnd() {
// 				if (!isDragging) return;
// 				isDragging = false;
				
// 				const movedBy = currentTranslate - prevTranslate;
// 				const threshold = sliderContainer.offsetWidth * 0.15;
				
// 				if (Math.abs(movedBy) > threshold) {
// 						if (movedBy > 0) {
// 								goToPrevSlide();
// 						} else {
// 								goToNextSlide();
// 						}
// 				} else {
// 						updateSliderPosition();
// 				}
				
// 				startAutoSlide();
// 		}
		
// 		// Обработчики mouse событий
// 		function mouseDown(e) {
// 				e.preventDefault();
// 				isDragging = true;
// 				startPosX = e.clientX;
// 				// sliderContainer.style.transition = 'none';
// 				prevTranslate = -currentIndex * sliderContainer.offsetWidth;
// 				stopAutoSlide();
				
// 				document.addEventListener('mousemove', mouseMove);
// 				document.addEventListener('mouseup', mouseUp);
// 		}
		
// 		function mouseMove(e) {
// 				if (!isDragging) return;
// 				const currentPosX = e.clientX;
// 				currentTranslate = prevTranslate + (currentPosX - startPosX);
// 				sliderContainer.style.transform = `translateX(${currentTranslate}px)`;
// 		}
		
// 		function mouseUp() {
// 				if (!isDragging) return;
// 				isDragging = false;
// 				document.removeEventListener('mousemove', mouseMove);
// 				document.removeEventListener('mouseup', mouseUp);
				
// 				const movedBy = currentTranslate - prevTranslate;
// 				const threshold = sliderContainer.offsetWidth * 0.15;
				
// 				if (Math.abs(movedBy) > threshold) {
// 						if (movedBy > 0) {
// 								goToPrevSlide();
// 						} else {
// 								goToNextSlide();
// 						}
// 				} else {
// 						updateSliderPosition();
// 				}
				
// 				startAutoSlide();
// 		}
		
// 		// Ресайз окна
// 		function handleResize() {
// 				updateSliderPosition();
// 		}
		
// 		// Инициализация слайдера
// 		initSlider();
// });



// document.addEventListener('DOMContentLoaded', function() {
// 	// Инициализация элементов
// 	const slider = document.querySelector('[data-site-gameton]');
// 	const sliderContainer = document.querySelector('[data-site-gameton-container]');
// 	const sliderItems = document.querySelectorAll('.slider-item');
// 	const sliderPrevBtn = document.querySelector('[data-slider-prev]');
// 	const sliderNextBtn = document.querySelector('[data-slider-next]');
// 	let currentSlidePos = 0;
// 	let isDragging = false;
// 	let startPos = 0;
// 	let currentTranslate = 0;
// 	let prevTranslate = 0;
// 	let autoSlideInterval;
// 	let slideWidth = calculateSlideWidth();

// 	// Функция обновления позиции
// 	function setSliderPosition() {
// 			const offset = currentSlidePos * slideWidth;
// 			sliderContainer.style.transform = `translateX(-${offset}px)`;
// 			updateActiveDot();
// 	}

// 	// Автоматическая прокрутка
// 	function startAutoSlide() {
// 			autoSlideInterval = setInterval(() => {
// 					currentSlidePos = (currentSlidePos >= sliderItems.length - 1) ? 0 : currentSlidePos + 1;
// 					sliderContainer.style.transition = 'transform 0.8s ease-out';
// 					setSliderPosition();
// 			}, 5000); // 10 секунд
// 	}

// 	// Остановка автоматической прокрутки
// 	function stopAutoSlide() {
// 			clearInterval(autoSlideInterval);
// 	}

// 	// NEXT SLIDE
// 	function slideNext() {
// 			currentSlidePos = (currentSlidePos >= sliderItems.length - 1) ? 0 : currentSlidePos + 1;
// 			sliderContainer.style.transition = 'transform 0.5s ease-out';
// 			setSliderPosition();
// 	}

// 	// PREV SLIDE
// 	function slidePrev() {
// 			currentSlidePos = (currentSlidePos <= 0) ? sliderItems.length - 1 : currentSlidePos - 1;
// 			sliderContainer.style.transition = 'transform 0.5s ease-out';
// 			setSliderPosition();
// 	}

// // 	// Обработчики кнопок
// 	sliderNextBtn.addEventListener('click', slideNext);
// 	sliderPrevBtn.addEventListener('click', slidePrev);

// 	// Touch-обработчики
// 	function handleTouchStart(e) {
// 			isDragging = true;
// 			startPos = getPositionX(e);
// 			sliderContainer.style.transition = 'none';
// 			prevTranslate = -currentSlidePos * slideWidth;
// 			stopAutoSlide();
// 	}

// 	function handleTouchMove(e) {
// 			if (!isDragging) return;
// 			const currentPosition = getPositionX(e);
// 			// Правильное направление движения (палец влево - слайд вправо)
// 			currentTranslate = prevTranslate + (currentPosition - startPos);
// 			sliderContainer.style.transform = `translateX(${currentTranslate}px)`;
// 	}


// 	function handleTouchEnd(e) {
// 		if (!isDragging) return;
// 		isDragging = false;
		
// 		const touchEndX = getPositionX(e);
// 		const movedBy = touchEndX - startPos;
// 		const threshold = slideWidth * 0.15;
// 		// const isQuickSwipe = (Date.now() - touchStartTime) < 300;
		
// 		// Если это был свайп
// 		if (Math.abs(movedBy) > threshold || isQuickSwipe) {
// 				sliderContainer.style.transition = 'transform 0.5s ease-out';
				
// 				if (movedBy > threshold) {
// 						// Свайп влево - слайд вправо (prev)
// 						slidePrev();
// 				} else if (movedBy < -threshold) {
// 						// Свайп влево - слайд влево (next)
// 						slideNext();
// 				} else {
// 					// Возврат к текущему слайду
// 					sliderContainer.style.transition = 'transform 0.5s ease-out';
// 					setSliderPosition();
// 				}
// 		} else {
// 				// Это клик - находим элемент под касанием
// 				const touch = e.changedTouches[0];
// 				const clickedElement = document.elementFromPoint(touch.clientX, touch.clientY);
// 				const link = clickedElement.closest('a');
				
// 				if (link) {
// 						// Добавляем небольшую задержку для уверенности, что переход обработан
// 						setTimeout(() => {
// 								window.location.href = link.href;
// 						}, 100);
// 				} else {
// 						setSliderPosition();
// 				}
// 		}
		
// 		startAutoSlide();
// 	}

// 	function getPositionX(e) {
// 			if (e.type.includes('touch')) {
// 					return e.touches && e.touches[0] ? e.touches[0].clientX : 
// 								e.changedTouches && e.changedTouches[0] ? e.changedTouches[0].clientX : 0;
// 			}
// 			return e.clientX;
// }

// 	// Добавляем обработчики
// 	sliderContainer.addEventListener('touchstart', handleTouchStart, {passive: false});
// 	sliderContainer.addEventListener('touchmove', handleTouchMove, {passive: false});
// 	sliderContainer.addEventListener('touchend', handleTouchEnd);
	
// 	// Для десктопов
// 	sliderContainer.addEventListener('mousedown', (e) => {
// 			e.preventDefault();
// 			handleTouchStart(e);
// 			document.addEventListener('mousemove', handleTouchMove);
// 			document.addEventListener('mouseup', () => {
// 					document.removeEventListener('mousemove', handleTouchMove);
// 					handleTouchEnd();
// 			}, {once: true});
// 	});

// 	// Обработчики точек
// 	sliderDots.forEach(dot => {
// 			dot.addEventListener('click', () => {
// 					stopAutoSlide();
// 					currentSlidePos = parseInt(dot.dataset.index);
// 					sliderContainer.style.transition = 'transform 0.5s ease-out';
// 					setSliderPosition();
// 					startAutoSlide();
// 			});
// 	});

// 	// Ресайз
// 	function handleResize() {
// 			slideWidth = calculateSlideWidth();
// 			setSliderPosition();
// 	}

// 	window.addEventListener('resize', handleResize);
	
// 	// Инициализация
// 	setSliderPosition();
// 	startAutoSlide();

// 	// Пауза при наведении
// 	slider.addEventListener('mouseenter', stopAutoSlide);
// 	slider.addEventListener('mouseleave', startAutoSlide);
// });




// document.addEventListener('DOMContentLoaded', function() {
// 		try {
// 				const swiper = new Swiper('.swiper', {
// 						autoHeight: true,
// 						loop: true,
// 						pagination: {
// 								el: '.swiper-pagination',
// 						},
// 						navigation: {
// 								nextEl: '.swiper-button-next',
// 								prevEl: '.swiper-button-prev',
// 						},
// 				});
// 				console.log('Swiper initialized successfully');
// 		} catch (error) {
// 				console.error('Swiper initialization error:', error);
// 		}
// });




// const swiper = new Swiper('.swiper', {
	
// 	autoHeight: true,
// 	loop: true,

// 	// If we need pagination
// 	pagination: {
// 		el: '.swiper-pagination',
// 	},

// 	// Navigation arrows
// 	navigation: {
// 		nextEl: '.swiper-button-next',
// 		prevEl: '.swiper-button-prev',
// 	},
// });





// document.addEventListener('DOMContentLoaded', function() {
// 		const swiper = new Swiper('.swiper-container', {
// 				// Параметры
// 				slidesPerView: 'auto',
// 				spaceBetween: 20,
// 				freeMode: true,
// 				grabCursor: true,
// 				mousewheel: {
// 						forceToAxis: true,
// 				},
// 				// Пагинация (опционально)
// 				pagination: {
// 						el: '.swiper-pagination',
// 						clickable: true,
// 				},
// 				// Навигационные кнопки (опционально)
// 				navigation: {
// 						nextEl: '.swiper-button-next',
// 						prevEl: '.swiper-button-prev',
// 				},
// 				// Адаптивность
// 				breakpoints: {
// 						// при 768px и выше
// 						768: {
// 								spaceBetween: 30
// 						}
// 				}
// 		});
// });