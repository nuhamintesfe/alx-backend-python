#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get and set fixture side_effects."""
        cls.get_patcher = patch('requests.get')

        # Start patching
        cls.mock_get = cls.get_patcher.start()

        # Mock responses for each URL based on what the client requests
        cls.mock_get.side_effect = cls.mocked_requests_get

    @classmethod
    def tearDownClass(cls):
        """Stop patcher."""
        cls.get_patcher.stop()

    @staticmethod
    def mocked_requests_get(url):
        """Mock requests.get(url).json() with appropriate payload."""
        class MockResponse:
            def __init__(self, json_data):
                self._json_data = json_data

            def json(self):
                return self._json_data

        if url == "https://api.github.com/orgs/test-org":
            return MockResponse(org_payload)
        elif url == org_payload["repos_url"]:
            return MockResponse(repos_payload)
        return MockResponse(None)

    def test_public_repos(self):
        """Test that public_repos returns expected repo names."""
        client = GithubOrgClient("test-org")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test that public_repos with license returns only apache2 repos."""
        client = GithubOrgClient("test-org")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
