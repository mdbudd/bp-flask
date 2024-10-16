import json
import unittest

from main import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_awesome(self):
        # response = self.client.post("/", data={"content": "hello world"})
        response = self.client.get("/awesome")
        assert response.status_code == 200

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data["message"], "My First Awesome API")


if __name__ == "__main__":
    unittest.main()
