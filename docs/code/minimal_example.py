import unittest
from mockstar import prefixed_p
from sample_app.blog import forms

ppatch = prefixed_p("sample_app.blog.forms")  # module under test


class TestPostForm(unittest.TestCase):
    @ppatch('is_post_exist')     # list / describe side-effects
    def side_effects(self, se):
        se.is_post_exist.return_value = False  # default side-effects behavior
        return self.invoke(se)

    def test_should_be_valid_for_simple_data(self, se):
        form = forms.PostForm({'title': 'foo', 'content': 'bar'})

        self.assertTrue(form.is_valid())

    def test_should_get_error_on_existing_post_title(self, se):
        se.is_post_exist.return_value = True
        form = forms.PostForm({'title': 'foo', 'content': 'bar'})

        self.assertFalse(form.is_valid())
        self.assertEquals(dict(form.errors),
                          ["Post with this title already exists"])
