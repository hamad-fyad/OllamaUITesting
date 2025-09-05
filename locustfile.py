from locust import HttpUser,task

class helloworld(HttpUser):
    @task
    def hello(self):
        self.client.get("/")