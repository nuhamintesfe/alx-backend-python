#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized_class
from client import GithubOrgClient

@parameterized_class(
    ("org_name",),
    [
        ("google",),
        ("abc",),
    ]
)
class TestGithubOrgClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # patch requests.get for the entire test class
        cls.get_patcher = patch('requests.get')
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        # stop patching requests.get
        cls.get_patcher.stop()

    def test_org(self):
        with patch("client.get_json") as mock_get_json:
            mock_get_json.return_value = {"login": self.org_name}
            client = GithubOrgClient(self.org_name)
            self.assertEqual(client.org, {"login": self.org_name})
            mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{self.org_name}")

    def test_public_repos_url(self):
        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": f"https://api.github.com/orgs/{self.org_name}/repos"}
            client = GithubOrgClient(self.org_name)
            self.assertEqual(client._public_repos_url, f"https://api.github.com/orgs/{self.org_name}/repos")

    def test_public_repos(self):
        with patch("client.get_json") as mock_get_json, \
             patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "mock_url"
            mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]
            client = GithubOrgClient(self.org_name)
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])
            mock_get_json.assert_called_once_with("mock_url")

    def test_has_license(self):
        test_cases = [
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False),
            ({}, "my_license", False),
        ]
        client = GithubOrgClient(self.org_name)
        for repo, license_key, expected in test_cases:
            self.assertEqual(client.has_license(repo, license_key), expected)
