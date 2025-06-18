$(document).ready(function() {
		// Конфигурация
		const config = {
				swipeThreshold: 50,
				autoSlideInterval: 5000
		};

		let autoSlideTimer;
		let startX = 0;
		let currentX = 0;
		let isDragging = false;
		let totalPages = 0;
		let currentPage = 1;

		// Основная функция инициализации
		function initSlider() {
				totalPages = parseInt($('.pagination-btn:not([aria-label]):last').text()) || 
										$('.pagination-btn:not([aria-label])').length;
				currentPage = parseInt($('.pagination-btn.active__button').text()) || 1;
				
				bindPaginationEvents();
				bindSwipeEvents();
				startAutoSlide();
				
				// Восстанавливаем кликабельность ссылок
				restoreLinks();
		}

		// Функция для восстановления работы ссылок
		function restoreLinks() {
				$('.recent-post-card a').off('click').on('click', function(e) {
						// Разрешаем переход по ссылке
						if ($(this).attr('href') && !$(this).hasClass('pagination-btn')) {
								window.location.href = $(this).attr('href');
						}
				});
		}

		// Автоматическое перелистывание
		function startAutoSlide() {
				stopAutoSlide();
				autoSlideTimer = setInterval(() => {
						const nextPage = currentPage >= totalPages ? 1 : currentPage + 1;
						goToPage(nextPage);
				}, config.autoSlideInterval);
		}

		function stopAutoSlide() {
				clearInterval(autoSlideTimer);
		}

		// Переход на конкретную страницу
		function goToPage(pageNum) {
				const pageBtn = $(`.pagination-btn:not([aria-label]):contains("${pageNum}")`);
				if (pageBtn.length && !pageBtn.hasClass('active__button')) {
						pageBtn.trigger('click');
				}
		}

		// Обработка пагинации
		function bindPaginationEvents() {
				$('.pagination-btn').off('click').on('click', function(event) {
						event.preventDefault();
						const url = $(this).attr('href');
						
						if (url !== '#') {
								stopAutoSlide();
								$.get(url, function(data) {
										$('.recent-post .container').html($(data).find('.recent-post .container').html());
										$('.pagination').html($(data).find('.pagination').html());
										
										currentPage = parseInt($(data).find('.pagination-btn.active__button').text()) || currentPage;
										
										bindPaginationEvents();
										bindSwipeEvents();
										startAutoSlide();
										restoreLinks(); // Восстанавливаем ссылки после загрузки
								});
						}
				});
		}

		// Обработка свайпа с проверкой целевого элемента
		function bindSwipeEvents() {
				const $gridList = $('.grid-list-recent');
				
				$gridList.css({
						'cursor': 'pointer',
						'user-select': 'none'
				});

				// Touch события
				$gridList.on('touchstart', function(e) {
						// Пропускаем, если клик по ссылке
						if ($(e.target).closest('a').length) return;
						
						startX = e.originalEvent.touches[0].clientX;
						isDragging = true;
						$(this).css('cursor', 'grabbing');
						stopAutoSlide();
				}).on('touchmove', function(e) {
						if (!isDragging) return;
						currentX = e.originalEvent.touches[0].clientX;
						$(this).css('cursor', 'grabbing');
				}).on('touchend', function(e) {
						if (!isDragging) return;
						$(this).css('cursor', 'pointer');
						isDragging = false;
						
						// Пропускаем, если клик по ссылке
						if ($(e.target).closest('a').length) return;
						
						handleSwipe();
						startAutoSlide();
				});

				// Mouse события
				$gridList.on('mousedown', function(e) {
						// Пропускаем, если клик по ссылке
						if ($(e.target).closest('a').length) return;
						
						startX = e.clientX;
						isDragging = true;
						$(this).css('cursor', 'grabbing');
						stopAutoSlide();
				}).on('mousemove', function(e) {
						if (!isDragging) return;
						currentX = e.clientX;
				}).on('mouseup', function(e) {
						if (!isDragging) return;
						$(this).css('cursor', 'pointer');
						isDragging = false;
						
						// Пропускаем, если клик по ссылке
						if ($(e.target).closest('a').length) return;
						
						handleSwipe();
						startAutoSlide();
				}).on('mouseleave', function() {
						$(this).css('cursor', 'pointer');
						isDragging = false;
				});
		}

		// Обработка жеста свайпа
		function handleSwipe() {
				const diffX = startX - currentX;
				
				if (Math.abs(diffX) > config.swipeThreshold) {
						if (diffX > 0) {
								const nextPage = currentPage >= totalPages ? 1 : currentPage + 1;
								goToPage(nextPage);
						} else {
								const prevPage = currentPage <= 1 ? totalPages : currentPage - 1;
								goToPage(prevPage);
						}
				}
		}

		// Инициализация
		initSlider();

		// Пауза при наведении
		$('.recent-post').hover(
				function() { stopAutoSlide(); },
				function() { startAutoSlide(); }
		);
});







// $(document).ready(function() {
// 		// Конфигурация
// 		const config = {
// 				swipeThreshold: 50,
// 				autoSlideInterval: 5000
// 		};

// 		let autoSlideTimer;
// 		let startX = 0;
// 		let currentX = 0;
// 		let isDragging = false;
// 		let totalPages = 0;
// 		let currentPage = 1;

// 		// Основная функция инициализации
// 		function initSlider() {
// 				// Получаем общее количество страниц
// 				totalPages = parseInt($('.pagination-btn:not([aria-label]):last').text()) || 
// 										$('.pagination-btn:not([aria-label])').length;
				
// 				// Получаем текущую страницу
// 				currentPage = parseInt($('.pagination-btn.active__button').text()) || 1;
				
// 				bindPaginationEvents();
// 				bindSwipeEvents();
// 				startAutoSlide();
// 		}

// 		// Автоматическое перелистывание с правильным циклом
// 		function startAutoSlide() {
// 				stopAutoSlide();
// 				autoSlideTimer = setInterval(() => {
// 						const nextPage = currentPage >= totalPages ? 1 : currentPage + 1;
// 						goToPage(nextPage);
// 				}, config.autoSlideInterval);
// 		}

// 		function stopAutoSlide() {
// 				clearInterval(autoSlideTimer);
// 		}

// 		// Переход на конкретную страницу
// 		function goToPage(pageNum) {
// 				const pageBtn = $(`.pagination-btn:not([aria-label]):contains("${pageNum}")`);
// 				if (pageBtn.length && !pageBtn.hasClass('active__button')) {
// 						pageBtn.trigger('click');
// 				}
// 		}

// 		// Обработка пагинации
// 		function bindPaginationEvents() {
// 				$('.pagination-btn').off('click').on('click', function(event) {
// 						event.preventDefault();
// 						const url = $(this).attr('href');
						
// 						if (url !== '#') {
// 								stopAutoSlide();
// 								$.get(url, function(data) {
// 										$('.recent-post .container').html($(data).find('.recent-post .container').html());
// 										$('.pagination').html($(data).find('.pagination').html());
										
// 										// Обновляем текущую страницу
// 										currentPage = parseInt($(data).find('.pagination-btn.active__button').text()) || currentPage;
										
// 										bindPaginationEvents();
// 										bindSwipeEvents();
// 										startAutoSlide();
// 								});
// 						}
// 				});
// 		}

// 		// Обработка свайпа с улучшенной логикой
// 		function bindSwipeEvents() {
// 				const $gridList = $('.grid-list-recent');
				
// 				// Добавляем стили для курсора
// 				$gridList.css({
// 						'cursor': 'pointer',
// 						'user-select': 'none'
// 				});

// 				// Touch события
// 				$gridList.on('touchstart', function(e) {
// 						startX = e.originalEvent.touches[0].clientX;
// 						isDragging = true;
// 						$(this).css('cursor', 'grabbing');
// 						stopAutoSlide();
// 						e.preventDefault();
// 				}).on('touchmove', function(e) {
// 						if (!isDragging) return;
// 						currentX = e.originalEvent.touches[0].clientX;
// 						$(this).css('cursor', 'grabbing');
// 						e.preventDefault();
// 				}).on('touchend', function() {
// 						if (!isDragging) return;
// 						$(this).css('cursor', 'pointer');
// 						isDragging = false;
// 						handleSwipe();
// 						startAutoSlide();
// 				});

// 				// Mouse события
// 				$gridList.on('mousedown', function(e) {
// 						startX = e.clientX;
// 						isDragging = true;
// 						$(this).css('cursor', 'grabbing');
// 						stopAutoSlide();
// 						e.preventDefault();
// 				}).on('mousemove', function(e) {
// 						if (!isDragging) return;
// 						currentX = e.clientX;
// 						e.preventDefault();
// 				}).on('mouseup', function() {
// 						if (!isDragging) return;
// 						$(this).css('cursor', 'pointer');
// 						isDragging = false;
// 						handleSwipe();
// 						startAutoSlide();
// 				}).on('mouseleave', function() {
// 						$(this).css('cursor', 'pointer');
// 						isDragging = false;
// 				});
// 		}

// 		// Обработка жеста свайпа
// 		function handleSwipe() {
// 				const diffX = startX - currentX;
				
// 				if (Math.abs(diffX) > config.swipeThreshold) {
// 						if (diffX > 0) {
// 								// Свайп влево - следующая страница
// 								const nextPage = currentPage >= totalPages ? 1 : currentPage + 1;
// 								goToPage(nextPage);
// 						} else {
// 								// Свайп вправо - предыдущая страница
// 								const prevPage = currentPage <= 1 ? totalPages : currentPage - 1;
// 								goToPage(prevPage);
// 						}
// 				}
// 		}

// 		// Инициализация при загрузке
// 		initSlider();

// 		// Пауза при наведении
// 		$('.recent-post').hover(
// 				function() { stopAutoSlide(); },
// 				function() { startAutoSlide(); }
// 		);
// });

// recent post



// $(document).ready(function() {
// 	function bindPaginationEvents() {
// 			$('.pagination-btn').off('click').on('click', function(event) {
// 					event.preventDefault(); // Предотвращаем перезагрузку страницы
// 					const url = $(this).attr('href');
					
// 					if (url !== '#') {
// 							$.get(url, function(data) {
// 									// Обновляем контейнер с постами
// 									$('.recent-post .container').html($(data).find('.recent-post .container').html());

// 									// Обновляем саму пагинацию
// 									$('.pagination').html($(data).find('.pagination').html());
									
// 									// Повторно привязываем события
// 									bindPaginationEvents();
// 							});
// 					}
// 			});
// 	}
	
// 	bindPaginationEvents();
// });



// - Снятие событий перед переинициализацией: Используем .off('click') для снятия предыдущих обработчиков событий, чтобы предотвратить их накопление.
// - Повторная привязка событий: После каждого обновления пагинации снова вызываем функцию bindPaginationEvents, чтобы привязать обработчики ко всем новым элементам.