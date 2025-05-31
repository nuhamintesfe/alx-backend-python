#!/usr/bin/env python3
"""
Integration tests for GithubOrgClient.public_repos
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized_class
from client import GithubOrgClient

# FIX: Make sure this matches your project structure
try:
    from fixtures import org_payload, repos_payload, expected_repos, apache2_repos
except ImportError as e:
    raise ImportError(f"Could not import from fixtures.py. Error: {e}")
    

@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests using mocked requests and fixtures"""

    @classmethod
    def setUpClass(cls):
        """Patch requests.get with a side_effect function"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            if url == "https://api.github.com/orgs/google":
                mock_response = Mock()
                mock_response.json.return_value = cls.org_payload
                return mock_response
            elif url == cls.org_payload.get("repos_url"):
                mock_response = Mock()
                mock_response.json.return_value = cls.repos_payload
                return mock_response
            return Mock(json=lambda: {})

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher"""
        cls.get_patcher.stop()

    @patch("requests.get")
    def test_public_repos(self, mock_get):
        """Test public_repos returns expected repos (with patch)"""
        mock_get.return_value.json.side_effect = [
            self.org_payload,
            self.repos_payload
        ]
        client = GithubOrgClient("google")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test filtering by license"""
        client = GithubOrgClient("google")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)
