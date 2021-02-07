data = [
 {
   "id_number": "SA4784",
   "name": "Mark",
   "birthdate": None
 },
 {
   "id_number": "V410Z8",
   "name": "Vincent",
   "birthdate": "15/02/1989"
 },
 {
   "id_number": "CZ1094",
   "name": "Paul",
   "birthdate": "27/09/1994"
 }
]

for i in data:
    if i['id_number'] == 'V410Z8':
        print(i['birthdate'])
        print(i['name'])
        break