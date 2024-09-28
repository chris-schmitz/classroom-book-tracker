import requests
from mockito import when, verify, mock, kwargs

from src.example import multiply_n_numbers, get_book_list, update_book


class TestSuite:
    def test_basic_idea(self):
        # * The basic idea behind testing is:
        # - set up the data that you'd pass in to your function/method or other supporting data
        # - run the code you're trying to test (call the function or method, trigger the process, etc)
        # - assert that what you expected to happen actually happened
        # * it's typically referred to as Arrange, Act, and Assert. so:

        # * Arrange:
        expected_output = 20

        # * Act:
        actual_output = 10 + 10

        # * Assert:
        assert actual_output == expected_output

    def test_external_tools(self):
        # * So given how a basic test is setup, we can test our actual code. It's the same as the last test case, but
        # * instead of having our "Act" logic in the test function itself, we reference an existing function. In this
        # * case it's in this same file, but you can just as easily import it from another file in the project.
        expected = 4

        actual = add_two_numbers(2, 2)

        assert expected == actual

    def test_external_tools_part_two(self):
        # * To drive it home, here we're going to test a function defined in `src/example.py` and test it
        expected = 64

        actual = multiply_n_numbers(2, 4, 8)

        assert expected == actual

    def test_mock_an_external_library(self):
        # * For most real programs, you also need to know how to mock an external tool/library you're code uses. So like
        # * here let's pretend that we're querying a server for some data during our process and operating off of it.
        # * We don't necessarily want to call the API each time we want to test (data could change per call, api could
        # * be down, and it's always going to make the test take longer than it needs to), so we can just mock out the
        # * call and tell it what data the call would return instead.

        # * Here we know that when you call `requests.get()` it returns an object containing a method `json` that we
        # * need to call to get the actual data. To fake that out, or mock it, we just write a simple class that has
        # * a method with the same name (json), and tell it to return whatever data we'd want to use for testing. this
        # * way our actual code in the `src` folder can be written exactly as it would be used normally, but we can
        # * fake out the requests tool (or whatever tool) and insert the data we want to work on.
        api_url = "http://www.somebooksearch.biz/search"

        class MockResponse:
            def json(self):
                return {"books": [{"title": "Some book title", "isbn": "123456"}]}

        # * Here's where we're doing the actual mocking. the normal python way looks a bit different, but I think the
        # * mockito tool reads way better. the actual method we're mocking out is the `get` method here:
        when(requests).get(api_url).thenReturn(MockResponse())

        actual = get_book_list()

        assert actual == [{"title": "Some book title", "isbn": "123456"}]

    def test_mock_an_external_library_but_without_comments(self):
        # * showing the exact same thing but without the giant comment blocks so we can see how easy and quick it can be
        api_url = "http://www.somebooksearch.biz/search"
        # * an slimer way of defining the same mock class
        mock_response = mock({
            "json": lambda: {"books": [{"title": "Some book title", "isbn": "123456"}]}
        })

        when(requests).get(api_url).thenReturn(mock_response)

        actual = get_book_list()

        assert actual == [{"title": "Some book title", "isbn": "123456"}]

    def test_verify_we_sent_data_somewhere(self):
        # * Sticking with the api calls, sometimes it's good to verify that a method was called even if there's not a
        # * result associated with it. Like if we `post` an http request to a server. Likely we're not going to get data
        # * as a response, or at least not data we care about, we just want to know the post call was made with the
        # * right data.
        api_url = "http://www.somebooksearch.biz/search"
        payload = {"title": "An updated title", "isbn": 12345}

        update_book(payload)

        verify(requests).post(api_url, data=None, json=payload)


def add_two_numbers(a: int, b: int) -> int:
    return a + b
