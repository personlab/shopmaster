$(document).ready(function() {
	function bindPaginationEvents() {
			$('.pagination-btn').off('click').on('click', function(event) {
					event.preventDefault(); // Предотвращаем перезагрузку страницы
					const url = $(this).attr('href');
					
					if (url !== '#') {
							$.get(url, function(data) {
									// Обновляем контейнер с постами
									$('.recent-post .container').html($(data).find('.recent-post .container').html());

									// Обновляем саму пагинацию
									$('.pagination').html($(data).find('.pagination').html());
									
									// Повторно привязываем события
									bindPaginationEvents();
							});
					}
			});
	}
	
	bindPaginationEvents();
});



// - Снятие событий перед переинициализацией: Используем .off('click') для снятия предыдущих обработчиков событий, чтобы предотвратить их накопление.
// - Повторная привязка событий: После каждого обновления пагинации снова вызываем функцию bindPaginationEvents, чтобы привязать обработчики ко всем новым элементам.