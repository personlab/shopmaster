# import psycopg2

# # Параметры подключения
# # Параметры подключения
# conn_params = {
# 		'dbname': 'postgres',  # Используйте имя вашей БД
# 		'user': 'postgres',     # Имя пользователя
# 		'password': '1234',  # Замените на ваш пароль
# 		'host': 'localhost',
# 		'port': '5432'
# }

# # Инициализация переменных
# connection = None
# cursor = None

# try:
# 		# Устанавливаем соединение
# 		connection = psycopg2.connect(**conn_params)
# 		print("Подключение к базе данных успешно!")

# 		# Создание курсора для выполнения SQL-запросов
# 		cursor = connection.cursor()

# 		# Пример выполнения простого запроса
# 		cursor.execute("SELECT version();")
# 		version = cursor.fetchone()
# 		print("Версия PostgreSQL:", version)

# except Exception as e:
# 		print("Ошибка при подключении к базе данных:", e)

# finally:
# 		# Закрытие курсора и соединения
# 		if cursor is not None:
# 				cursor.close()
# 		if connection is not None:
# 				connection.close()
