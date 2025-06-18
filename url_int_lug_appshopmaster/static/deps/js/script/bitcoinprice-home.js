async function fetchBitCoinPrice() {
	try {
			// Используем эндпоинт с 24-часовыми изменениями
			const response = await fetch('https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT');
			
			if (!response.ok) {
					throw new Error(`Ошибка сети: ${response.status} ${response.statusText}`);
			}

			const data = await response.json();

			if (!data.lastPrice || !data.priceChangePercent) {
					throw new Error('Данные о цене BTC не найдены в ответе API');
			}

			// Округляем значения
			const roundedPrice = parseFloat(data.lastPrice).toFixed(2);
			const changePercent = parseFloat(data.priceChangePercent).toFixed(2);
			
			// Обновляем цену
			// document.getElementById('bitcoin-price-home').textContent = `BTC: $${roundedPrice}`;
			document.getElementById('bitcoin-price-home').innerHTML = `
				<span class="crypto-symbol">BTC:</span>
				<span class="crypto-name">Bitcoin</span>
				<span class="crypto-price">$${roundedPrice}</span>
			`;
			
			// Обновляем процент изменения
			const changeElement = document.getElementById('bitcoin-change-home');
			changeElement.textContent = `${changePercent}%`;
			
			
			// Устанавливаем класс в зависимости от значения
			changeElement.className = 'price-change ' + (changePercent >= 0 ? 'positive' : 'negative');
	} catch (error) {
			console.error('Ошибка получения цены BITCOIN:', error);
			document.getElementById('bitcoin-price-home').textContent = 'Ошибка загрузки цены';
			document.getElementById('bitcoin-change-home').textContent = '';
	}
}

// Запускаем сразу и затем каждые 10 секунд
fetchBitCoinPrice();
setInterval(fetchBitCoinPrice, 10000);


// async function fetchBitCoinPrice() {
// 	try {
// 			const response = await fetch('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT');
			
// 			if (!response.ok) {
// 					throw new Error(`Ошибка сети: ${response.status} ${response.statusText}`);
// 			}

// 			const data = await response.json();

// 			if (!data.price) {
// 					throw new Error('Данные о цене BTC не найдены в ответе API');
// 			}

// 			// Округляем цену до 2 знаков после запятой
// 			const roundedPrice = parseFloat(data.price).toFixed(2);
// 			document.getElementById('bitcoin-price-home').textContent = `BTC: $${roundedPrice}`;
// 	} catch (error) {
// 			console.error('Ошибка получения цены BITCOIN:', error);
// 			document.getElementById('bitcoin-price-home').textContent = 'Ошибка загрузки цены';
// 	}
// }

// fetchBitCoinPrice();
// setInterval(fetchBitCoinPrice, 10000);