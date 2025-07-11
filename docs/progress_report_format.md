# Формат файла "Отчёт об успеваемости и посещаемости ученика"

Этот документ описывает ожидаемое расположение данных в XLSX-файле, который
импортируется командой `progress_report`.

## Общий вид таблицы

Файл создаётся выгрузкой из электронного журнала и содержит одну или несколько
таблиц. Каждая таблица начинается строкой `Ученик: <ФИО>` и имеет следующую
структуру:

1. Перед таблицей могут находиться строки вида `Учебный год: 2024/2025`,
   `Класс: 8А` и `Период: с 01.09.2024 по 24.05.2025`.
2. Первая строка таблицы содержит заголовок `Предмет`, а далее названия
   месяцев (например, "сентябрь", "октябрь" и т.д.).
3. Под строкой месяцев идёт строка с номерами дней месяца.
4. Ниже располагаются строки предметов. В ячейках могут встречаться оценки и
   обозначения посещаемости (`Н`, `Б`, `У`, `О`). Допускается несколько
   значений через `/`, например `5/Н`.

## Расчёт дат занятий

Дата занятия вычисляется по столбцу месяца и номеру дня. Если месяц указан с
сентября по декабрь, используется первый год из строки "Учебный год".
Январь–август относятся ко второму году. Таким образом формируется полная дата
урока, применяемая как `lesson_date`.

Также из даты выводятся параметры четверти: сентябрь–октябрь дают `quarter` 1,
ноябрь–декабрь — `quarter` 2, январь–март — `quarter` 3, апрель–май — `quarter`
4. Для остальных месяцев используется `year` с индексом 1.

## Поля `grade_kind`, `term_type` и `term_index`

- `grade_kind` — тип оценки. Для строк отчёта всегда используется значение
  `regular`.
- `term_type` — тип учебного периода (например, `quarter`, `trimester`,
  `semester`, `year`).
- `term_index` — порядковый номер периода, определяемый по дате урока.

## Импорт через CLI

Пример запуска импорта отчёта:

```bash
python app/cli.py import progress_report FILE.xlsx
```

После выполнения будет создан сводный отчёт о добавленных и изменённых данных.
