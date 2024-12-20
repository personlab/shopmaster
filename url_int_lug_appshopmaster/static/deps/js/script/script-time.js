// Формат с id="time"


// // time footer
// function updateTime() {
// 	const now = new Date();
// 	const options = {
// 			year: 'numeric',
// 			month: '2-digit',
// 			day: '2-digit',
// 			hour: '2-digit',
// 			minute: '2-digit',
// 			second: '2-digit',
// 			hour12: true // Используйте true & false для 24 - 12-часового формата
// 	};

// 	const formattedTime = now.toLocaleString('en-CA', options);
// 	document.getElementById('time').innerText = formattedTime;
// }

// // Обновляем время сразу, чтобы не ждать 1 секунду
// updateTime();

// // Обновляем время каждую секунду
// setInterval(updateTime, 1000);



// формат с классом time

function updateTime() {
	const now = new Date();
	const options = {
			year: 'numeric',
			month: '2-digit',
			day: '2-digit',
			hour: '2-digit',
			minute: '2-digit',
			second: '2-digit',
			hour12: true // Используйте true & false для 24 - 12-часового формата
	};

	const formattedTime = now.toLocaleString('en-CA', options);
	
	// Получаем все элементы с классом "time"
	const timeElements = document.getElementsByClassName('time');

	// Обновляем текст всех элементов
	for (let i = 0; i < timeElements.length; i++) {
		timeElements[i].innerText = formattedTime;
	}
}

// Обновляем время сразу, чтобы не ждать 1 секунду
updateTime();

// Обновляем время каждую секунду
setInterval(updateTime, 1000);