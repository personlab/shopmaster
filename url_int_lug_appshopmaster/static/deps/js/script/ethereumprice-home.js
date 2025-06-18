async function fetchEthereumPrice() {
	try {
			// Используем эндпоинт с 24-часовыми изменениями
			const response = await fetch('https://api.binance.com/api/v3/ticker/24hr?symbol=ETHUSDT');
			
			if (!response.ok) {
					throw new Error(`Ошибка сети: ${response.status} ${response.statusText}`);
			}

			const data = await response.json();

			if (!data.lastPrice || !data.priceChangePercent) {
					throw new Error('Данные о цене ETH не найдены в ответе API');
			}

			// Округляем значения
			const roundedPrice = parseFloat(data.lastPrice).toFixed(2);
			const changePercent = parseFloat(data.priceChangePercent).toFixed(2);
			
			// Обновляем цену
			document.getElementById('ethereum-price-home').innerHTML = `
				<span class="crypto-etereum-text">ETH:</span>
				<span class="crypto-name">Ethereum</span>
				<span class="crypto-price">$${roundedPrice}</span>
			`;
			
			// Обновляем процент изменения
			const changeElement = document.getElementById('ethereum-change-home');
			changeElement.textContent = `${changePercent}%`;
			
			// Устанавливаем класс в зависимости от значения
			changeElement.className = 'price-change ' + (changePercent >= 0 ? 'positive' : 'negative');
	} catch (error) {
			console.error('Ошибка получения цены ETHEREUM:', error);
			document.getElementById('ethereum-price-home').textContent = 'Ошибка загрузки цены';
			document.getElementById('ethereum-change-home').textContent = '';
	}
}

// Запускаем сразу и затем каждые 10 секунд
fetchEthereumPrice();
setInterval(fetchEthereumPrice, 10000);