#!/usr/bin/env python3
"""
Integration test for GithubOrgClient.public_repos
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized_class
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
    """Integration tests with fixtures"""

    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            if url == "https://api.github.com/orgs/google":
                mock_resp = Mock()
                mock_resp.json.return_value = cls.org_payload
                return mock_resp
            elif url == cls.org_payload.get("repos_url"):
                mock_resp = Mock()
                mock_resp.json.return_value = cls.repos_payload
                return mock_resp
            return Mock(json=lambda: {})

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )

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

    @parameterized.expand([
        ({"license": {"key": "apache-2.0"}}, "apache-2.0", True),
        ({"license": {"key": "mit"}}, "apache-2.0", False),
        ({}, "apache-2.0", False),
        ({"license": {}}, "apache-2.0", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test the has_license static method"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)

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
