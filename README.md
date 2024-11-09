# AI-international-2024

Система классификации электрокортикограмм.

## Backend

Имеет эндпоинт для загрузки `edf` файлов.

`/upload`

Требует `form-data` `edf` файл.

Ответ:
```
{
    "file": "<ссылка на edf-файл>",
    "json": "<ссылка на json-файл с данными о каналах>"
}
```


Сам `json` с данными о каналх выглядит так:
```
{
    "FrL" : [0.5151,50,5132....],
    "FrR" : [0.5151,50,5132....],
    "OcR" : [0.5151,50,5132....],
    "classes: [0,0,0,1,1,1,0,0,0,3,3,3,3,0,0,0....]
}
```
Частота дискретизации - 400Гц.