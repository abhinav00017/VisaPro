import json

class Records:
    def __init__(self):
        pass
    
    def create_record(self, record):
        try:
            with open('database.txt', 'r') as file:
                try:
                    data = json.load(file)
                except:
                    data = {}

                key = list(record.keys())[0]
                value = json.dumps(list(record.values())[0])  # Convert dict to string

                if data.get(key):
                    # Convert each dict in the list to a string before checking
                    if value not in [json.dumps(d) for d in data[key]]:
                        data[key].append(json.loads(value))  # Convert string back to dict
                else:
                    data[key] = [json.loads(value)]  # Convert string back to dict

            with open('database.txt', 'w') as file:
                json.dump(data, file)
                
            return True
        except Exception as e:
            return e

    
    def retrieve_record(self, email_id):
        with open('database.txt', 'r') as file:
            record = json.load(file)
            
            if record.get(email_id):
                return list(record[email_id])
            else:
                return "Record not found"

    
    
# rec = Records()

# print(rec.create_record({'abhinavch53@gmail.com': {'id': 'thread_TTmAMxdsf9STVBdfdrfdjWvuuzXvehlOtxcvx', 'object': 'thread', 'created_at': 1718038918, 'metadata': {'action': 'False'}, 'tool_resources': {}}}))
# # print(rec.retrieve_record('abhinavch53@gmail.com'))

