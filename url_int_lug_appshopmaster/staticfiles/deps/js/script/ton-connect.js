// Инициализация TON Connect UI
const tonConnectUI = new TON_CONNECT_UI.TonConnectUI({
		manifestUrl: 'https://gameton.app/tonconnect-manifest.json',
		buttonRootId: 'ton-connect',
		language: 'ru',
		uiPreferences: {
				theme: 'DARK',
				walletIconsCache: { cacheType: 'local' }
		}
});

// Основная функция обработки подключения
async function handleWalletConnection() {
		try {
				console.log('Начинаем подключение кошелька...');
				
				// Проверяем, не подключен ли уже кошелек
				if (tonConnectUI.connected) {
						console.log('Используем существующее подключение');
						const wallet = tonConnectUI.account;
						if (!wallet || !wallet.address) {
								throw new Error('Кошелек подключен, но адрес не найден');
						}
						return await proceedWithWallet(wallet);
				}
				
				// Пытаемся подключиться
				try {
						const wallet = await tonConnectUI.connectWallet();
						if (!wallet) {
								throw new Error('Подключение не удалось - пустой ответ');
						}
						return await proceedWithWallet(wallet);
				} catch (err) {
						if (err.message.includes('Cancelled by user')) {
								console.log('Пользователь отменил подключение');
								return;
						}
						throw err;
				}
				
		} catch (error) {
				console.error('Ошибка подключения кошелька:', error);
				showNotification(error.message || 'Ошибка подключения к кошельку', 'error');
		}
}

async function proceedWithWallet(wallet) {
		// Получаем адрес (новые версии SDK используют account.address)
		const address = wallet.account?.address || wallet.address;
		if (!address) {
				console.error('Структура объекта кошелька:', wallet);
				throw new Error('Не удалось найти адрес кошелька');
		}

		// Получаем данные Telegram
		const tgUser = window.Telegram?.WebApp?.initDataUnsafe?.user;
		console.log('Данные пользователя Telegram:', tgUser);
		
		// Отправляем на сервер
		await sendWalletDataToServer({ ...wallet, address }, tgUser);
		
		// Обновляем интерфейс
		updateUI(wallet, tgUser);
}

// Отправка данных на сервер
async function sendWalletDataToServer(wallet, tgUser = null) {
		try {
				console.log('Preparing to send wallet data:', wallet);
				
				// Validate the wallet object structure
				if (!wallet?.address) {
						console.error('Invalid wallet object structure:', wallet);
						throw new Error('Invalid wallet data - missing address');
				}

				const payload = {
						address: wallet.address,
						telegram_data: tgUser ? {
								id: tgUser.id,
								username: tgUser.username || null,
								first_name: tgUser.first_name || null,
								last_name: tgUser.last_name || null,
								photo_url: tgUser.photo_url || null
						} : null
				};

				console.log('Sending to server:', payload);

				const response = await fetch('/api/wallet_info/', {
						method: 'POST',
						headers: {
								'Content-Type': 'application/json',
								'X-Requested-With': 'XMLHttpRequest'
						},
						body: JSON.stringify(payload)
				});

				if (!response.ok) {
						const errorData = await response.text();
						throw new Error(`Server error: ${response.status} - ${errorData}`);
				}

				const responseData = await response.json();
				console.log('Server response:', responseData);
				return responseData;
				
		} catch (error) {
				console.error('Error saving wallet:', error);
				throw error;
		}
}

// Обновление интерфейса
function updateUI(wallet, tgUser = null) {
		const container = document.getElementById('user-telegram-info');
		if (!container) return;

		const shortAddress = wallet.address 
				? `${wallet.address.slice(0, 6)}...${wallet.address.slice(-4)}`
				: 'Неизвестный адрес';

		container.innerHTML = `
				<div class="telegram-user">
						${tgUser?.photo_url ? `
						<img src="${tgUser.photo_url}" alt="User Photo" class="telegram-user-photo">` : ''}
						<div class="telegram-user-info">
								<h3>${tgUser ? `${tgUser.first_name || ''} ${tgUser.last_name || ''}` : 'Анонимный пользователь'}</h3>
								${tgUser?.username ? `<p>@${tgUser.username}</p>` : ''}
						</div>
				</div>
		`;
		container.style.display = 'block';
}

// Показать уведомление
function showNotification(message, type = 'success') {
		alert(`${type === 'error' ? 'Ошибка:' : ''} ${message}`);
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
		const connectButton = document.getElementById('ton-connect');
		if (connectButton) {
				connectButton.addEventListener('click', handleWalletConnection);
		}
		
		// Автоматическая обработка при загрузке, если уже подключен
		if (tonConnectUI.connected) {
				handleWalletConnection();
		}
});

// Отслеживаем изменения состояния подключения
tonConnectUI.onStatusChange((wallet) => {
		console.log('Состояние подключения изменилось:', wallet);
		
		if (wallet) {
				console.log('Кошелек подключен:', wallet);
				proceedWithWallet(wallet).catch(console.error);
		} else {
				console.log('Кошелек отключен');
				const container = document.getElementById('user-telegram-info');
				if (container) container.style.display = 'none';
		}
});

// Инициализация при загрузке
tonConnectUI.connectionRestored.then(() => {
		console.log('Инициализация TON Connect завершена');
		if (tonConnectUI.connected) {
				proceedWithWallet(tonConnectUI.account).catch(console.error);
		}
});











// рабочая версия

// // Проверка Telegram WebApp
// if (!window.Telegram?.WebApp) {
// 		console.log('Telegram WebApp environment not detected');
// }


// // Инициализация TON Connect UI
// const tonConnectUI = new TON_CONNECT_UI.TonConnectUI({
// 		manifestUrl: 'https://gameton.app/tonconnect-manifest.json',
// 		buttonRootId: 'ton-connect',
// 		language: 'ru',
// 		uiPreferences: {
// 				theme: 'DARK',
// 				walletIconsCache: { cacheType: 'local' }
// 		}
// });


// // логика подключения и обновления данных:
// async function handleWalletConnection() {
// 		const wallet = tonConnectUI.connected ? tonConnectUI.account : await tonConnectUI.connectWallet();
		
// 		if (wallet) {
// 				await sendWalletDataToServer(wallet);
// 				window.location.reload();
// 		}
// }

// // Инициализация
// document.addEventListener('DOMContentLoaded', () => {
// 		const connectButton = document.getElementById('ton-connect');
// 		if (connectButton) {
// 				connectButton.addEventListener('click', handleWalletConnection);
// 		}
		
// 		// Автоматическая обработка при загрузке, если уже подключен
// 		if (tonConnectUI.connected) {
// 				handleWalletConnection();
// 		}
// });

// // Отправка данных на сервер
// async function sendWalletDataToServer(wallet) {
// 		const tgUser = window.Telegram?.WebApp?.initDataUnsafe?.user;
// 		console.log('Telegram user:', tgUser); // Debug
		
// 		const payload = {
// 				address: wallet.account.address,
// 				telegram_data: tgUser ? {
// 						id: tgUser.id,
// 						username: tgUser.username,
// 						first_name: tgUser.first_name,
// 						last_name: tgUser.last_name,
// 						photo_url: tgUser.photo_url
// 				} : null
// 		};
		
// 		console.log('Sending payload:', payload); // Debug

// 		try {
// 				const response = await fetch('/api/wallet_info/', {
// 						method: 'POST',
// 						headers: {
// 								'Content-Type': 'application/json',
// 						},
// 						body: JSON.stringify(payload)
// 				});
				
// 				const data = await response.json();
// 				console.log('Server response:', data);
// 				return data;
// 		} catch (error) {
// 				console.error('Error:', error);
// 				throw error;
// 		}
// }

// // Показать уведомление
// function showNotification(message, type = 'success') {
// 		alert(`${type === 'error' ? 'Ошибка:' : ''} ${message}`);
// }

// // Инициализация при загрузке страницы
// document.addEventListener('DOMContentLoaded', () => {
// 		const connectButton = document.getElementById('ton-connect');
// 		if (connectButton) {
// 				connectButton.addEventListener('click', connectToWallet);
// 		}
		
// 		// Проверяем, есть ли уже подключенный кошелек
// 		if (tonConnectUI.connected) {
// 				connectToWallet();
// 		}
// });




// // Инициализация TON Connect UI
// const tonConnectUI = new TON_CONNECT_UI.TonConnectUI({
// 		manifestUrl: 'https://gameton.app/tonconnect-manifest.json',
// 		buttonRootId: 'ton-connect',
// 		language: 'ru',
// 		uiPreferences: {
// 				theme: 'DARK',
// 				walletIconsCache: { cacheType: 'local' }
// 		},
// 		actionsConfiguration: {
// 				twaReturnUrl: 'https://t.me/GameTonApp_bot?startapp=webapp'
// 		}
// });

// // Основная функция обработки подключения
// async function handleWalletConnection(connectedWallet) {
// 		if (!connectedWallet) return;
		
// 		const walletData = {
// 				address: connectedWallet.account.address,
// 				telegram: window.Telegram?.WebApp?.initDataUnsafe?.user || null
// 		};

// 		try {
// 				// Отправляем данные на сервер
// 				const response = await saveWalletData(walletData);
				
// 				if (response.success) {
// 						updateUI({
// 								wallet: walletData,
// 								userData: response.user || null
// 						});
// 				} else {
// 						showNotification(response.error || 'Ошибка сохранения данных', 'error');
// 				}
// 		} catch (error) {
// 				console.error('Connection error:', error);
// 				showNotification('Ошибка подключения', 'error');
// 		}
// }

// // Отправка данных на сервер
// async function saveWalletData(data) {
// 			const payload = {
// 					address: data.address,  // изменено с wallet_address на address
// 					telegram_data: data.telegram ? {  // добавляем вложенный объект telegram_data
// 							id: data.telegram.id,
// 							username: data.telegram.username,
// 							first_name: data.telegram.first_name,
// 							last_name: data.telegram.last_name,
// 							photo_url: data.telegram.photo_url
// 					} : null
// 			};

// 			try {
// 					const response = await fetch('https://gameton.app/api/wallet_info/', {
// 							method: 'POST',
// 							headers: {
// 									'Content-Type': 'application/json',
// 									// Уберите CSRF токен или убедитесь, что endpoint имеет @csrf_exempt
// 									// 'X-CSRFToken': getCookie('csrftoken')
// 							},
// 							body: JSON.stringify(payload)
// 					});

// 					if (!response.ok) {
// 							throw new Error(`HTTP error! status: ${response.status}`);
// 					}
// 					return await response.json();
// 			} catch (error) {
// 					console.error('Error saving wallet:', error);
// 					throw error;
// 			}
// }

// // Обновление интерфейса
// function updateUI(data) {
// 		const container = document.getElementById('user-telegram-info');
// 		if (!container) return;

// 		const tg = data.wallet?.telegram;  // Получаем telegram данные из переданного объекта
// 		const address = data.wallet?.address || '';  // Получаем адрес кошелька

// 		let html = '';
// 		if (data.loading) {
// 				html = `<div class="loader">Загрузка данных...</div>`;
// 		} else if (data.error) {
// 				html = `<div class="error">${data.error}</div>`;
// 		} else {
// 				html = `
// 						<div class="wallet-card">
// 								${tg?.photo_url ? `<img src="${tg.photo_url}" alt="User" class="wallet-avatar">` : ''}
// 								<div class="wallet-info">
// 										<h3>${tg ? `${tg.first_name || ''} ${tg.last_name || ''}` : 'Анонимный пользователь'}</h3>
// 										${tg?.username ? `<p>@${tg.username}</p>` : ''}
// 										<p class="wallet-address">${address.slice(0, 6)}...${address.slice(-4)}</p>
// 										${data.userData?.email ? `<p>${data.userData.email}</p>` : ''}
// 								</div>
// 						</div>
// 				`;
// 		}
		
// 		container.innerHTML = html;
// 		container.style.display = 'block';
// }

// // Подписка на изменения статуса кошелька
// tonConnectUI.onStatusChange((wallet) => {
// 		if (wallet) {
// 				handleWalletConnection(wallet);
// 		} else {
// 				const container = document.getElementById('user-telegram-info');
// 				if (container) container.style.display = 'none';
// 		}
// });

// // Инициализация
// document.addEventListener('DOMContentLoaded', () => {
// 		if (tonConnectUI.connected) {
// 				handleWalletConnection(tonConnectUI.account);
// 		}
		
// 		const connectButton = document.getElementById('ton-connect');
// 		if (connectButton) {
// 				connectButton.addEventListener('click', () => tonConnectUI.connectWallet());
// 		}
// });

// // Вспомогательные функции
// function getCookie(name) {
// 		const value = `; ${document.cookie}`;
// 		const parts = value.split(`; ${name}=`);
// 		if (parts.length === 2) return parts.pop().split(';').shift();
// }

// function showNotification(message, type = 'success') {
// 		alert(`${type === 'error' ? 'Ошибка:' : ''} ${message}`);
// }



















// // Проверка Telegram WebApp
// if (!window.Telegram?.WebApp) {
// 		console.log('Telegram WebApp environment not detected');
// }

// // Инициализация TON Connect UI
// const tonConnectUI = new TON_CONNECT_UI.TonConnectUI({
// 		manifestUrl: 'https://gameton.app/tonconnect-manifest.json',
// 		buttonRootId: 'ton-connect',
// 		language: 'ru',
// 		uiPreferences: {
// 				theme: 'DARK',
// 				walletIconsCache: { cacheType: 'local' }
// 		},
// });

// tonConnectUI.uiOptions = {
// 		twaReturnUrl: 'https://t.me/GameTonApp_bot?startapp=webapp'
// };

// // При загрузке страницы проверяем подключенный кошелек
// tonConnectUI.connectionRestored.then(async () => {
// 		const wallet = tonConnectUI.wallet;
// 		if (wallet) {
// 				await handleWalletConnection(wallet);
// 		}
// });

// // Обработчик подключения кошелька
// async function connectToWallet() {
// 		try {
// 				const connectedWallet = await tonConnectUI.connectWallet();
// 				if (connectedWallet) {
// 						await handleWalletConnection(connectedWallet);
// 						window.location.reload();
// 				}
// 		} catch (error) {
// 				console.error("Error connecting to wallet:", error);
// 				showNotification('Ошибка подключения кошелька', 'error');
// 		}
// }

// // Общая функция обработки подключения кошелька
// async function handleWalletConnection(wallet) {
// 		const tgUser = window.Telegram?.WebApp?.initDataUnsafe?.user;
// 		const walletAddress = wallet.account.address;
		
// 		// 1. Отправляем данные на сервер
// 		await sendWalletDataToServer(walletAddress, tgUser);
		
// 		// 2. Показываем информацию пользователя
// 		await showUserInfo(walletAddress);
// }

// // Отправка данных на сервер
// async function sendWalletDataToServer(walletAddress, tgUser = null) {
// 		try {
// 				const response = await fetch('/ton_auth/', {
// 						method: 'POST',
// 						headers: {
// 								'Content-Type': 'application/json',
// 								'X-CSRFToken': getCookie('csrftoken'),
// 						},
// 						body: JSON.stringify({
// 								wallet_address: walletAddress,
// 								telegram_id: tgUser?.id,
// 								telegram_username: tgUser?.username,
// 								telegram_first_name: tgUser?.first_name,
// 								telegram_last_name: tgUser?.last_name,
// 								telegram_photo_url: tgUser?.photo_url,
// 						})
// 				});
// 				return await response.json();
// 		} catch (error) {
// 				console.error('Error sending wallet data:', error);
// 		}
// }

// // Получение и отображение информации о пользователе
// async function showUserInfo(walletAddress) {
// 		try {
// 				const response = await fetch(`/api/user_info/?wallet=${encodeURIComponent(walletAddress)}`);
// 				const data = await response.json();
				
// 				if (data.success && data.user) {
// 						displayUserInfo(data.user, walletAddress);
// 				} else {
// 						displayWalletOnly(walletAddress);
// 				}
// 		} catch (error) {
// 				console.error('Error fetching user info:', error);
// 				displayWalletOnly(walletAddress);
// 		}
// }

// function displayUserInfo(userData, walletAddress) {
// 		const userInfoDiv = document.getElementById('user-telegram-info');
// 		if (!userInfoDiv) return;
		
// 		userInfoDiv.innerHTML = `
// 				<div class="telegram-user">
// 						${userData.photo_url ? `
// 						<img src="${userData.photo_url}" 
// 								alt="User Photo" 
// 								class="telegram-user-photo">` : ''}
// 						<div class="telegram-user-info">
// 								<p>${userData.first_name || ''} ${userData.last_name || ''}</p>
// 								${userData.username ? `<p>@${userData.username}</p>` : ''}
// 								<p class="wallet-address">${walletAddress}</p>
// 						</div>
// 				</div>
// 		`;
// 		userInfoDiv.style.display = 'block';
// }

// function displayWalletOnly(walletAddress) {
// 		const userInfoDiv = document.getElementById('user-telegram-info');
// 		if (!userInfoDiv) return;
		
// 		userInfoDiv.innerHTML = `
// 				<div class="wallet-info">
// 						<p class="wallet-address">${walletAddress}</p>
// 				</div>
// 		`;
// 		userInfoDiv.style.display = 'block';
// }

// // Вспомогательная функция для получения CSRF токена
// function getCookie(name) {
// 		let cookieValue = null;
// 		if (document.cookie && document.cookie !== '') {
// 				const cookies = document.cookie.split(';');
// 				for (let i = 0; i < cookies.length; i++) {
// 						const cookie = cookies[i].trim();
// 						if (cookie.substring(0, name.length + 1) === (name + '=')) {
// 								cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
// 								break;
// 						}
// 				}
// 		}
// 		return cookieValue;
// }












// // Инициализация TON Connect UI
// const tonConnectUI = new TON_CONNECT_UI.TonConnectUI({
// 		manifestUrl: 'https://gameton.app/tonconnect-manifest.json',
// 		buttonRootId: 'ton-connect',
// 		language: 'ru',
// 		uiPreferences: {
// 				theme: 'DARK',
// 		},
// 		actionsConfiguration: {
// 				// returnStrategy: 'back', // 'back' или URL вашего сайта
// 				twaReturnUrl: 'https://t.me/GameTonApp_bot?startapp=webapp' // Раскомментируйте только для TMA
// 		}
// });

// // Обработчик подключения кошелька
// async function connectToWallet() {
// 		try {
// 				const connectedWallet = await tonConnectUI.connectWallet();
// 				console.log('Connected wallet:', connectedWallet);
				
// 				if (connectedWallet) {
// 						await sendWalletDataToServer(connectedWallet);
						
// 						// Обновляем страницу после успешного подключения
// 						window.location.reload();
// 				}
// 		} catch (error) {
// 				console.error("Error connecting to wallet:", error);
// 				showNotification('Ошибка подключения кошелька', 'error');
// 		}
// }

// // Функция для показа уведомлений
// function showNotification(message, type = 'success') {
// 		// Реализуйте вашу систему уведомлений
// 		alert(`${type === 'error' ? 'Ошибка:' : ''} ${message}`);
// }

// // Отправка данных на сервер
// async function sendWalletDataToServer(walletData) {
// 		try {
// 				const response = await fetch('/api/ton-auth/', {
// 						method: 'POST',
// 						headers: {
// 								'Content-Type': 'application/json',
// 								'X-CSRFToken': getCookie('csrftoken')
// 						},
// 						body: JSON.stringify({
// 								address: walletData.account.address,
// 								provider: walletData.provider
// 						})
// 				});

// 				const data = await response.json();
				
// 				if (!data.success) {
// 						throw new Error(data.error || 'Ошибка авторизации');
// 				}
				
// 				return data;
// 		} catch (error) {
// 				console.error('Server request failed:', error);
// 				throw error;
// 		}
// }

// document.addEventListener('DOMContentLoaded', () => {
// 		const userDataDiv = document.getElementById('user-telegram-info');
		
// 		if (window.Telegram?.WebApp?.initDataUnsafe?.user) {
// 				const user = window.Telegram.WebApp.initDataUnsafe.user;
// 				userDataDiv.innerHTML = `
// 					<div class="telegram-user">
// 								${userData.photo_url ? `
// 								<img src="${userData.photo_url}" 
// 										alt="User Photo" 
// 										class="telegram-user-photo">` : ''}
// 								<div class="telegram-user-info">
// 										<p>${userData.first_name || ''} ${userData.last_name || ''}</p>
// 										${userData.username ? `<p>@${userData.username}</p>` : ''}
// 										<p class="wallet-address">${walletAddress}</p>
// 								</div>
// 						</div>
// 				`;
// 		} else {
// 				userDataDiv.innerHTML = '<p>Open this page in Telegram WebApp to see user data</p>';
// 		}
// });


// // function displayUserInfo(userData, walletAddress) {
// // 		const userInfoDiv = document.getElementById('user-telegram-info');
// // 		userInfoDiv.innerHTML = `
// // 				<div class="telegram-user">
// // 						${userData.photo_url ? `
// // 						<img src="${userData.photo_url}" 
// // 								alt="User Photo" 
// // 								class="telegram-user-photo">` : ''}
// // 						<div class="telegram-user-info">
// // 								<p>${userData.first_name || ''} ${userData.last_name || ''}</p>
// // 								${userData.username ? `<p>@${userData.username}</p>` : ''}
// // 								<p class="wallet-address">${walletAddress}</p>
// // 						</div>
// // 				</div>
// // 		`;
// // 		userInfoDiv.style.display = 'block';
// // }



// // Остальные функции остаются без изменений
// function getCookie(name) {
// 		let cookieValue = null;
// 		if (document.cookie && document.cookie !== '') {
// 				const cookies = document.cookie.split(';');
// 				for (let i = 0; i < cookies.length; i++) {
// 						const cookie = cookies[i].trim();
// 						if (cookie.substring(0, name.length + 1) === (name + '=')) {
// 								cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
// 								break;
// 						}
// 				}
// 		}
// 		return cookieValue;
// }

// // Подписка на изменения статуса
// tonConnectUI.onStatusChange((wallet) => {
// 		if (wallet) {
// 				console.log('Wallet changed:', wallet);
// 				// Можно автоматически обновить интерфейс
// 				updateUIForConnectedWallet(wallet);
// 		} else {
// 				console.log('Wallet disconnected');
// 				updateUIForDisconnectedWallet();
// 		}
// });

// // Инициализация при загрузке
// document.addEventListener('DOMContentLoaded', () => {
// 		if (tonConnectUI.connected) {
// 				console.log('Already connected:', tonConnectUI.account);
// 				updateUIForConnectedWallet(tonConnectUI.account);
// 		}
		
// 		const connectButton = document.getElementById('ton-connect');
// 		if (connectButton) {
// 				connectButton.addEventListener('click', connectToWallet);
// 		}
// });

// // Функции обновления интерфейса
// function updateUIForConnectedWallet(wallet) {
// 		// Обновите UI для подключенного кошелька
// 		const button = document.getElementById('ton-connect');
// 		if (button) {
// 				button.textContent = `Кошелек: ${wallet.account.address.slice(0, 4)}...${wallet.account.address.slice(-4)}`;
// 				button.style.backgroundColor = '#4CAF50';
// 		}
// }

// function updateUIForDisconnectedWallet() {
// 		// Верните UI в исходное состояние
// 		const button = document.getElementById('ton-connect');
// 		if (button) {
// 				button.textContent = 'Подключить кошелек';
// 				button.style.backgroundColor = '';
// 		}
// }


// // Инициализация TON Connect UI
// const tonConnectUI = new TON_CONNECT_UI.TonConnectUI({
// 		manifestUrl: 'https://gameton.app/tonconnect-manifest.json',
// 		buttonRootId: 'ton-connect',
// 		language: 'ru',
// 		uiPreferences: {
// 				theme: 'DARK',
// 		}
// });

// tonConnectUI.uiOptions = {
// 		twaReturnUrl: 'https://t.me/GameTonApp_bot?startapp=webapp'
// };

// // информация о пользователе
// async function showUserInfo(wallet) {
// 		const userInfoDiv = document.getElementById('user-telegram-info');
// 		if (!userInfoDiv || !wallet) return;
		
// 		// 1. Пробуем получить данные из Telegram WebApp (если есть)
// 		const tgUser = window.Telegram?.WebApp?.initDataUnsafe?.user;
		
// 		if (tgUser) {
// 				displayUserInfo(tgUser, wallet.address);
// 				await sendAuthData(wallet.address, tgUser);
// 		} else {
// 				try {
// 						const response = await fetch(`/api/user_info/?wallet=${encodeURIComponent(wallet.address)}`, {
// 								headers: {
// 										'Accept': 'application/json' // Явно указываем что ждем JSON
// 								}
// 						});
						
// 						// Проверяем статус ответа
// 						if (!response.ok) {
// 								throw new Error(`HTTP error! status: ${response.status}`);
// 						}
						
// 						// Проверяем content-type
// 						const contentType = response.headers.get('content-type');
// 						if (!contentType || !contentType.includes('application/json')) {
// 								throw new TypeError("Ожидался JSON, но получен " + contentType);
// 						}
						
// 						const userData = await response.json();
						
// 						if (userData.success && userData.user) {
// 								displayUserInfo(userData.user, wallet.address);
// 						} else {
// 								displayWalletOnly(wallet.address);
// 						}
// 				} catch (error) {
// 						console.error('Error fetching user data:', error);
// 						// Добавим больше информации для отладки
// 						try {
// 								const errorResponse = await response.text();
// 								console.error('Response text:', errorResponse);
// 						} catch (e) {
// 								console.error('Could not read error response:', e);
// 						}
// 						displayWalletOnly(wallet.address);
// 				}
// 		}
// }

// function displayUserInfo(userData, walletAddress) {
// 		const userInfoDiv = document.getElementById('user-telegram-info');
// 		userInfoDiv.innerHTML = `
// 				<div class="telegram-user">
// 						${userData.photo_url ? `
// 						<img src="${userData.photo_url}" 
// 								alt="User Photo" 
// 								class="telegram-user-photo">` : ''}
// 						<div class="telegram-user-info">
// 								<p>${userData.first_name || ''} ${userData.last_name || ''}</p>
// 								${userData.username ? `<p>@${userData.username}</p>` : ''}
// 								<p class="wallet-address">${walletAddress}</p>
// 						</div>
// 				</div>
// 		`;
// 		userInfoDiv.style.display = 'block';
// }

// function displayWalletOnly(walletAddress) {
// 		const userInfoDiv = document.getElementById('user-telegram-info');
// 		userInfoDiv.innerHTML = `
// 				<div class="wallet-info">
// 						<p class="wallet-address">${walletAddress}</p>
// 				</div>
// 		`;
// 		userInfoDiv.style.display = 'block';
// }

// // Обработчик подключения кошелька
// tonConnectUI.onStatusChange(async (wallet) => {
// 		if (wallet) {
// 				await showUserInfo(wallet);
// 		} else {
// 				const userInfoDiv = document.getElementById('user-telegram-info');
// 				if (userInfoDiv) userInfoDiv.style.display = 'none';
// 		}
// });

// async function sendAuthData(walletAddress, tgUser) {
// 		try {
// 				await fetch('/ton_auth/', {
// 						method: 'POST',
// 						headers: {
// 								'Content-Type': 'application/json',
// 								'X-CSRFToken': getCookie('csrftoken'),
// 						},
// 						body: JSON.stringify({
// 								wallet_address: walletAddress,
// 								telegram_id: tgUser?.id,
// 								telegram_username: tgUser?.username,
// 								telegram_first_name: tgUser?.first_name,
// 								telegram_last_name: tgUser?.last_name,
// 								telegram_photo_url: tgUser?.photo_url,
// 						})
// 				});
// 		} catch (error) {
// 				console.error('Error sending auth data:', error);
// 		}
// }

// // Вспомогательная функция для получения CSRF токена
// function getCookie(name) {
// 		let cookieValue = null;
// 		if (document.cookie && document.cookie !== '') {
// 				const cookies = document.cookie.split(';');
// 				for (let i = 0; i < cookies.length; i++) {
// 						const cookie = cookies[i].trim();
// 						if (cookie.substring(0, name.length + 1) === (name + '=')) {
// 								cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
// 								break;
// 						}
// 				}
// 		}
// 		return cookieValue;
// }








// // Проверка Telegram WebApp
// if (!window.Telegram?.WebApp) {
// 		console.log('Telegram WebApp environment not detected');
// }

// // Инициализация TON Connect UI
// const tonConnectUI = new TON_CONNECT_UI.TonConnectUI({
// 		manifestUrl: 'https://gameton.app/tonconnect-manifest.json',
// 		buttonRootId: 'ton-connect',
// 		language: 'ru',
// 		uiPreferences: {
// 				theme: 'DARK',
// 		}
// });

// tonConnectUI.uiOptions = {
// 		twaReturnUrl: 'https://t.me/GameTonApp_bot?startapp=webapp'
// };

// // Функция для отображения информации о пользователе
// function showUserInfo(walletInfo, tgUser = null) {
// 		const userInfoDiv = document.getElementById('user-telegram-info');
// 		if (!userInfoDiv) return;
		
// 		// Проверяем, является ли текущий пользователь администратором (вами)
// 		const isAdmin = checkIfAdmin(walletInfo.address); // Нужно реализовать эту функцию
		
// 		if (isAdmin && tgUser) {
// 				// Показываем полную информацию для администратора
// 				userInfoDiv.innerHTML = `
// 						<div class="telegram-user">
// 								${tgUser.photo_url ? `
// 								<img src="${tgUser.photo_url}" 
// 										alt="User Photo" 
// 										class="telegram-user-photo">` : ''}
// 								<div class="telegram-user-info">
// 										<p>${tgUser.first_name || ''} ${tgUser.last_name || ''}</p>
// 										${tgUser.username ? `<p>@${tgUser.username}</p>` : ''}
// 										<p class="wallet-address">${walletInfo.address}</p>
// 								</div>
// 						</div>
// 				`;
// 		} else {
// 				// Для обычных пользователей показываем только адрес кошелька
// 				userInfoDiv.innerHTML = `
// 						<div class="wallet-info">
// 								<p class="wallet-address">${walletInfo.address}</p>
// 						</div>
// 				`;
// 		}
		
// 		userInfoDiv.style.display = 'block';
// }

// // Функция для проверки, является ли пользователь администратором
// function checkIfAdmin(walletAddress) {
// 		// Здесь нужно реализовать проверку, является ли кошелек вашим
// 		// Например, сравнение с заранее заданным адресом
// 		const adminWallets = [
// 				'EQABC...', // Ваш адрес кошелька
// 				'EQDEF...'  // Другие админы
// 		];
// 		return adminWallets.includes(walletAddress);
// }

// // Обработчик подключения кошелька
// tonConnectUI.onStatusChange((wallet) => {
// 		if (wallet) {
// 				// Получаем данные Telegram WebApp
// 				const tgUser = window.Telegram?.WebApp?.initDataUnsafe?.user;
				
// 				// Отправляем данные на сервер
// 				sendAuthData(wallet, tgUser);
				
// 				// Показываем информацию о пользователе
// 				showUserInfo(wallet, tgUser);
// 		}
// });

// // Функция отправки данных аутентификации на сервер
// function sendAuthData(wallet, tgUser) {
// 		fetch('/ton_auth/', {
// 				method: 'POST',
// 				headers: {
// 						'Content-Type': 'application/json',
// 						'X-CSRFToken': getCookie('csrftoken'),
// 				},
// 				body: JSON.stringify({
// 						wallet_address: wallet.address,
// 						telegram_id: tgUser?.id,
// 						telegram_username: tgUser?.username,
// 						telegram_first_name: tgUser?.first_name,
// 						telegram_last_name: tgUser?.last_name,
// 						telegram_photo_url: tgUser?.photo_url,
// 				})
// 		})
// 		.then(response => response.json())
// 		.then(data => {
// 				if (data.success && data.redirect_url) {
// 						window.location.href = data.redirect_url;
// 				}
// 		})
// 		.catch(error => console.error('Error:', error));
// }

// // Вспомогательная функция для получения CSRF токена
// function getCookie(name) {
// 		let cookieValue = null;
// 		if (document.cookie && document.cookie !== '') {
// 				const cookies = document.cookie.split(';');
// 				for (let i = 0; i < cookies.length; i++) {
// 						const cookie = cookies[i].trim();
// 						if (cookie.substring(0, name.length + 1) === (name + '=')) {
// 								cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
// 								break;
// 						}
// 				}
// 		}
// 		return cookieValue;
// }






// // Проверка Telegram WebApp
// if (!window.Telegram?.WebApp) {
// 		console.log('Telegram WebApp environment not detected');
// }

// // Инициализация TON Connect UI
// const tonConnectUI = new TON_CONNECT_UI.TonConnectUI({
// 		manifestUrl: 'https://gameton.app/tonconnect-manifest.json',
// 		buttonRootId: 'ton-connect',
// 		language: 'ru',
// 		uiPreferences: {
// 				theme: 'DARK',
// 		}
// });


// tonConnectUI.uiOptions = {
// 		twaReturnUrl: 'https://t.me/GameTonApp_bot?startapp=webapp'
// };




// // // Проверка десктопной версии (исправленная)
// // function isDesktop() {
// // 		// Если есть Telegram WebApp и это не TDesktop
// // 		if (window.Telegram?.WebApp) {
// // 				return window.Telegram.WebApp.platform === 'tdesktop';
// // 		}
		
// // 		// Если нет Telegram WebApp, проверяем userAgent
// // 		return !/Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
// // }

// // // Обновленный запрос баланса
// // async function getWalletBalance(address) {
// // 		try {
// // 				const response = await fetch(`https://toncenter.com/api/v2/getAddressBalance?address=${address}`);
// // 				const data = await response.json();
// // 				return data.result ? Number(data.result) / 1000000000 : 0;
// // 		} catch (error) {
// // 				console.error('Error fetching balance:', error);
// // 				try {
// // 						// Fallback к альтернативному API
// // 						const backupResponse = await fetch(`https://tonapi.io/v2/accounts/${address}`);
// // 						const backupData = await backupResponse.json();
// // 						return backupData.balance ? Number(backupData.balance) / 1000000000 : 0;
// // 				} catch (e) {
// // 						return 0;
// // 				}
// // 		}
// // }

// // // Обновленный обработчик подключения
// // async function connectToWallet() {
// // 		try {
// // 				const connectedWallet = await tonConnectUI.connectWallet();
// // 				if (connectedWallet) {
// // 						const tgUser = window.Telegram?.WebApp?.initDataUnsafe?.user || null;
// // 						const balance = await getWalletBalance(connectedWallet.account.address);
						
// // 						await sendWalletDataToServer({
// // 								wallet: connectedWallet,
// // 								telegram: tgUser,
// // 								balance: balance
// // 						});

// // 						// Принудительное обновление UI
// // 						setTimeout(() => {
// // 								updateUIAfterConnection(connectedWallet, tgUser, balance);
// // 						}, 500); // Небольшая задержка для гарантии обновления
						
// // 						// Если в WebApp - закрываем после подключения
// // 						if (window.Telegram?.WebApp?.close) {
// // 								setTimeout(() => window.Telegram.WebApp.close(), 1000);
// // 						}
// // 				}
// // 		} catch (error) {
// // 				console.error("Connection error:", error);
// // 				showNotification('Ошибка подключения: ' + error.message, 'error');
// // 		}
// // }



// // Отображение данных Telegram


// function showTelegramUserInfo(tgUser) {
// 		const userInfoDiv = document.getElementById('user-telegram-info');
// 		if (!userInfoDiv) return;
		
// 		userInfoDiv.innerHTML = `
// 				<div class="telegram-user">
// 						${tgUser.photo_url ? `
// 						<img src="${tgUser.photo_url}" 
// 								alt="User Photo" 
// 								class="telegram-user-photo">` : ''}
// 						<div class="telegram-user-info">
// 								<p>${tgUser.first_name || ''} ${tgUser.last_name || ''}</p>
// 								${tgUser.username ? `<p>@${tgUser.username}</p>` : ''}
// 						</div>
// 				</div>
// 		`;
// 		userInfoDiv.style.display = 'block';
// }

// // Отображение баланса
// function showWalletBalance(balance) {
// 		const balanceDiv = document.getElementById('wallet-balance') || document.createElement('div');
// 		balanceDiv.id = 'wallet-balance';
// 		balanceDiv.innerHTML = `<p>Баланс: ${balance.toFixed(2)} TON</p>`;
// 		document.querySelector('.ton-connect-container').appendChild(balanceDiv);
// }

// // Уведомление для десктопной версии (обновленное)
// function showDesktopNotification() {
// 		if (!isDesktop()) return;
		
// 		// Проверяем, есть ли уже уведомление
// 		if (document.getElementById('desktop-notification')) return;
		
// 		const notification = document.createElement('div');
// 		notification.id = 'desktop-notification';
// 		notification.className = 'desktop-notification';
// 		notification.innerHTML = `
// 				<p>Для полного доступа к функциям откройте приложение в мобильной версии Telegram</p>
// 				<a href="https://t.me/GameTonApp_bot?startapp=webapp" target="_blank" class="telegram-app-link">
// 						Открыть в Telegram
// 				</a>
// 		`;
// 		document.body.appendChild(notification);
		
// 		// Автоматическое скрытие через 10 секунд
// 		setTimeout(() => {
// 				notification.style.opacity = '0';
// 				setTimeout(() => notification.remove(), 500);
// 		}, 10000);
// }

// // Вызов функции проверки и уведомления
// showDesktopNotification();



// async function sendWalletDataToServer(data) {
// 		if (!data.wallet?.account?.address) {
// 				throw new Error('Invalid wallet data');
// 		}
		
// 		try {
// 				const response = await fetch('/api/ton-auth/', {
// 						method: 'POST',
// 						headers: {
// 								'Content-Type': 'application/json',
// 								'X-CSRFToken': getCookie('csrftoken')
// 						},
// 						body: JSON.stringify({
// 								wallet_address: data.wallet.account.address,
// 								provider: data.wallet.provider,
// 								balance: data.balance || 0, // Гарантированное значение
// 								telegram_id: data.telegram?.id || null,
// 								telegram_username: data.telegram?.username || null,
// 								telegram_first_name: data.telegram?.first_name || null,
// 								telegram_last_name: data.telegram?.last_name || null,
// 								telegram_photo_url: data.telegram?.photo_url || null
// 						})
// 				});

// 				if (!response.ok) throw new Error('Network error');
// 				return await response.json();
// 		} catch (error) {
// 				console.error('Server request failed:', error);
// 				throw error;
// 		}
// }

// // Инициализация при загрузке
// document.addEventListener('DOMContentLoaded', () => {
// 		if (tonConnectUI.connected) {
// 				tonConnectUI.account && updateUIForConnectedWallet(tonConnectUI.account);
// 		}
		
// 		// Скрываем данные Telegram по умолчанию
// 		const userDataDiv = document.getElementById('user-telegram-info');
// 		if (userDataDiv) userDataDiv.style.display = 'none';
// });


// // Обновление UI после подключения
// async function updateUIAfterConnection(wallet, tgUser, balance) {
// 		updateUIForConnectedWallet(wallet);
		
// 		if (tgUser) {
// 				showTelegramUserInfo(tgUser);
// 		}
		
// 		if (balance > 0) {
// 				showWalletBalance(balance);
// 		}
		
// 		if (isDesktop()) {
// 				showDesktopNotification();
// 		}
// }























// // Добавьте эту проверку в самом начале
// if (!window.Telegram?.WebApp) {
// 		console.error('Telegram WebApp not detected! Load the script: https://telegram.org/js/telegram-web-app.js');
// }


// // Инициализация TON Connect UI
// const tonConnectUI = new TON_CONNECT_UI.TonConnectUI({
// 		manifestUrl: 'https://gameton.app/tonconnect-manifest.json',
// 		buttonRootId: 'ton-connect',
// 		language: 'ru',
// 		uiPreferences: {
// 				theme: 'DARK',
// 		}
// 		// actionsConfiguration: {
// 		// 		returnStrategy: 'https://t.me/GameTonApp_bot?startapp=webapp'
// 		// }
		
// });


// tonConnectUI.uiOptions = {
// 		twaReturnUrl: 'https://t.me/GameTonApp_bot?startapp=webapp'
// };


// // Обновленный обработчик подключения кошелька
// async function connectToWallet() {
// 		try {
// 				const connectedWallet = await tonConnectUI.connectWallet();
// 				if (connectedWallet) {
// 						const tgUser = window.Telegram?.WebApp?.initDataUnsafe?.user || null;
// 						console.log('Telegram user data:', tgUser); // Логируем данные
						
// 						await sendWalletDataToServer({
// 								wallet: connectedWallet,
// 								telegram: tgUser
// 						});
						
// 						checkTelegramUser(); // Обновляем отображение данных
// 						window.location.reload();
// 				}
// 		} catch (error) {
// 				console.error("Connection error:", error);
// 				showNotification('Ошибка подключения: ' + error.message, 'error');
// 		}
// }

// // Инициализация при загрузке
// document.addEventListener('DOMContentLoaded', () => {
// 		checkTelegramUser();
		
// 		// Остальная инициализация...
// 		if (tonConnectUI.connected) {
// 				updateUIForConnectedWallet(tonConnectUI.account);
// 		}
// });


// // Отправка данных на сервер
// async function sendWalletDataToServer(data) {
// 		try {
// 				const response = await fetch('/api/ton-auth/', {
// 						method: 'POST',
// 						headers: {
// 								'Content-Type': 'application/json',
// 								'X-CSRFToken': getCookie('csrftoken')
// 						},
// 						body: JSON.stringify({
// 								wallet_address: data.wallet.account.address,
// 								provider: data.wallet.provider,
// 								telegram_id: data.telegram?.id,
// 								telegram_username: data.telegram?.username,
// 								telegram_first_name: data.telegram?.first_name,
// 								telegram_last_name: data.telegram?.last_name,
// 								telegram_photo_url: data.telegram?.photo_url
// 						})
// 				});

// 				const responseData = await response.json();
// 				if (!responseData.success) {
// 						throw new Error(responseData.error || 'Ошибка авторизации');
// 				}
// 				return responseData;
// 		} catch (error) {
// 				console.error('Server request failed:', error);
// 				throw error;
// 		}
// }

// // Подписка на изменения статуса с отображением Telegram данных
// tonConnectUI.onStatusChange(async (wallet) => {
// 		if (wallet) {
// 				console.log('Wallet changed:', wallet);
				
// 				// Проверяем наличие Telegram WebApp
// 				const telegramUser = window.Telegram?.WebApp?.initDataUnsafe?.user;
// 				if (telegramUser) {
// 						console.log('Telegram user data:', telegramUser);
						
// 						// Создаем элемент для отображения данных
// 						const userInfoDiv = document.getElementById('user-telegram-info') || document.createElement('div');
// 						userInfoDiv.id = 'user-telegram-info';
// 						userInfoDiv.style.display = 'flex';
// 						userInfoDiv.style.alignItems = 'center';
// 						userInfoDiv.style.gap = '10px';
// 						userInfoDiv.style.marginTop = '10px';
						
// 						// Добавляем аватар, если есть
// 						if (telegramUser.photo_url) {
// 								const avatarImg = document.createElement('img');
// 								avatarImg.src = telegramUser.photo_url;
// 								avatarImg.style.width = '40px';
// 								avatarImg.style.height = '40px';
// 								avatarImg.style.borderRadius = '50%';
// 								userInfoDiv.appendChild(avatarImg);
// 						}
						
// 						// Добавляем имя пользователя
// 						const nameDiv = document.createElement('div');
// 						let userName = telegramUser.first_name || '';
// 						if (telegramUser.last_name) userName += ' ' + telegramUser.last_name;
// 						if (telegramUser.username) userName += ` (@${telegramUser.username})`;
						
// 						nameDiv.textContent = userName;
// 						userInfoDiv.appendChild(nameDiv);
						
// 						// Вставляем в DOM
// 						const connectButton = document.getElementById('ton-connect-button');
// 						if (connectButton) {
// 								connectButton.parentNode.insertBefore(userInfoDiv, connectButton.nextSibling);
// 						}
// 				}
				
// 				updateUIForConnectedWallet(wallet);
// 		} else {
// 				console.log('Wallet disconnected');
// 				const userInfoDiv = document.getElementById('user-telegram-info');
// 				if (userInfoDiv) userInfoDiv.remove();
// 				updateUIForDisconnectedWallet();
// 		}
// });

// // Остальные функции остаются без изменений
// function showNotification(message, type = 'success') {
// 		alert(`${type === 'error' ? 'Ошибка:' : ''} ${message}`);
// }

// function getCookie(name) {
// 		let cookieValue = null;
// 		if (document.cookie && document.cookie !== '') {
// 				const cookies = document.cookie.split(';');
// 				for (let i = 0; i < cookies.length; i++) {
// 						const cookie = cookies[i].trim();
// 						if (cookie.substring(0, name.length + 1) === (name + '=')) {
// 								cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
// 								break;
// 						}
// 				}
// 		}
// 		return cookieValue;
// }

// // // Инициализация при загрузке

// // Обновленная функция проверки Telegram данных
// function checkTelegramUser() {
// 		const userDataDiv = document.getElementById('user-data-telegram');
// 		if (!userDataDiv) return;
		
// 		const tgUser = window.Telegram?.WebApp?.initDataUnsafe?.user;
		
// 		if (tgUser) {
// 				userDataDiv.innerHTML = `
// 						<div class="telegram-user">
// 								${tgUser.photo_url ? `
// 								<img src="${tgUser.photo_url}" 
// 										alt="User Photo" 
// 										class="telegram-user-photo">` : ''}
// 								<div class="telegram-user-info">
// 										<p>${tgUser.first_name || ''} ${tgUser.last_name || ''}</p>
// 										${tgUser.username ? `<p>@${tgUser.username}</p>` : ''}
// 								</div>
// 						</div>
// 				`;
// 				userDataDiv.style.display = 'block';
// 		} else {
// 				userDataDiv.innerHTML = '<p class="telegram-warning">Данные Telegram доступны только при открытии через бота</p>';
// 				userDataDiv.style.display = 'none'; // Скрываем, если не в WebApp
// 		}
// }


// // document.addEventListener('DOMContentLoaded', () => {
// // 		if (tonConnectUI.connected) {
// // 				console.log('Already connected:', tonConnectUI.account);
// // 				updateUIForConnectedWallet(tonConnectUI.account);
// // 		}
		
// // 		const connectButton = document.getElementById('ton-connect-button');
// // 		if (connectButton) {
// // 				connectButton.addEventListener('click', connectToWallet);
// // 		}
// // });

// // Функции обновления интерфейса
// function updateUIForConnectedWallet(wallet) {
// 		const button = document.getElementById('ton-connect-button');
// 		if (button) {
// 				button.textContent = `Кошелек: ${wallet.account.address.slice(0, 4)}...${wallet.account.address.slice(-4)}`;
// 				button.style.backgroundColor = '#4CAF50';
// 		}
// }

// function updateUIForDisconnectedWallet() {
// 		const button = document.getElementById('ton-connect-button');
// 		if (button) {
// 				button.textContent = 'Подключить TON кошелек';
// 				button.style.backgroundColor = '';
// 		}
// }














// рабочая версия

// // Инициализация TON Connect UI
// const tonConnectUI = new TON_CONNECT_UI.TonConnectUI({
// 		manifestUrl: 'https://gameton.app/tonconnect-manifest.json',
// 		buttonRootId: 'ton-connect',
// 		language: 'ru',
// 		uiPreferences: {
// 				theme: 'DARK',
// 		},
// 		actionsConfiguration: {
// 				returnStrategy: 'back', // 'back' или URL вашего сайта
// 				// twaReturnUrl: 'https://t.me/GameTonApp_bot' // Раскомментируйте только для TMA
// 		}
// });


// // Обработчик подключения кошелька
// async function connectToWallet() {
// 		try {
// 				const connectedWallet = await tonConnectUI.connectWallet();
// 				console.log('Connected wallet:', connectedWallet);
				
// 				if (connectedWallet) {
// 						await sendWalletDataToServer(connectedWallet);
						
// 						// Обновляем страницу после успешного подключения
// 						window.location.reload();
// 				}
// 		} catch (error) {
// 				console.error("Error connecting to wallet:", error);
// 				showNotification('Ошибка подключения кошелька', 'error');
// 		}
// }

// // Функция для показа уведомлений
// function showNotification(message, type = 'success') {
// 		// Реализуйте вашу систему уведомлений
// 		alert(`${type === 'error' ? 'Ошибка:' : ''} ${message}`);
// }

// // Отправка данных на сервер
// async function sendWalletDataToServer(walletData) {
// 		try {
// 				const response = await fetch('/api/ton-auth/', {
// 						method: 'POST',
// 						headers: {
// 								'Content-Type': 'application/json',
// 								'X-CSRFToken': getCookie('csrftoken')
// 						},
// 						body: JSON.stringify({
// 								address: walletData.account.address,
// 								provider: walletData.provider
// 						})
// 				});

// 				const data = await response.json();
				
// 				if (!data.success) {
// 						throw new Error(data.error || 'Ошибка авторизации');
// 				}
				
// 				return data;
// 		} catch (error) {
// 				console.error('Server request failed:', error);
// 				throw error;
// 		}
// }

// // Остальные функции остаются без изменений
// function getCookie(name) { /* ... */ }

// // Подписка на изменения статуса
// tonConnectUI.onStatusChange((wallet) => {
// 		if (wallet) {
// 				console.log('Wallet changed:', wallet);
// 				// Можно автоматически обновить интерфейс
// 				updateUIForConnectedWallet(wallet);
// 		} else {
// 				console.log('Wallet disconnected');
// 				updateUIForDisconnectedWallet();
// 		}
// });

// // Инициализация при загрузке
// document.addEventListener('DOMContentLoaded', () => {
// 		if (tonConnectUI.connected) {
// 				console.log('Already connected:', tonConnectUI.account);
// 				updateUIForConnectedWallet(tonConnectUI.account);
// 		}
		
// 		const connectButton = document.getElementById('ton-connect-button');
// 		if (connectButton) {
// 				connectButton.addEventListener('click', connectToWallet);
// 		}
// });

// // Функции обновления интерфейса
// function updateUIForConnectedWallet(wallet) {
// 		// Обновите UI для подключенного кошелька
// 		const button = document.getElementById('ton-connect-button');
// 		if (button) {
// 				button.textContent = `Кошелек: ${wallet.account.address.slice(0, 4)}...${wallet.account.address.slice(-4)}`;
// 				button.style.backgroundColor = '#4CAF50';
// 		}
// }

// function updateUIForDisconnectedWallet() {
// 		// Верните UI в исходное состояние
// 		const button = document.getElementById('ton-connect-button');
// 		if (button) {
// 				button.textContent = 'Подключить TON кошелек';
// 				button.style.backgroundColor = '';
// 		}
// }









// // const tonConnectUI = new TON_CONNECT_UI.TonConnectUI({
// // 		manifestUrl: 'https://gameton.app/tonconnect-manifest.json',
// // 		buttonRootId: 'ton-connect'
// // });

// // async function connectToWallet() {
// // 		const connectedWallet = await tonConnectUI.connectWallet();
// // 		// Do something with connectedWallet if needed
// // 		console.log(connectedWallet);
// // }

// // // Call the function
// // connectToWallet().catch(error => {
// // 		console.error("Error connecting to wallet:", error);
// // });

// // tonConnectUI.uiOptions = {
// // 				actionsConfiguration: {
// // 						returnStrategy: 'https://gameton.app/blog/'
// // 				}
// // 		};