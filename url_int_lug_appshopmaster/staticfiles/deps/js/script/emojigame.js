const emojis = ["💞","💞","🚀","🚀","📈","📈","🔒","🔒","🐳","🐳","😎","😎","👍","👍","📲","📲"];
let gameStarted = false;

function initGame() {
		const gameTable = document.querySelector('.telegram_game_table');
		gameTable.innerHTML = '';
		
		var shuf_emojis = emojis.sort(() => (Math.random() > .5) ? 2 : -1);
		
		for (var i = 0; i < emojis.length; i++) {
				let box = document.createElement('div');
				box.className = 'item';
				box.innerHTML = shuf_emojis[i];
				
				// Добавляем обработчик клика для карточек
				box.addEventListener('click', function() {
						this.classList.toggle('boxOpen');
						setTimeout(function(){
							if (document.querySelectorAll('.boxOpen').length > 1) {
								if (document.querySelectorAll('.boxOpen')[0].innerHTML == document.querySelectorAll('.boxOpen')[1].innerHTML) {
									document.querySelectorAll('.boxOpen')[0].classList.add('boxMatch');
									document.querySelectorAll('.boxOpen')[1].classList.add('boxMatch');

									document.querySelectorAll('.boxOpen')[1].classList.remove('boxOpen');
									document.querySelectorAll('.boxOpen')[0].classList.remove('boxOpen');

									// if (document.querySelectorAll('.boxMatch').length == emojis.length) {
									// 	alert('TELEGRAM WALLET БУДУЩЕЕ У ТЕБЯ В РУКЕ ')
									// }
									if (document.querySelectorAll('.boxMatch').length == emojis.length) {
										// Создаем модальное окно
										const modal = document.createElement('div');
										modal.style.cssText = `
												position: fixed;
												top: 0;
												left: 0;
												width: 100%;
												height: 100%;
												background: rgba(0,0,0,0.8);
												display: flex;
												justify-content: center;
												align-items: center;
												z-index: 1000;
										`;
										
										modal.innerHTML = `
												<div style="background: white; padding: 30px; border-radius: 15px; text-align: center;">
														<h2 style="color: #333; margin-bottom: 20px;">TELEGRAM WALLET - БУДУЩЕЕ У ТЕБЯ В РУКЕ</h2>
														<a href="https://t.me/wallet" 
															target="_blank" 
															style="display: inline-block; 
																			background: #0088cc; 
																			color: white; 
																			padding: 15px 30px; 
																			text-decoration: none; 
																			border-radius: 8px; 
																			font-weight: bold;
																			margin: 10px;">
																Перейти в Telegram Wallet
														</a>
														<br>
														<button onclick="this.parentElement.parentElement.remove()" 
																		style="margin-top: 20px; 
																					padding: 10px 20px; 
																					background: #ccc; 
																					border: none; 
																					border-radius: 5px; 
																					cursor: pointer;">
																Закрыть
														</button>
												</div>
										`;
										
										document.body.appendChild(modal);
								}

								} else {
									document.querySelectorAll('.boxOpen')[1].classList.remove('boxOpen');
									document.querySelectorAll('.boxOpen')[0].classList.remove('boxOpen');
								}
							}
						}, 500)
				});
				
				gameTable.appendChild(box);
		}
		
		gameStarted = true;
}

// Инициализация при загрузке
document.addEventListener('DOMContentLoaded', function() {
		const resetBtn = document.querySelector('.resset_telegram_game');
		
		resetBtn.addEventListener('click', function(e) {
				e.preventDefault();
				initGame();
		});
		
		initGame(); // Запускаем игру первый раз
});




// добавить  onclick="window.location.reload();"


// const emojis = ["💞","💞","🚀","🚀","📈","📈","🔒","🔒","🐳","🐳","😎","😎","👍","👍","📲","📲"];

// function initGame() {
// 		const gameTable = document.querySelector('.telegram_game_table');
// 		gameTable.innerHTML = ''; // Очищаем поле
		
// 		var shuf_emojis = emojis.sort(() => (Math.random() > .5) ? 2 : -1);
		
// 		for (var i = 0; i < emojis.length; i++) {
// 				let box = document.createElement('div');
// 				box.className = 'item';
// 				box.innerHTML = shuf_emojis[i];
// 				gameTable.appendChild(box);
// 		}
// }

// // Инициализируем игру при загрузке
// document.addEventListener('DOMContentLoaded', initGame);

// // Обработчик для кнопки reset
// document.querySelector('.resset_telegram_game').addEventListener('click', function(e) {
// 		e.preventDefault(); // Предотвращаем стандартное поведение
// 		initGame(); // Перезапускаем игру
// });




// const emojis = ["💞","💞","🚀","🚀","📈","📈","🔒","🔒","🐳","🐳","😎","😎","👍","👍","📲","📲"];
// var shuf_emojis = emojis.sort(() => (Math.random() > .5) ? 2 : -1);
// for (var i =0; i<emojis.length; i++){
// 	let box = document.createElement('div')
// 	box.className = 'item';
// 	box.innerHTML = shuf_emojis[i];
// 	document.querySelector('.telegram_game_table').appendChild(box);
// }