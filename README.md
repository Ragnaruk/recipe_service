# Рецепты
Веб-сервер, получающий на вход виды и количество ингредиентов, а отдающий список блюд, которые можно из них приготовить.

## Эндпоинты
* `GET /` - Страница с ссылками на другие эндпоинты.

Вид страницы:
```html
POST /recipes/possible
GET /recipes/last
GET /components/popular
```

* `POST /recipes/possible` - Получение списка рецептов, которые можно приготовить из ингредиентов.

Получает и возвращает данные в формате JSON.

Пример получаемых данных.
```json
{
    "мясо": 200,
    "огурец": 1,
    "картофель": 10
}
```

Пример возвращаемых данных.
```json
[
    {"name": "Салат «Русский»", "quantity": 0.5},
    {"name": "Салат «Ленинградский»", "quantity": 0.4}
]
```

* `GET /recipes/last` - Получение списка рецептов, рекомендованных за последний час.

Пример возвращаемых данных.
```json
{
    "last_recommended_recipes": ["Салат «Ленинградский»", "Салат «Русский»"]
}
```

* `GET /components/popular` - Получение списка самых популярных ингредиентов у клиентов.

Пример возвращаемых данных.
```json
{
    "most_popular_components": [
        {"огурец": 1},
        {"мясо": 1},
        {"картофель": 1},
        {"яйцо": 0},
        {"рыба": 0}
    ]
}
```

## Задание
Иван любит готовить. У него есть ингредиенты в холодильнике и книга рецептов. К сожалению, он плохо разбирается в математике. Напишите сервис, который подсчитает сколько рецептов он может приготовить с учетом того, что есть холодильнике.На вход сервису отправляем то, что у нас находится в холодильнике. Формат и способ отправки на ваше усмотрение. На выходе должно быть что и в каких количествах можно приготовить, если бы готовили только этот вид рецепта.Для простоты для количеств ингредиентов нет единиц  (например, 1 кг муки или 200 г сахара просто 1 или 200). Ингредиенты, которых нет в рецептах, не требуются.Книга рецептов в json формате: https://yadi.sk/d/mJP0GMUzgZaCAw Состоит из множества рецептов и компонент с количествами. Также сервис должен предоставлять возможность:

* получения списка рецептов, которые были рекомендованы пользователям за последний час.
* получения топ 10 популярных (наиболее часто встречающихся) продуктов в холодильнике пользователя

### Примечание к заданию:
- [X] Написать тесты
- [X]  Сделать логирование 
- [X]  Написать Dockerfile
- [X]  Без использования Django
- [ ]  Обосновать необходимость применения тех или иных технологий
- [X]  Использование асинхронных фреймворков будет плюсом (если дадут преимущество, зависит от вашей реализации)