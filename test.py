from requests import get, post, delete

print(get('http://localhost:8080/api/v2/users').json())
print(get('http://localhost:8080/api/v2/users/1').json())
print(get('http://localhost:8080/api/v2/users/148').json())

data = {'surname': 'Zyranov1', 'name': 'Vitalik', 'age': 16, 'position': 'human', 'speciality': 'human',
        'address': 'dom', 'email': 'vit5@lik.zyr', 'password': 'Vitlik'}

print(post('http://localhost:8080/api/v2/users', data=data).json())
print(post('http://localhost:8080/api/v2/users', data=data).json())


print(delete('http://localhost:8080/api/v2/users/10', data=data).json())
print(delete('http://localhost:8080/api/v2/users/10', data=data).json())
