# -*- coding: utf-8 -*-

from mockstar import BaseTestCase
from mockstar import prefixed_p
from app.bl.user import create_user

ppatch = prefixed_p('app.bl.user', autospec=True)


class TestCreateUser(BaseTestCase):
    @ppatch('discover_possible_friends')
    @ppatch('mail')
    @ppatch('choose_high_quality_avatar')
    @ppatch('choose_low_quality_avatar')
    @ppatch('count_score')
    @ppatch('not_md5_and_has_salt')
    @ppatch('User')
    def side_effects(self, se):
        se.user = se.User.return_value
        se.secure_pwd = se.not_md5_and_has_salt.return_value
        se.score = se.count_score.return_value
        return self.invoke(se)

    def test_should_create_save_and_return_user(self, se):
        # do
        rv = create_user("foo@bar.com", "pwd", "Foo Bar")

        se.User.assert_called_with(
            email="foo@bar.com",
            password=se.secure_pwd,
            full_name="Foo Bar")
        se.not_md5_and_has_salt.assert_called_with("pwd")
        self.assertIs(rv, se.user)

    def test_should_choose_low_quality_avatar_on_small_score(self, se):
        se.count_score.return_value = 9

        # do
        create_user("foo@bar.com", "pwd", "Foo Bar")

        se.count_score.assert_called_with(se.user)
        se.choose_low_quality_avatar.assert_called_with(se.user)

    def test_should_choose_high_quality_avatar_on_big_score(self, se):
        se.count_score.return_value = 11

        # do
        create_user("foo@bar.com", "pwd", "Foo Bar")

        se.choose_high_quality_avatar.assert_called_with(se.user)

    # I'm not so bored now :)
