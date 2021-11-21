# Задание 1
```mysql
SELECT 
    c.id,
    CONCAT(first_name, " ", last_name) AS name,
    ANY_VALUE(category) AS category,  # COUNT(DISTINCT category) = 1 so it's determined
    GROUP_CONCAT(product SEPARATOR ", ") AS products
FROM clients AS c 
INNER JOIN client_orders AS co 
    ON c.id = co.client_id 
INNER JOIN orders AS o 
    ON o.id = co.order_id 
WHERE 18 <= c.age AND c.age <= 65 
GROUP BY c.id
HAVING COUNT(product) = 2 AND COUNT(DISTINCT category) = 1
```

# Задание 2
## Запуск
Для запуска потребуется docker-compose. Запустите:
```
docker-compose up --build -d
```
Сервис будет доступен по адресу `http://localhost:80/`

## Краткое описание
Методы реализованы в соответствии с ТЗ. Реализованы методы `profile` и `likes`.
Информация собирается без авторизации в VK.

Для сбора информации используется как десктопная, так и мобильная версия VK.
Это связязано с тем, что в мобильной количество подписчиков указывается точно (без округления до тысяч К и миллионов М), но нет гарантии получить `id` пользователя кроме его `username`.
Используется только англоязычная версия VK (запрашиваемый язык указывается с помощью `cookies`).

Метод `posts` реализовать не успел. Если бы было время, реализовал бы так:

Собрал бы страницу `m.vk.com/<username>?offset=N`, где `N` - количество постов, запрашиваемых у VK.
Далее бы выделял оттуда `div` с постами и парсил статистику, используя готовые методы модуля `VKPostParser` - теги те же,
что и на странице одного поста. Кроме `post_id` и `url`, для этого нужно пара других методов. Сама информация есть в 
атрибутах `div`, который содержит пост.

## Лимитирование запросов
Для ограничения в один одновременный запрос от одного IP
создан абстрактный класс `BaseBlocklist`. Перед выполнением запроса проверяем IP в блоклисте.
Если есть - отдаём ошибку. Если нет - добавляем, обрабатываем запрос, удаляем.

Имплементация этого абстрактного
класса сделана с помощью встроенного типа `set`, так что храним
адреса просто в памяти.

Из-за этого блоклист локален для каждого воркера, и ограничение работает 
корректно только при одном запущенном воркере. По-хорошему надо
реализовать блоклист в стороннем хранилище типа `Redis`.
На это не хватило немного времени.
