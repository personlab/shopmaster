document.getElementById('contact-form').addEventListener('input', function(e) {
	if (e.target.name === 'user_phone') {
			// Автоматическое форматирование при вводе
			let value = e.target.value.replace(/\D/g, '');
			if (value.length > 0) {
					if (value.startsWith('7')) {
							value = '+7' + value.substring(1);
					} else if (value.startsWith('8')) {
							value = '+7' + value.substring(1);
					}
					e.target.value = value;
			}
	}
});




// document.getElementById('contact-form').addEventListener('submit', function(e) {
// 	const phoneInput = this.querySelector('input[name="user_phone"]');
// 	const phoneValue = phoneInput.value.trim();
	
// 	// Проверяем формат номера: +7XXXXXXXXXX или 8XXXXXXXXXX
// 	const phoneRegex = /^(\+7|8)\d{10}$/;
// 	const digitsOnly = phoneValue.replace(/\D/g, '');
	
// 	if (!phoneRegex.test(phoneValue)) {
// 			// Показываем ошибку
// 			document.getElementById('contact-message').textContent = '❌ Введите номер в формате +7XXX... или 8XXX...';
// 			document.getElementById('contact-message').style.color = 'red';
// 			e.preventDefault();
// 			return false;
// 	}
	
// 	// Если номер начинается с 8, заменяем на +7
// 	if (digitsOnly.startsWith('8')) {
// 			phoneInput.value = '+7' + digitsOnly.slice(1);
// 	}
	
// 	return true;
// });