# Deepfake_recognition_method_in_video

## Описание

Система представляет собой комплексное решение для обнаружения и распознавания поддельных видео (deepfake) и состоит из следующих основных компонентов:

1. Модуль загрузки и обработки видео:
   - Пользователи могут загружать видео файлы в систему для анализа.
   - Система использует алгоритмы машинного обучения и компьютерного зрения для определения наличия deepfake в загруженных видео.
   - Результаты анализа отображаются в удобном для пользователя формате, включая информацию о наличии/отсутствии deepfake и вероятность его присутствия.

2. Система аутентификации и управления пользователями:
   - Пользователи могут зарегистрироваться и войти в систему.
   - Система сохраняет историю загруженных пользователем видео и результаты их анализа.

3. Модели распознавания deepfake:
   - Была разработана модель распознавания deepfake, которая анализирует аномалии в движении лиц.
   - Модель была обучена на собранном наборе данных.
   - Предобученная модель XceptionNet была дообучена на дополнительных данных для повышения точности распознавания.
   - Проведены сравнительные тесты оригинальной и дообученной моделей, чтобы выбрать наиболее эффективную.

Deepfake Detector использует передовые технологии машинного обучения для обнаружения поддельных медиа-файлов. Приложение предоставляет пользователям следующие возможности:

| Возможность | Описание |
| --- | --- |
| Загрузка видео для анализа | Пользователи могут загружать изображения и видео в систему для анализа на наличие deepfake. |
| Просмотр профиля пользователя и истории анализа | Пользователи могут просматривать свой профиль, включая историю загруженных и проанализированных медиа-файлов. |
| Подробный анализ обнаруженных deepfake-элементов | Система предоставляет детальный отчет об обнаруженных deepfake-элементах в загруженных медиа-файлах, включая вероятность их присутствия. |
| Просмотр истории проанализированных видео | Пользователи могут просматривать историю всех ранее проанализированных видео, включая результаты анализа и вероятность наличия deepfake. |

## Установка

Для установки Deepfake Detector вам потребуется:

1. Убедиться, что у вас установлены Python 3 (3.8).
2. Клонировать репозиторий.
3. Перейти в директорию проекта.
```
git clone https://github.com/veb-bet/Deepfake_recognition_method_in_video.git
cd Deepfake_recognition_method_in_video
```
4. Создать и активировать виртуальное окружение
```
# Windows
python -m venv dr-venv
dr-venv\Scripts\activate.bat
```
```
# Linux:
python -m venv dr-venv
source ./dr-venv/bin/activate
```
5. Установить зависимости.

Сначала установите setuptools:
```
pip install setuptools
```    
Затем установите остальные зависимости:
```
pip install -r requirements.txt
```
6. Запустить приложение.
```
python Main.py
```

Когда приложение запущено, вы можете перейти к вкладке "Анализ" и загрузить изображение или видео для анализа. Результаты анализа будут отображены на экране, а история анализа будет сохранена в базе данных.

## Дополнительно:

В репозитории есть директория с тестами первой модели /tests/. Вы можете использовать эти тесты для проверки работы первой модели.
Есть директория с графиками точностей, потерь и тетирования метрик моделей /graphics/.
Также есть набор видеофайлов для распознавания в приложении. (Ссылка для скачивания: https://drive.google.com/drive/folders/1GAcI5ZW4o_jl1gxjtrc1TKhnDmZJkR3S?usp=sharing)

<details>
<summary>Диаграммы и схемы</summary>
   
### Диаграммы бизнес-процессов системы распознавания:
![444](https://github.com/veb-bet/Deepfake_recognition_method_in_video/assets/73333734/c4c46078-f08c-4626-a572-786a211e10a7)
![333](https://github.com/veb-bet/Deepfake_recognition_method_in_video/assets/73333734/ae60e632-e9db-472d-bb09-51acac239efa)

### Диаграмма классов:
![1](https://github.com/veb-bet/Deepfake_recognition_method_in_video/assets/73333734/b0788a74-873f-45c4-9006-7c96b2f95b7c)

### Струкрута базы данных:
![2](https://github.com/veb-bet/Deepfake_recognition_method_in_video/assets/73333734/eede3e94-4528-42f4-afd9-c4af26764bd8)

### Структурная схема
![Рисунок1](https://github.com/veb-bet/Deepfake_recognition_method_in_video/assets/73333734/8031e7d8-8cc5-43e8-a715-2382c6e9a004)

</details>

<details>
<summary>Работа приложения</summary>


https://github.com/veb-bet/Deepfake_recognition_method_in_video/assets/73333734/43510ffa-3c8b-4e28-a192-b21fd3464749


   
</details>
