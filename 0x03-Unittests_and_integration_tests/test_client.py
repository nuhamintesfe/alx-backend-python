#!/usr/bin/env python3
"""
Unit test for GithubOrgClient.public_repos
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected, mock_get_json):
        """Test org method"""
        mock_get_json.return_value = expected
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org(), expected)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test _public_repos_url property"""
        with patch.object(GithubOrgClient, 'org',
                          new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/test/repos"
            }
            client = GithubOrgClient("test")
            self.assertEqual(client._public_repos_url,
                             "https://api.github.com/orgs/test/repos")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos method output"""
        mock_get_json.side_effect = [
            {"repos_url": "https://api.github.com/orgs/google/repos"},
            [
                {"name": "repo1", "license": {"key": "apache-2.0"}},
                {"name": "repo2", "license": {"key": "mit"}},
                {"name": "repo3", "license": {"key": "apache-2.0"}}
            ]
        ]
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(),
                         ["repo1", "repo2", "repo3"])

    @patch('client.get_json')
    def test_public_repos_with_license(self, mock_get_json):
        """Test public_repos filtered by license"""
        mock_get_json.side_effect = [
            {"repos_url": "https://api.github.com/orgs/google/repos"},
            [
                {"name": "repo1", "license": {"key": "apache-2.0"}},
                {"name": "repo2", "license": {"key": "mit"}},
                {"name": "repo3", "license": {"key": "apache-2.0"}},
                {"name": "repo4", "license": {"key": "gpl"}}
            ]
        ]
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2.0"),
                         ["repo1", "repo3"])
