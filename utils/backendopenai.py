import requests
import json


class BackendOpenAI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1/"

    def create_thread(self):
        print(self.api_key, self.base_url + 'threads')
        headers = {
            "Content-Type": "application/json",
            "OpenAI-Beta": "assistants=v2",
            "Authorization": f"Bearer {self.api_key}"
        }
        data_payload = json.dumps({
            "metadata": {
                "action": "False"
            }
        })
        response = requests.post(
            self.base_url + 'threads', headers=headers, data=data_payload)
        print(response, response.status_code)
        return response.json()

    def get_thread(self, thread_id):
        headers = {
            "Content-Type": "application/json",
            "OpenAI-Beta": "assistants=v2",
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.get(
            self.base_url + f'threads/{thread_id}', headers=headers)
        return response.json()

    def modify_thread(self, thread_id):
        headers = {
            "Content-Type": "application/json",
            "OpenAI-Beta": "assistants=v2",
            "Authorization": f"Bearer {self.api_key}"
        }
        data_payload = json.dumps({
            "metadata": {
                "action": "False"
            }
        })
        response = requests.post(
            self.base_url + f'threads/{thread_id}/messages', headers=headers, data=data_payload)
        print(response.json())
        return response.json()

    def delete_thread(self, thread_id):
        headers = {
            "Content-Type": "application/json",
            "OpenAI-Beta": "assistants=v2",
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.delete(
            self.base_url + f'threads/{thread_id}', headers=headers)
        print(response.json())
        return response.json()
