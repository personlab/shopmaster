$(document).ready(function() {
	$('#users__commentss').on('submit', function(e) {
			e.preventDefault();  // Предотвращаем стандартную отправку формы

			var form = $(this);
			var url = form.attr('action');
			var textarea = form.find('textarea[name="text"]');

			// Отправляем данные через AJAX
			$.ajax({
					type: 'POST',
					url: url,
					data: form.serialize(),  // Сериализуем данные формы
					headers: {
							'X-Requested-With': 'XMLHttpRequest'  // Указываем, что это AJAX-запрос
					},
					success: function(response) {
							if (response.success) {
									// Очищаем текстовое поле
									textarea.val('');

									// Добавляем новый комментарий под формой
									$('.comment-list').append(`
											<li>
													<div class="comment-card">
															<blockquote class="card-text">
																	“${response.comment.text}”
															</blockquote>
															<div class="profile-card">
																	<figure class="profile-banner img-holder">
																			<img src="${response.comment.author_image}" width="32" height="32" loading="lazy" alt="${response.comment.author}">
																	</figure>
																	<div>
																			<p class="card-title">${response.comment.author}</p>
																			<time datetime="${response.comment.created_at}" class="card-date">${response.comment.created_at}</time>
																	</div>
															</div>
													</div>
											</li>
									`);
							} else {
									alert('Ошибка при отправке комментария.');
							}
					},
					error: function(xhr, status, error) {
							alert('Произошла ошибка при отправке запроса.');
					}
			});
	});
});


// $(document).ready(function() {
// 	$('#users__commentss').on('submit', function(e) {
// 			e.preventDefault();  // Предотвращаем стандартную отправку формы

// 			var form = $(this);
// 			var url = form.attr('action');
// 			var textarea = form.find('textarea[name="text"]');
// 			var userImage = form.data('user-image'); // Получаем URL аватарки пользователя

// 			// Отправляем данные через AJAX
// 			$.ajax({
// 					type: 'POST',
// 					url: url,
// 					data: form.serialize(),  // Сериализуем данные формы
// 					headers: {
// 							'X-Requested-With': 'XMLHttpRequest'  // Указываем, что это AJAX-запрос
// 					},
// 					success: function(response) {
// 							if (response.success) {
// 									// Очищаем текстовое поле
// 									textarea.val('');

// 									// Добавляем новый комментарий под формой
// 									$('.comment-list').append(`
// 											<li>
// 													<div class="comment-card">
// 															<blockquote class="card-text">
// 																	“${response.comment.text}”
// 															</blockquote>
// 															<div class="profile-card">
// 																	<figure class="profile-banner img-holder">
// 																			<img src="${userImage}" width="32" height="32" loading="lazy" alt="${response.comment.author}">
// 																	</figure>
// 																	<div>
// 																			<p class="card-title">${response.comment.author}</p>
// 																			<time datetime="${response.comment.created_at}" class="card-date">${response.comment.created_at}</time>
// 																	</div>
// 															</div>
// 													</div>
// 											</li>
// 									`);
// 							} else {
// 									alert('Ошибка при отправке комментария.');
// 							}
// 					},
// 					error: function(xhr, status, error) {
// 							alert('Произошла ошибка при отправке запроса.');
// 					}
// 			});
// 	});
// });
