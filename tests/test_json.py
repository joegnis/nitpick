"""JSON tests."""
from tests.helpers import ProjectMock


def test_suggest_initial_contents(request):
    """Suggest initial contents for missing JSON file."""
    ProjectMock(request).load_styles("package-json").pyproject_toml(
        """
        [tool.nitpick]
        style = ["package-json"]
        """
    ).flake8().assert_errors_contain(
        """
        NIP341 File package.json was not found. Create it with this content:\x1b[32m
        {
          "name": "<some value here>",
          "release": {
            "plugins": "<some value here>"
          },
          "repository": {
            "type": "<some value here>",
            "url": "<some value here>"
          },
          "version": "<some value here>"
        }\x1b[0m
        """
    )


def test_json_file_contains_keys(request):
    """Test if JSON file contains keys."""
    ProjectMock(request).load_styles("package-json").pyproject_toml(
        """
        [tool.nitpick]
        style = ["package-json"]
        """
    ).save_file("package.json", '{"name": "myproject", "version": "0.0.1"}').flake8().assert_errors_contain(
        """
        NIP348 File package.json has missing keys:\x1b[32m
        {
          "release": {
            "plugins": "<some value here>"
          },
          "repository": {
            "type": "<some value here>",
            "url": "<some value here>"
          }
        }\x1b[0m
        """
    )


def test_missing_different_values(request):
    """Test missing and different values on the JSON file."""
    ProjectMock(request).style(
        '''
        [nitpick.JSONFile]
        file_names = ["my.json"]

        ["my.json".contains_json]
        "some.dotted.root.key" = """
            { "valid": "JSON", "content": ["should", "be", "here"] }
        """
        formatting = """ {"doesnt":"matter","here":true,"on the": "config file"} """
        '''
    ).save_file("my.json", '{"name":"myproject","formatting":{"on the":"actual file"}}').flake8().assert_errors_contain(
        """
        NIP348 File my.json has missing values:\x1b[32m
        {
          "formatting": {
            "doesnt": "matter",
            "here": true
          },
          "some.dotted.root.key": {
            "content": [
              "should",
              "be",
              "here"
            ],
            "valid": "JSON"
          }
        }\x1b[0m
        """
        # TODO: check different values on JSON files
        # ).assert_errors_contain(
        #     """
        #     NIP349 File my.json has different values. Use this:\x1b[32m
        #     {
        #       "formatting": {
        #         "here": true,
        #         "on the": "config file"
        #       }
        #     }\x1b[0m
        #     """
    )


def test_invalid_json(request):
    """Test invalid JSON on a TOML style."""
    # pylint: disable=line-too-long
    ProjectMock(request).style(
        '''
        [nitpick.JSONFile]
        file_names = ["another.json"]

        ["another.json".contains_json]
        some_field = """
            { "this": "is missing the end...
        """

        ["another.json".with]
        extra = "key"
        '''
    ).flake8().assert_errors_contain(
        """
        NIP001 File nitpick-style.toml has an incorrect style. Invalid config:\x1b[32m
        "another.json".contains_json.some_field.value: Invalid JSON (json.decoder.JSONDecodeError: Invalid control character at: line 1 column 37 (char 36))
        "another.json".with: Unknown configuration. See https://nitpick.rtfd.io/en/latest/nitpick_section.html.\x1b[0m
        """,
        1,
    )


def test_json_file_with_extra_keys(request):
    """Test TOML style with extra keys for a JSON file."""
    ProjectMock(request).style(
        """
        [nitpick.JSONFile]
        file_names = ["your.json"]

        ["your.json".has]
        an_extra = "key"

        ["their.json"]
        x = 1
        """
    ).flake8().assert_errors_contain(
        """
        NIP001 File nitpick-style.toml has an incorrect style. Invalid config:\x1b[32m
        "their.json": Unknown file. See https://nitpick.rtfd.io/en/latest/config_files.html.
        "your.json".has: Unknown configuration. See https://nitpick.rtfd.io/en/latest/nitpick_section.html.\x1b[0m
        """,
        1,
    )
