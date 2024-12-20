// =============== email js ==============

$(document).ready(function () {
	$('#contact-form').on('submit', function (e) {
			e.preventDefault(); // Предотвращаем стандартное поведение

			$.ajax({
					type: 'POST',
					url: '', // URL, куда отправляется запрос
					data: $(this).serialize(),
					success: function (response) {
							$('#contact-message').text(response.message);
							
							// Очищаем поля формы
							$('#contact-form')[0].reset(); // Сбрасываем форму
					},
					error: function () {
							$('#contact-message').text('Ошибка отправки сообщения.');
					}
			});
	});
});




$.ajaxSetup({
	headers: {
			'X-CSRFToken': getCookie('csrftoken')  // Функция getCookie должна извлекать токен из куки
	}
});

function getCookie(name) {
		let cookieValue = null;
		if (document.cookie && document.cookie !== '') {
				const cookies = document.cookie.split(';');
				for (let i = 0; i < cookies.length; i++) {
						const cookie = cookies[i].trim();
						// Проверяем, начинается ли cookie с имени нашего токена
						if (cookie.substring(0, name.length + 1) === (name + '=')) {
								cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
								break;
						}
				}
		}
		return cookieValue;
}


