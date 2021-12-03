# Тестовое задание
## Задание 1

### Задание: Необходимо вывести самую популярную категорию товаров

```sql
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS goods;
DROP TABLE IF EXISTS goods_type;
CREATE TABLE goods_type(
	goods_type_id INT GENERATED ALWAYS AS IDENTITY,
	goods_type_name VARCHAR(255) NOT NULL,
	PRIMARY KEY(goods_type_id));
CREATE TABLE goods(
	goods_id INT GENERATED ALWAYS AS IDENTITY,
	goods_name VARCHAR(255) NOT NULL,
	goods_type_id INT,
	PRIMARY KEY(goods_id),
	CONSTRAINT fk_goods FOREIGN KEY(goods_type_id) REFERENCES goods_type(goods_type_id));
CREATE TABLE orders(
	order_id INT GENERATED ALWAYS AS IDENTITY,
	user_name VARCHAR(255) NOT NULL,
	total INT,
	goods_id INT,
	PRIMARY KEY(order_id),
	CONSTRAINT fk_order FOREIGN KEY(goods_id) REFERENCES goods(goods_id));
INSERT INTO goods_type(goods_type_name) VALUES
	('vegetables'),
	('fruits'),
	('cookie');
INSERT INTO goods(goods_name, goods_type_id) VALUES
	('tomato',1),
	('potatoes',1),
	('banana',2),
	('orange',2),
	('oreo',3),
	('chocopie',3);
INSERT INTO orders(user_name, total, goods_id) VALUES
	('John',2,1),
	('John',1,3),
	('Jane',3,5),
	('Jane',3,6),
	('David',10,2),
	('David',5,5),
	('David',3,1),
	('Ann', 1,6);
```

### Решение:

```sql
SELECT goods_type.goods_type_name AS category
FROM orders, goods, goods_type
WHERE orders.goods_id = goods.goods_id AND goods.goods_type_id = goods_type.goods_type_id
GROUP BY goods_type.goods_type_name
ORDER BY SUM(total) DESC
LIMIT 1
```
Сделал группировку по `goods_type.goods_type_name`, в предположении, что, несмотря на отсутсвие ограничений, данные корректные, и значения поля `goods_type.goods_type_name` уникальны.


## Задание 2

### Задание: Найти изображения для которых есть метаданные (пары), и сформировать из них список для каждой папки.
Дан путь до дирректории в которой находятся папки и файлы. Внутри папок лежат изображения с расширением jpg, jpeg, png и методанные к ним с таким же именем, но с расширением json. Расширения могут быть написаны как строчными, так и заглавными буквами. Помимо перечисленных расширений могут быть и другие.
```python
import os
from glob import glob
labels_dir = "/tmp/labels"os.makedirs(labels_dir, exist_ok=True)
labels = {
    "label1": ["1image.JPG", "2.jpeg", "2.json", "1image.json", "3.jpg"],
    "label2": ["1.jpg", "1.json", "2.json", "3.json"],
    "label3": ["15.png", "15.json", "16.json", "16.jpg", "1.PNG", "1.JSON"],
    "label4": ["1.png", "1.txt", "2.txt", ],}
for label in labels:
    label_path = os.path.join(labels_dir, label)
    os.makedirs(label_path, exist_ok=True)
    for item in labels[label]:
        open(os.path.join(label_path, item), 'a').close()
    print(f"{label_path} {os.listdir(label_path)}")
open(os.path.join(labels_dir, "test.txt"), 'a').close()
```
Должен получиться следующий ответ:
```
[
    {"label1": [
        ['/tmp/labels/label1/2.jpeg', '/tmp/labels/label1/2.json'],
        ['/tmp/labels/label1/1image.JPG', '/tmp/labels/label1/1image.json']
    ]},
    {"label2": [['/tmp/labels/label2/1.jpg', '/tmp/labels/label2/1.json']]},
    {"label3" : [
        ['/tmp/labels/label3/1.PNG', '/tmp/labels/label3/1.JSON'],
        ['/tmp/labels/label3/16.jpg', '/tmp/labels/label3/16.json'],
        ['/tmp/labels/label3/15.png', '/tmp/labels/label3/15.json']
    ]}
]
```

### Решение:
Решение приведено в файле `get_list.py`.

| :exclamation:  Представленное решение подразумевает, что структура исследуемой дирректории неизвестна, и искомые пары (*изображение-метаданные*) могут находиться на любом уровне вложенности.  |
|:-----------------------------------------|

Скрипт для создания тестовых файлов находится в файле `create_dirs.py`.
