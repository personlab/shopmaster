function updateFileName() {
	var input = document.getElementById('id_image');
	var fileNameDisplay = document.getElementById('file-name');
	if (input.files.length > 0) {
		fileNameDisplay.textContent = input.files[0].name; // Отображаем имя файла вместо текста
	} else {
		fileNameDisplay.textContent = 'Выберите файл'; // Возвращаем исходный текст, если файл не выбран
	}
}