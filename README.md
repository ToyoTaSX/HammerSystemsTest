# Описание API
## Основные роуты
```localhost:8000/``` - главная страница / профиль<br>
```localhost:8000/login``` - страница логина<br>
```localhost:8000/users/profile``` - получение данных профиля<br>
```localhost:8000/users/invite-code``` - ввод инфайт-кода<br>
```localhost:8000/auth/send-code``` - отправка номера телефона для получения кода<br>
```localhost:8000/verification-code``` - отправка кода подтверждения для авторизации<br>



## localhost:8000/
Защищенный запрос, требует авторизации, возвращает страницу с профилем пользователя
#### request
```GET``` - тип запроса<br>
```Authorization``` - Bearer-токен в заголовке или в coockies<br>
#### response
```HTML``` - тип ответа
```200``` - статус-код ответа
![image](https://github.com/user-attachments/assets/ac981928-1b31-4a5f-9691-6dc2b4b325c4)



## localhost:8000/login
Страница авторизации
#### request
```GET``` - тип запроса<br>
```Authorization``` - не требуется
#### response
```HTML``` - тип ответа
```200``` - статус-код ответа
![image](https://github.com/user-attachments/assets/8b847f90-0969-4789-b06e-3a4c36eff2b7)
![image](https://github.com/user-attachments/assets/ede7de50-134a-4907-b755-74240df73ba6)
![image](https://github.com/user-attachments/assets/acde482e-2512-401d-9006-91184d9493f8)





## localhost:8000/users/profile
Получение данных о своем пользователе
#### request
```GET``` - тип запроса<br>
```Authorization``` - Bearer-токен в заголовке или в coockies<br>
#### response
```JSON``` - тип ответа
```200``` - статус-код ответа
```
Пример ответа
{
    "your_number": "+79900759910", #Номер телефона
    "your_code": "9vzi13",         #Инвайт-код
    "activated_code": null,        #Введенный инфайт-код
    "referals_numbers": []         #Список номеров людей, которые уже ввели ваш инфайт-код
}
```



## localhost:8000/users/invite-code
Ввод чужого инвайт-кода
#### request
```POST``` - тип запроса<br>
```Authorization``` - Bearer-токен в заголовке или в coockies<br>
```
Пример запроса
Request body:
{
    "invite_code": "5d7K3D" 
}
```
#### response
```JSON``` - тип ответа
```200``` - статус-код ответа
```
Пример ответа
{
    "message": "Код успешно применен"
}
В случае неверного инвайт-кода возвращает ошибку
```



## localhost:8000/auth/send-code
Отправка номера телефона, генерация кода подтверждения на сервере, задержка несколько секунд, возврат кода подтверждения (заглушка вместо отправки смс)
#### request
```POST``` - тип запроса<br>
```Authorization``` - не требуется
```
Пример запроса
Request body:
{
    "number": "+79080474120" 
}
```
#### response
```JSON``` - тип ответа
```200``` - статус-код ответа
```
Пример ответа
{
    "message": "Код подтверждения отправлен (заглушка).",
    "code": "2130"
}
В случае невалидного номера возвращает ошибку
```



## localhost:8000/auth/verification-code
Отправка номера телефона и кода подтверждения, получение auth и refresh токенов, установка coockies для авторизации
#### request
```POST``` - тип запроса<br>
```Authorization``` - не требуется
```
Пример запроса
Request body:
{
    "number": "+79080474120",
    "code": "3243" 
}
```
#### response
```JSON``` - тип ответа
```200``` - статус-код ответа
```
Пример ответа
{
    "message": "Успешный вход.",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMzMTgwNTAyLCJpYXQiOjE3MzMwOTQxMDIsImp0aSI6IjRkMDQ4Yjk5Zjk4ODQ2NzlhYjVhZmEwYmZjNzI2ZmNhIiwidXNlcl9pZCI6MTl9.K1opgPkPVjclrXi1fawnn2QH5P7DvZwW647l2WPc4ZQ",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMzE4MDUwMiwiaWF0IjoxNzMzMDk0MTAyLCJqdGkiOiJiZGI1Mzg2MzZlNzk0NWY5YmVmYTBjYzFhZTYzZTI3OSIsInVzZXJfaWQiOjE5fQ.H2E6RBfpLuVH8MtcZJn-2aj8iChke9T0OFApvpwPLpA"
}
В случае неверного кода возвращает ошибку
```

# Тесты
## Запускать папку Tests, порядок не менять, снять галочки на сохранение coockies и переменных коллекции, иначе при повторном запуске тесты на неавторизованный доуступ не пройдут
![image](https://github.com/user-attachments/assets/7a2a4512-1752-4e7f-8192-284ff34b9790)

