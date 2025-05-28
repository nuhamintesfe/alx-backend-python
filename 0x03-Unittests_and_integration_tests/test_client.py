#!/usr/bin/env python3
"""
Integration test for GithubOrgClient.public_repos
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
        "somevalue": 42
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient using fixtures."""

    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get and define side_effect"""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def side_effect(url):
            mock_response = Mock()
            if url == "https://api.github.com/orgs/test-org":
                mock_response.json.return_value = cls.org_payload
            elif url == "https://api.github.com/orgs/test-org/repos":
                mock_response.json.return_value = cls.repos_payload
            return mock_response

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected list of repos"""
        client = GithubOrgClient("test-org")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos returns repos filtered by license"""
        client = GithubOrgClient("test-org")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )

    def test_n(self):
        """Dummy test to validate parameterized_class usage"""
        self.assertEqual(self.somevalue, 42)
