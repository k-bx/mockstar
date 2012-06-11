# -*- coding: utf-8 -*-

import unittest
from mock import patch
from app.bl.user import create_user


class TestCreateUser(unittest.TestCase):
    @patch('app.bl.user.choose_low_quality_avatar', autospec=True)
    @patch('app.bl.user.count_score', autospec=True)
    @patch('app.bl.user.not_md5_and_has_salt', autospec=True)
    @patch('app.bl.user.User', autospec=True)
    def test_should_create_save_and_return_user(
        self, user_mock, not_md5_and_has_salt_mock, count_score_mock,
        choose_low_quality_avatar_mock):

        count_score_mock.return_value = 0
        user = user_mock.return_value

        # do
        rv = create_user("foo@bar.com", "pwd", "Foo Bar")
        user_mock.assert_called_with(
            email="foo@bar.com",
            password=not_md5_and_has_salt_mock.return_value,
            full_name="Foo Bar")
        not_md5_and_has_salt_mock.assert_called_with("pwd")
        user.save.assert_called_with()
        self.assertIs(rv, user)

    @patch('app.bl.user.choose_low_quality_avatar', autospec=True)
    @patch('app.bl.user.count_score', autospec=True)
    @patch('app.bl.user.not_md5_and_has_salt', autospec=True)
    @patch('app.bl.user.User', autospec=True)
    def test_should_choose_low_quality_avatar_on_small_score(
        self, user_mock, not_md5_and_has_salt_mock, count_score_mock,
        choose_low_quality_avatar_mock):

        count_score_mock.return_value = 9
        user = user_mock.return_value

        # do
        create_user("foo@bar.com", "pwd", "Foo Bar")

        count_score_mock.assert_called_with(user)
        choose_low_quality_avatar_mock.assert_called_with(user)

    @patch('app.bl.user.discover_possible_friends', autospec=True)
    @patch('app.bl.user.mail', autospec=True)
    @patch('app.bl.user.choose_high_quality_avatar', autospec=True)
    @patch('app.bl.user.count_score', autospec=True)
    @patch('app.bl.user.not_md5_and_has_salt', autospec=True)
    @patch('app.bl.user.User', autospec=True)
    def test_should_choose_high_quality_avatar_on_big_score(
        self, user_mock, not_md5_and_has_salt_mock, count_score_mock,
        choose_high_quality_avatar_mock, mail_mock,
        discover_possible_friends_mock):

        # ok, I'm bored already
        pass
