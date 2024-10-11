Приложение для управления общественной библиотеой.

1.Подготовка. Перед запуском web-приложения создайте файл Dockerfile в которой опишите сценарий создания web-приложения. 
Сценарий отвечает за установку всех необходимых пакетов из файла pyproject.toml, за создание базы данных, создание и примените миграции. 
Также заполните файл .env со всеми переменными окружения для успешной установки и работы сервиса. Файл создается по образцу .env_sample.

2.Подготовка контейнеров Docker. Подготовьте файл docker-compose.yaml для создания и запуска контейнера с проектом. 
Оберните в Docker Compose Django-проект с БД PostgreSQL, Redis и Celery. Проект запускается одной командой docker-compose up -d --build 
в ходе которой создаются контейнеры Django, PostrgeSQL, Redis, Celery, Celery-beat, образы к ним и автоматический запуск приложения 
Django и всех других конейнеров необходимых для успешной работы сервиса. Таким образом проект готов для доставки на удаленный сервер.

3.Работа с приложением. Работа с приложением в варианте с контейнером ничем отличется от использования в локальном аврианте. 
Перед началом работаты с контейнером остановите службу PostgeSQL на локальном компьютере.
Подключаемся к контейнеру app-1 (http://127.0.0.1:8000/) и управление данными выполняется через приложение Postman. 
Перед запуском контейнера app-1 позаботьтесь о запуске контейнеров postgres-1 и redis-1. Контейнеры celery-1 и celery-beat-1, 
если они не остановлены, можно запустить после ввода курсов, уроков, и расписания