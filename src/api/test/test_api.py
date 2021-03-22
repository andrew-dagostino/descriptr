"""Test Descriptr JSON API."""

from apipkg import create_app
import flask_unittest
import os


""" Change working directory to one level above here """
os.chdir(os.path.dirname(os.path.dirname(__file__)))


class TestDescriptrApi(flask_unittest.ClientTestCase):
    """A unittest class whose "test_*" methods will be called."""
    app = create_app()

    def test_root(self, client):
        """Test that the root endpoint returns the correct response."""
        ret = client.get("/")
        self.assertIn('available_endpoints', ret.json)
        self.assertIn('/search', ret.json["available_endpoints"])

    def test_search_get(self, client):
        """Test that the root endpoint returns the correct response."""
        ret = client.get("/search")
        self.assertIn('available_filters', ret.json)
        self.assertNotEqual(len(ret.json["available_filters"]), 0)

    def test_search_post_simple(self, client):
        """Test POSTing a simple search and getting correct response."""
        ret = client.post("/search", json=dict(number=dict(query="2750", comparison='=')))
        ret_json = ret.get_json()
        self.assertIn('courses', ret_json)
        self.assertGreater(len(ret_json["courses"]), 0)

    def test_search_post_complex(self, client):
        """Test POSTing a complex search and getting correct response."""
        ret = client.post("/search", json=dict(code=dict(query='cis', comparison='='), level=dict(query="1", comparison='=')))
        ret_json = ret.get_json()
        self.assertIn('courses', ret_json)
        self.assertGreater(len(ret.json["courses"]), 0)