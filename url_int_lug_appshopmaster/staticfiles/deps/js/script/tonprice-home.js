

async function fetchTonPrice() {
	try {
		// Используем эндпоинт с 24-часовыми изменениями
		const response = await fetch('https://api.binance.com/api/v3/ticker/24hr?symbol=TONUSDT');
			
			if (!response.ok) {
					throw new Error(`Ошибка сети: ${response.status} ${response.statusText}`);
			}

			const data = await response.json();
			
			if (!data.lastPrice || !data.priceChangePercent) {
					throw new Error('Данные о цене TON не найдены в ответе API');
			}
			
			// Округляем значения
			const roundedPrice = parseFloat(data.lastPrice).toFixed(2);
			const changePercent = parseFloat(data.priceChangePercent).toFixed(2);
			
			// Обновляем цену
			// document.getElementById('ton-price-home').textContent = `TON: $${roundedPrice}`;

			document.getElementById('ton-price-home').innerHTML = `
			<span class="crypto-ton">TON:</span>
			<span class="crypto-name">Toncoin</span>
			<span class="crypto-price">$${roundedPrice}</span>
		`;
			
			// Обновляем процент изменения
			const changeElement = document.getElementById('ton-change-home');
			changeElement.textContent = `${changePercent}%`;
			
			// Устанавливаем класс в зависимости от значения
			changeElement.className = 'price-change ' + (changePercent >= 0 ? 'positive' : 'negative');
		} catch (error) {
			console.error('Ошибка получения цены TON:', error);
			document.getElementById('ton-price-home').textContent = 'Ошибка загрузки цены';
			document.getElementById('ton-change-home').textContent = '';
		}
	}
	

// Запускаем сразу и затем каждые 10 секунд
fetchTonPrice();
setInterval(fetchTonPrice, 10000);




// async function fetchTonPrice() {
// 	try {
// 			const response = await fetch('https://api.binance.com/api/v3/ticker/price?symbol=TONUSDT');
			
// 			if (!response.ok) {
// 					throw new Error(`Ошибка сети: ${response.status} ${response.statusText}`);
// 			}

// 			const data = await response.json();

// 			if (!data.price) {
// 					throw new Error('Данные о цене TON не найдены в ответе API');
// 			}

// 			// Округляем цену до 2 знаков после запятой
// 			const roundedPrice = parseFloat(data.price).toFixed(2);
// 			document.getElementById('ton-price-home').textContent = `TON: $${roundedPrice}`;
// 	} catch (error) {
// 			console.error('Ошибка получения цены TON:', error);
// 			document.getElementById('ton-price-home').textContent = 'Ошибка загрузки цены';
// 	}
// }

// fetchTonPrice();
// setInterval(fetchTonPrice, 10000);