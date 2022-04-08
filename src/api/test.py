from datetime import datetime
import requests

printSep = lambda: print("----------------")


def test1():
    print(requests.get('http://localhost:5000/api/jobs').json())
    printSep()

    print(requests.get('http://localhost:5000/api/jobs/1').json())
    printSep()

    print(requests.get('http://localhost:5000/api/jobs/100').json())
    printSep()

    print(requests.get('http://localhost:5000/api/jobs/first').json())
    printSep()


def test2():
    # Нет json данных
    print(requests.post('http://localhost:5000/api/jobs').json())
    printSep()

    # Не все поля присутствуют
    print(requests.post('http://localhost:5000/api/jobs',
            json={'job': 'Работа'}).json())
    printSep()

    # Запись с таким id уже существует
    print(requests.post('http://localhost:5000/api/jobs',
                        json={
                            "id": 1,
                            "team_leader": 1,
                            "job": "Помыть полы",
                            "work_size": 1,
                            "collaborators": "2, 3, 4, 5",
                            "start_date": datetime.now().isoformat(),
                            "end_date": datetime.now().isoformat(),
                            "is_finished": False,
                        }).json())
    printSep()

    # Всё правильно
    print(requests.post('http://localhost:5000/api/jobs',
                        json={
                            "id": 30,
                            "team_leader": 1,
                            "job": "Помыть полы",
                            "work_size": 1,
                            "collaborators": "2, 3, 4, 5",
                            "start_date": datetime.now().isoformat(),
                            "end_date": datetime.now().isoformat(),
                            "is_finished": False,
                        }).json())
    printSep()

    print(requests.get('http://localhost:5000/api/jobs').json())
    printSep()


def test3():
    print(requests.delete('http://localhost:5000/api/jobs/100').json())
    printSep()

    print(requests.delete('http://localhost:5000/api/jobs/second').json())
    printSep()

    print(requests.delete('http://localhost:5000/api/jobs/30').json())
    printSep()

    print(requests.get('http://localhost:5000/api/jobs').json())
    printSep()


def test4():
    print(requests.put('http://localhost:5000/api/jobs/100').json())
    printSep()

    print(requests.put('http://localhost:5000/api/jobs/second').json())
    printSep()

    print(requests.put('http://localhost:5000/api/jobs/30',
                        json={
                            "team_leader": 3,
                            "work_size": 2,
                            "collaborators": "2, 5",
                            "is_finished": True,
                        }).json())
    printSep()

    print(requests.get('http://localhost:5000/api/jobs/30').json())
    printSep()

    print(requests.put('http://localhost:5000/api/jobs/30',
                        json={
                            "team_leader": 30,
                        }).json())
    printSep()

    print(requests.get('http://localhost:5000/api/jobs/30').json())
    printSep()

    print(requests.put('http://localhost:5000/api/jobs/30',
                        json={
                            "team_leader": 1,
                            "job": "Помыть полы начисто",
                            "work_size": 20,
                            "collaborators": "2, 3, 4, 5, 6, 7, 8",
                            "start_date": datetime.now().isoformat(),
                            "end_date": datetime.now().isoformat(),
                            "is_finished": False,
                        }).json())

    print(requests.get('http://localhost:5000/api/jobs/30').json())
    printSep()


# test4()
# print(requests.post('http://localhost:5000/api/login',
#                     json={
#                         "email": "scott_chief@mars.org",
#                         "password": "123",
#                     }).json())
# print(requests.post('http://localhost:5000/api/jobs',
#                     json={
#                         "id": 1,
#                         "team_leader": 1,
#                         "job": "Помыть полы",
#                         "work_size": 1,
#                         "collaborators": "2, 3, 4, 5",
#                         "start_date": datetime.now().isoformat(),
#                         "end_date": datetime.now().isoformat(),
#                         "is_finished": False,
#                     }, headers={
#                         "Authorization" : "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NDY3MzI4NjksImlhdCI6MTY0NjcyOTI2OSwibmJmIjoxNjQ2NzI5MjY5LCJzdWIiOjF9.10TCBgoybzY4KgIS2Q_saFUdzQY1hvvwxyZp8c1XyKQ"
#                     }).json())
print(requests.put('http://localhost:5000/api/v2/users/1', json={
    "age": 1,
}).json())