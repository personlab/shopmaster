'use strict';

/**
 * Add event listener on multiple elements
 */

const addEventOnElements = function (elements, eventType, callback) {
		for (let i = 0, len = elements.length; i < len; i++) {
				elements[i].addEventListener(eventType, callback);
		}
}

/**
 * MOBILE NAVBAR TOGGLER 
 */

const navbar = document.querySelector("[data-navbar]");
const navTogglers = document.querySelectorAll("[data-nav-toggler]");

const toggleNav = () => {
	navbar.classList.toggle("active");
	document.body.classList.toggle("nav-active");
}

addEventOnElements(navTogglers, "click", toggleNav);


/**
 * HEADER ANIMATION
 * when scrolled done to 100px header will be active
 */

const header = document.querySelector("[data-header]");
const backTopBtn = document.querySelector("[data-back-top-btn]");

window.addEventListener("scroll", () => {
		if (window.scrollY > 100) {
				header.classList.add("active");
				backTopBtn.classList.add("active");
		} else {
				header.classList.remove("active");
				backTopBtn.classList.remove("active");
		}
});


/**
 * SLIDER
 */


document.addEventListener('DOMContentLoaded', function() {
	// Инициализация элементов
	const slider = document.querySelector('[data-slider]');
	const sliderContainer = document.querySelector('[data-slider-container]');
	const sliderItems = document.querySelectorAll('.slider-item');
	const sliderDots = document.querySelectorAll('.slider-dot');
	const sliderPrevBtn = document.querySelector('[data-slider-prev]');
	const sliderNextBtn = document.querySelector('[data-slider-next]');
	let currentSlidePos = 0;
	let isDragging = false;
	let startPos = 0;
	let currentTranslate = 0;
	let prevTranslate = 0;
	const gap = 20; // Фиксированный gap между слайдами
	let autoSlideInterval;
	let slideWidth = calculateSlideWidth();

	// Рассчитываем ширину слайда с учетом gap
	function calculateSlideWidth() {
			return sliderItems[0].offsetWidth + gap;
	}

	// Функция обновления позиции
	function setSliderPosition() {
			const offset = currentSlidePos * slideWidth;
			sliderContainer.style.transform = `translateX(-${offset}px)`;
			updateActiveDot();
	}

	// Обновление активной точки
	function updateActiveDot() {
			sliderDots.forEach((dot, index) => {
					dot.classList.toggle('active', index === currentSlidePos);
			});
	}

	// Автоматическая прокрутка
	function startAutoSlide() {
			autoSlideInterval = setInterval(() => {
					currentSlidePos = (currentSlidePos >= sliderItems.length - 1) ? 0 : currentSlidePos + 1;
					sliderContainer.style.transition = 'transform 0.8s ease-out';
					setSliderPosition();
			}, 10000); // 10 секунд
	}

	// Остановка автоматической прокрутки
	function stopAutoSlide() {
			clearInterval(autoSlideInterval);
	}

	// NEXT SLIDE
	function slideNext() {
			currentSlidePos = (currentSlidePos >= sliderItems.length - 1) ? 0 : currentSlidePos + 1;
			sliderContainer.style.transition = 'transform 0.5s ease-out';
			setSliderPosition();
	}

	// PREV SLIDE
	function slidePrev() {
			currentSlidePos = (currentSlidePos <= 0) ? sliderItems.length - 1 : currentSlidePos - 1;
			sliderContainer.style.transition = 'transform 0.5s ease-out';
			setSliderPosition();
	}

// 	// Обработчики кнопок
	sliderNextBtn.addEventListener('click', slideNext);
	sliderPrevBtn.addEventListener('click', slidePrev);

	// Touch-обработчики
	function handleTouchStart(e) {
			isDragging = true;
			startPos = getPositionX(e);
			sliderContainer.style.transition = 'none';
			prevTranslate = -currentSlidePos * slideWidth;
			stopAutoSlide();
	}

	function handleTouchMove(e) {
			if (!isDragging) return;
			const currentPosition = getPositionX(e);
			// Правильное направление движения (палец влево - слайд вправо)
			currentTranslate = prevTranslate + (currentPosition - startPos);
			sliderContainer.style.transform = `translateX(${currentTranslate}px)`;
	}


	function handleTouchEnd(e) {
		if (!isDragging) return;
		isDragging = false;
		
		const touchEndX = getPositionX(e);
		const movedBy = touchEndX - startPos;
		const threshold = slideWidth * 0.15;
		// const isQuickSwipe = (Date.now() - touchStartTime) < 300;
		
		// Если это был свайп
		if (Math.abs(movedBy) > threshold || isQuickSwipe) {
				sliderContainer.style.transition = 'transform 0.5s ease-out';
				
				if (movedBy > threshold) {
						// Свайп влево - слайд вправо (prev)
						slidePrev();
				} else if (movedBy < -threshold) {
						// Свайп влево - слайд влево (next)
						slideNext();
				} else {
					// Возврат к текущему слайду
					sliderContainer.style.transition = 'transform 0.5s ease-out';
					setSliderPosition();
				}
		} else {
				// Это клик - находим элемент под касанием
				const touch = e.changedTouches[0];
				const clickedElement = document.elementFromPoint(touch.clientX, touch.clientY);
				const link = clickedElement.closest('a');
				
				if (link) {
						// Добавляем небольшую задержку для уверенности, что переход обработан
						setTimeout(() => {
								window.location.href = link.href;
						}, 100);
				} else {
						setSliderPosition();
				}
		}
		
		startAutoSlide();
	}

	// function handleTouchEnd() {
	// 		if (!isDragging) return;
	// 		isDragging = false;
			
	// 		const movedBy = currentTranslate - prevTranslate;
	// 		const threshold = slideWidth * 0.15;
			
	// 		// Определение направления свайпа
	// 		if (movedBy > threshold) {
	// 				// Свайп влево - слайд вправо (prev)
	// 				slidePrev();
	// 		} else if (movedBy < -threshold) {
	// 				// Свайп влево - слайд влево (next)
	// 				slideNext();
	// 		} else {
	// 				// Возврат к текущему слайду
	// 				sliderContainer.style.transition = 'transform 0.5s ease-out';
	// 				setSliderPosition();
	// 		}
			
	// 		startAutoSlide();
	// }

	// Получение позиции
	// function getPositionX(e) {
	// 		return e.type.includes('touch') ? e.touches[0].clientX : e.clientX;
	// }

	function getPositionX(e) {
			if (e.type.includes('touch')) {
					return e.touches && e.touches[0] ? e.touches[0].clientX : 
								e.changedTouches && e.changedTouches[0] ? e.changedTouches[0].clientX : 0;
			}
			return e.clientX;
}

	// Добавляем обработчики
	sliderContainer.addEventListener('touchstart', handleTouchStart, {passive: false});
	sliderContainer.addEventListener('touchmove', handleTouchMove, {passive: false});
	sliderContainer.addEventListener('touchend', handleTouchEnd);
	
	// Для десктопов
	sliderContainer.addEventListener('mousedown', (e) => {
			e.preventDefault();
			handleTouchStart(e);
			document.addEventListener('mousemove', handleTouchMove);
			document.addEventListener('mouseup', () => {
					document.removeEventListener('mousemove', handleTouchMove);
					handleTouchEnd();
			}, {once: true});
	});

	// Обработчики точек
	sliderDots.forEach(dot => {
			dot.addEventListener('click', () => {
					stopAutoSlide();
					currentSlidePos = parseInt(dot.dataset.index);
					sliderContainer.style.transition = 'transform 0.5s ease-out';
					setSliderPosition();
					startAutoSlide();
			});
	});

	// Ресайз
	function handleResize() {
			slideWidth = calculateSlideWidth();
			setSliderPosition();
	}

	window.addEventListener('resize', handleResize);
	
	// Инициализация
	setSliderPosition();
	startAutoSlide();

	// Пауза при наведении
	slider.addEventListener('mouseenter', stopAutoSlide);
	slider.addEventListener('mouseleave', startAutoSlide);
});







// document.addEventListener('DOMContentLoaded', function() {
// 	// Инициализация элементов
// 	const slider = document.querySelector('[data-slider]');
// 	const sliderContainer = document.querySelector('[data-slider-container]');
// 	const sliderItems = document.querySelectorAll('.slider-item');
// 	const sliderPrevBtn = document.querySelector('[data-slider-prev]');
// 	const sliderNextBtn = document.querySelector('[data-slider-next]');
// 	const sliderDots = document.querySelectorAll('.slider-dot');
// 	let currentSlidePos = 0;
// 	let isDragging = false;
// 	let startPos = 0;
// 	let currentTranslate = 0;
// 	let prevTranslate = 0;
// 	let animationID = 0;
// 	let slideWidth = sliderItems[0].offsetWidth + 20; // 20px gap

// 	// Функция обновления позиции слайдера
// 	function updateSliderPosition() {
// 			sliderContainer.style.transform = `translateX(-${currentSlidePos * slideWidth}px)`;
// 			updateActiveDot();
// 	}

// 	// Функция обновления активной точки
// 	function updateActiveDot() {
// 			sliderDots.forEach(dot => {
// 					dot.classList.remove('active');
// 					if (parseInt(dot.dataset.index) === currentSlidePos) {
// 							dot.classList.add('active');
// 					}
// 			});
// 	}

// 	// Переключение на конкретный слайд
// 	function goToSlide(index) {
// 			currentSlidePos = index;
// 			updateSliderPosition();
// 	}

// 	// NEXT SLIDE
// 	function slideNext() {
// 			currentSlidePos = (currentSlidePos >= sliderItems.length - 1) ? 0 : currentSlidePos + 1;
// 			updateSliderPosition();
// 	}

// 	// PREV SLIDE
// 	function slidePrev() {
// 			currentSlidePos = (currentSlidePos <= 0) ? sliderItems.length - 1 : currentSlidePos - 1;
// 			updateSliderPosition();
// 	}

// 	// Обработчики кнопок
// 	sliderNextBtn.addEventListener('click', slideNext);
// 	sliderPrevBtn.addEventListener('click', slidePrev);

// 	// Обработчики точек навигации
// 	sliderDots.forEach(dot => {
// 			dot.addEventListener('click', function() {
// 					goToSlide(parseInt(this.dataset.index));
// 			});
// 	});

// 	// Функции для обработки свайпа
// 	function getPositionX(event) {
// 			return event.type.includes('mouse') ? event.pageX : event.touches[0].clientX;
// 	}

// 	function touchStart(event) {
// 			// Проверяем, был ли клик по ссылке
// 			const isLinkClick = event.target.closest('a');
			
// 			if (!isLinkClick) {
// 					startPos = getPositionX(event);
// 					isDragging = true;
// 					sliderContainer.style.transition = 'none';
// 					animationID = requestAnimationFrame(animation);
// 					sliderContainer.classList.add('grabbing');
// 			}
// 	}

// 	function touchMove(event) {
// 			if (isDragging) {
// 					const currentPosition = getPositionX(event);
// 					currentTranslate = prevTranslate + currentPosition - startPos;
					
// 					// Отменяем событие только если это не касание по ссылке
// 					if (!event.target.closest('a')) {
// 							event.preventDefault();
// 					}
// 			}
// 	}

// 	function touchEnd(event) {
// 			if (!isDragging) return;
			
// 			isDragging = false;
// 			cancelAnimationFrame(animationID);
// 			sliderContainer.classList.remove('grabbing');
// 			sliderContainer.style.transition = 'transform 0.3s ease-out';
			
// 			const movedBy = currentTranslate - prevTranslate;
// 			const threshold = slideWidth * 0.2; // 20% ширины слайда
			
// 			if (movedBy < -threshold) {
// 					slideNext();
// 			} else if (movedBy > threshold) {
// 					slidePrev();
// 			} else {
// 					updateSliderPosition();
// 			}
			
// 			// Если движение было небольшим и клик был по ссылке - разрешаем переход
// 			if (Math.abs(movedBy) < 10 && event.target.closest('a')) {
// 					event.target.closest('a').click();
// 			}
// 	}

// 	function animation() {
// 			sliderContainer.style.transform = `translateX(calc(-${currentSlidePos * slideWidth}px + ${currentTranslate - prevTranslate}px)`;
// 			if (isDragging) requestAnimationFrame(animation);
// 	}

// 	// Добавляем обработчики событий
// 	sliderContainer.addEventListener('touchstart', touchStart, {passive: false});
// 	sliderContainer.addEventListener('touchend', touchEnd);
// 	sliderContainer.addEventListener('touchmove', touchMove, {passive: false});
	
// 	sliderContainer.addEventListener('mousedown', touchStart);
// 	sliderContainer.addEventListener('mouseup', touchEnd);
// 	sliderContainer.addEventListener('mouseleave', touchEnd);
// 	sliderContainer.addEventListener('mousemove', touchMove);

// 	// Обработчик ресайза
// 	function handleResize() {
// 			slideWidth = sliderItems[0].offsetWidth + 20;
// 			updateSliderPosition();
// 	}

// 	window.addEventListener('resize', handleResize);

// 	// Автопрокрутка (опционально)
// 	let autoSlideInterval = setInterval(slideNext, 5000);

// 	slider.addEventListener('mouseenter', () => clearInterval(autoSlideInterval));
// 	slider.addEventListener('touchstart', () => clearInterval(autoSlideInterval));
// 	slider.addEventListener('mouseleave', () => {
// 			autoSlideInterval = setInterval(slideNext, 10000);
// 	});

// 	// Инициализация
// 	updateSliderPosition();
// });






// // Инициализация переменных слайдера
// const slider = document.querySelector('[data-slider]');
// const sliderContainer = document.querySelector('[data-slider-container]');
// const sliderItems = document.querySelectorAll('.slider-item');
// const sliderPrevBtn = document.querySelector('[data-slider-prev]');
// const sliderNextBtn = document.querySelector('[data-slider-next]');
// let totalSliderItem = sliderItems.length - 1;
// let isDragging = false;
// let startPos = 0;
// let currentPos = 0;
// let prevPos = 0;
// let animationID = 0;
// let currentSlidePos = 0;
// let movedDistance = 0;

// // Получаем количество видимых слайдов
// let totalSliderVisibleItems = Number(getComputedStyle(slider).getPropertyValue("--slider-items"));

// // Функция для перемещения слайдов
// const moveSliderItem = function () {
// 		const slideWidth = sliderItems[0].offsetWidth + 20; // 20px gap
// 		sliderContainer.style.transform = `translateX(-${currentSlidePos * slideWidth}px)`;
// 		prevPos = -currentSlidePos * slideWidth;
// }

// // NEXT SLIDE
// const slideNext = function () {
// 		const slideEnd = currentSlidePos >= totalSliderItem;
// 		if (slideEnd) {
// 				currentSlidePos = 0;
// 		} else {
// 				currentSlidePos++;
// 		}
// 		moveSliderItem();
// }

// // PREV SLIDE
// const slidePrev = function () {
// 		if (currentSlidePos <= 0) {
// 				currentSlidePos = totalSliderItem;
// 		} else {
// 				currentSlidePos--;
// 		}
// 		moveSliderItem();
// }

// // Обработчики кнопок
// if (sliderNextBtn) sliderNextBtn.addEventListener("click", slideNext);
// if (sliderPrevBtn) sliderPrevBtn.addEventListener("click", slidePrev);

// // Функции для обработки свайпа
// function getPositionX(event) {
// 		return event.type.includes('mouse') ? event.pageX : event.touches[0].clientX;
// }

// function touchStart(event) {
// 		// Отменяем клик только если это не касание по ссылке
// 		if (!event.target.closest('a')) {
// 				event.preventDefault();
// 		}
		
// 		startPos = getPositionX(event);
// 		isDragging = true;
// 		movedDistance = 0;
// 		sliderContainer.classList.add('grabbing');
// 		sliderContainer.style.transition = 'none';
// 		animationID = requestAnimationFrame(animation);
// }

// function touchMove(event) {
// 		if (!isDragging) return;
		
// 		const currentPosition = getPositionX(event);
// 		movedDistance = currentPosition - startPos;
// 		currentPos = prevPos + movedDistance;
		
// 		// Отменяем событие, если это не касание по ссылке
// 		if (Math.abs(movedDistance) > 5 && !event.target.closest('a')) {
// 				event.preventDefault();
// 		}
// }

// function touchEnd(event) {
// 		if (!isDragging) return;
		
// 		isDragging = false;
// 		cancelAnimationFrame(animationID);
// 		sliderContainer.classList.remove('grabbing');
// 		sliderContainer.style.transition = 'transform 0.3s ease-out';
		
// 		const slideWidth = sliderItems[0].offsetWidth + 20; // 20px gap
// 		const threshold = slideWidth * 0.2; // 20% ширины слайда
		
// 		if (movedDistance < -threshold && currentSlidePos < totalSliderItem) {
// 				currentSlidePos++;
// 		} else if (movedDistance > threshold && currentSlidePos > 0) {
// 				currentSlidePos--;
// 		}
		
// 		moveSliderItem();
		
// 		// Если свайп был небольшим, разрешаем клик
// 		if (Math.abs(movedDistance) < 10) {
// 				const link = event.target.closest('a');
// 				if (link) {
// 						link.click();
// 				}
// 		}
// }

// function animation() {
// 		sliderContainer.style.transform = `translateX(${currentPos}px)`;
// 		if (isDragging) requestAnimationFrame(animation);
// }

// // Добавляем обработчики событий для свайпа
// sliderContainer.addEventListener('touchstart', touchStart, {passive: false});
// sliderContainer.addEventListener('touchend', touchEnd);
// sliderContainer.addEventListener('touchmove', touchMove, {passive: false});

// sliderContainer.addEventListener('mousedown', touchStart);
// sliderContainer.addEventListener('mouseup', touchEnd);
// sliderContainer.addEventListener('mouseleave', touchEnd);
// sliderContainer.addEventListener('mousemove', touchMove);

// // Обработчик ресайза
// function handleResize() {
// 		const slideWidth = sliderItems[0].offsetWidth + 20; // 20px gap
// 		totalSliderVisibleItems = Math.min(
// 				Number(getComputedStyle(slider).getPropertyValue("--slider-items")),
// 				sliderItems.length
// 		);
// 		totalSliderItem = sliderItems.length - totalSliderVisibleItems;
// 		moveSliderItem();
// }

// window.addEventListener("resize", handleResize);

// // Инициализация при загрузке
// document.addEventListener('DOMContentLoaded', function() {
// 		handleResize();
		
// 		// Автопрокрутка (опционально)
// 		let autoSlideInterval = setInterval(slideNext, 10000);

// 		// Останавливаем автопрокрутку при взаимодействии
// 		slider.addEventListener('mouseenter', () => clearInterval(autoSlideInterval));
// 		slider.addEventListener('touchstart', () => clearInterval(autoSlideInterval));
// 		slider.addEventListener('mouseleave', () => {
// 				autoSlideInterval = setInterval(slideNext, 10000);
// 		});
// });









// // Инициализация переменных слайдера
// const slider = document.querySelector('[data-slider]');
// const sliderContainer = document.querySelector('[data-slider-container]');
// const sliderItems = document.querySelectorAll('.slider-item');
// const sliderPrevBtn = document.querySelector('[data-slider-prev]');
// const sliderNextBtn = document.querySelector('[data-slider-next]');
// let totalSliderItem = sliderItems.length - 1;
// let isDragging = false;
// let startPos = 0;
// let currentTranslate = 0;
// let prevTranslate = 0;
// let animationID = 0;
// let currentSlidePos = 0;

// // Получаем количество видимых слайдов
// let totalSliderVisibleItems = Number(getComputedStyle(slider).getPropertyValue("--slider-items"));

// // Функция для перемещения слайдов
// const moveSliderItem = function () {
// 		sliderContainer.style.transform = `translateX(-${sliderContainer.children[currentSlidePos].offsetLeft}px)`;
// }


// // NEXT SLIDE
// const slideNext = function () {
// 		const slideEnd = currentSlidePos >= totalSliderItem;
// 		if (slideEnd) {
// 				currentSlidePos = 0;
// 		} else {
// 				currentSlidePos++;
// 		}
// 		moveSliderItem();
// }


// // PREV SLIDE
// const slidePrev = function () {
// 		if (currentSlidePos <= 0) {
// 				currentSlidePos = totalSliderItem;
// 		} else {
// 				currentSlidePos--;
// 		}
// 		moveSliderItem();
// }

// // // Обработчики кнопок
// if (sliderNextBtn) sliderNextBtn.addEventListener("click", slideNext);
// if (sliderPrevBtn) sliderPrevBtn.addEventListener("click", slidePrev);

// // Функции для обработки свайпа
// function getPositionX(event) {
// 		return event.type.includes('mouse') ? event.pageX : event.touches[0].clientX;
// }

// function touchStart(index) {
// 		return function(event) {
// 				currentSlidePos = index;
// 				startPos = getPositionX(event);
// 				isDragging = true;
// 				animationID = requestAnimationFrame(animation);
// 				sliderContainer.classList.add('grabbing');
// 		}
// }

// function touchMove(event) {
// 		if (isDragging) {
// 				const currentPosition = getPositionX(event);
// 				currentTranslate = prevTranslate + currentPosition - startPos;
// 		}
// }

// function touchEnd() {
// 		cancelAnimationFrame(animationID);
// 		isDragging = false;
// 		const movedBy = currentTranslate - prevTranslate;

// 		if (movedBy < -100 && currentSlidePos < totalSliderItem) {
// 				currentSlidePos += 1;
// 		}

// 		if (movedBy > 100 && currentSlidePos > 0) {
// 				currentSlidePos -= 1;
// 		}

// 		setPositionByIndex();
// 		sliderContainer.classList.remove('grabbing');
// }

// function animation() {
// 		sliderContainer.style.transform = `translateX(calc(-${currentSlidePos * 100}% + ${currentTranslate}px))`;
// 		if (isDragging) requestAnimationFrame(animation);
// }

// function setPositionByIndex() {
// 		currentTranslate = currentSlidePos * -window.innerWidth;
// 		prevTranslate = currentTranslate;
// 		sliderContainer.style.transform = `translateX(${currentTranslate}px)`;
// }

// // Добавляем обработчики событий для свайпа
// sliderItems.forEach((item, index) => {
// 		// Touch events
// 		item.addEventListener('touchstart', touchStart(index));
// 		item.addEventListener('touchend', touchEnd);
// 		item.addEventListener('touchmove', touchMove);

// 		// Mouse events
// 		item.addEventListener('mousedown', touchStart(index));
// 		item.addEventListener('mouseup', touchEnd);
// 		item.addEventListener('mouseleave', touchEnd);
// 		item.addEventListener('mousemove', touchMove);
// });

// // Обработчик ресайза
// window.addEventListener("resize", function () {
// 		totalSliderVisibleItems = Number(getComputedStyle(slider).getPropertyValue("--slider-items"));
// 		totalSliderItem = sliderContainer.childElementCount - totalSliderVisibleItems;
// 		moveSliderItem();
// });


// // Автопрокрутка (опционально)
// let autoSlideInterval = setInterval(slideNext, 5000);

// // Останавливаем автопрокрутку при взаимодействии
// slider.addEventListener('mouseenter', () => clearInterval(autoSlideInterval));
// slider.addEventListener('touchstart', () => clearInterval(autoSlideInterval));
// slider.addEventListener('mouseleave', () => {
// 		autoSlideInterval = setInterval(slideNext, 10000);
// });



// /**
//  * SLIDER
//  */

// const slider = document.querySelector("[data-slider]");
// const sliderContainer = document.querySelector("[data-slider-container]");
// const sliderPrevBtn = document.querySelector("[data-slider-prev]");
// const sliderNextBtn = document.querySelector("[data-slider-next]");

// let totalSliderVisibleItems = Number(getComputedStyle(slider).getPropertyValue("--slider-items"));
// let totalSliderItem = sliderContainer.childElementCount - totalSliderVisibleItems;

// let currentSlidePos = 0;

// const moveSliderItem = function () {
// 		sliderContainer.style.transform = `translateX(-${sliderContainer.children[currentSlidePos].offsetLeft}px)`;
// }


// /**
//  * NEXT SLIDE
//  */

// const slideNext = function () {
// 		const slideEnd = currentSlidePos >= totalSliderItem;

// 		if (slideEnd) {
// 			currentSlidePos = 0;
// 		} else {
// 			currentSlidePos++;
// 		}

// 		moveSliderItem();
// }

// sliderNextBtn.addEventListener("click", slideNext);


// /**
//  * PREV SLIDE
//  */

// const slidePrev = function () {
// 		if (currentSlidePos <= 0) {
// 			currentSlidePos = totalSliderItem;
// 		} else {
// 			currentSlidePos--;
// 		}

// 		moveSliderItem();
// }

// sliderPrevBtn.addEventListener("click", slidePrev);

// /**
//  * RESPONSIVE
//  */

// window.addEventListener("resize", function () {
// 		totalSliderVisibleItems = Number(getComputedStyle(slider).getPropertyValue("--slider-items"));
// 		totalSliderItem = sliderContainer.childElementCount - totalSliderVisibleItems;

// 		moveSliderItem();
// });