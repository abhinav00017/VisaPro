import json

class Records:
    def __init__(self):
        pass
    
    # def check_record(self, email_id):
    #     with open('database.txt', 'r') as file:
    #         record = json.load(file)
            
    #         if record.get(email_id):
    #             return list(record[email_id])
    #         else:
    #             return "None"
        
    def create_record(self, record):
        try:
            with open('database.txt', 'r') as file:
                try:
                    data = json.load(file)
                except:
                    data = {}

                key = list(record.keys())[0]
                value = list(record.values())[0] 
                if data.get(key):
                    return False
                    if value not in [json.dumps(d) for d in data[key]]:
                        data[key]['threads'].append(json.loads(value))  
                else:
                    data[key] = {"country":value['country'], "user_name": value["user_name"],'threads':value['threads']}
            with open('database.txt', 'w') as file:
                json.dump(data, file)
                
            return True
        except Exception as e:
            return e

    
    def retrieve_record(self, email_id):
        with open('database.txt', 'r') as file:
            try:
                data = json.load(file)
            except:
                return "None"
            
            record = data
            
            if record.get(email_id):
                return record[email_id]
            else:
                return "None"
            
    def update_record(self, record):
        try:
            with open('database.txt', 'r') as file:
                data = json.load(file)
                data[list(record.keys())[0]] = list(record.values())[0]
            with open('database.txt', 'w') as file:
                json.dump(data, file)
            return True
        except Exception as e:
            return e

    
    
# rec = Records()

# print(rec.create_record({'abhinavch534@gmail.com': {
#     'userid':'abhinav1234',
#     'country':'india',
#     'threads':{'id': 'thread_TTmAMxdsf9STVBdfdrfdjWvuuzXvehlOtxcvx', 'object': 'thread', 'created_at': 1718038918, 'metadata': {'action': 'False'}, 'tool_resources': {}}}}))

# print(rec.retrieve_record('abhinavch53@gmail.com'))

# print(rec.update_record({'abhinavch53@gmail.com': {
#     'userid':'abhinav1234',
#     'country':'india',
#     'threads':{'id': 'thread_TTmAMxdsf9STVBdfdrfdjWvuuzXvehlOtxcvx', 'object': 'thread', 'created_at': 1718038918, 'metadata': {'action': 'False'}, 'tool_resources': {}}}}))

