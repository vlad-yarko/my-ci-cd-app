from locust import HttpUser, task, between


class BackendUser(HttpUser):
    wait_time = between(2, 10)
    
    @task
    def load_root_page(self):
        # self.client.get("/")
        self.client.get("/api/requests")
