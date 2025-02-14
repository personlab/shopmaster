document.addEventListener('DOMContentLoaded', function () {
	// Проверяем, было ли уже согласие на использование cookies
	if (!document.cookie.includes('cookies_accepted=true')) {
			// Показываем модальное окно
			const modal = document.getElementById('cookieModal');
			modal.style.display = 'flex';

			// Обработчик для кнопки "Принять"
			const acceptButton = document.getElementById('acceptCookies');
			acceptButton.addEventListener('click', function () {
					// Устанавливаем cookie на 30 дней
					const date = new Date();
					date.setTime(date.getTime() + (30 * 24 * 60 * 60 * 1000));
					document.cookie = 'cookies_accepted=true; expires=' + date.toUTCString() + '; path=/';

					// Скрываем модальное окно
					modal.style.display = 'none';
			});
	}
});