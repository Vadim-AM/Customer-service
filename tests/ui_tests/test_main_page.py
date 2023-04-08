import pytest
import requests

from tests.ui_tests.pages.base_page import BasePage
from tests.ui_tests.pages.locators import MainPageLocators
from tests.ui_tests.pages.main_page import MainPage


class TestMainPage:
    LINK = "http://localhost:5000/"

    PAGES_LOCATORS: list[tuple[str, str]] = [MainPageLocators.MAIN_PAGE_LINK,
                                             MainPageLocators.FEATURES_PAGE_LINK,
                                             MainPageLocators.PRICING_PAGE_LINK,
                                             MainPageLocators.REVIEWS_PAGE_LINK,
                                             MainPageLocators.LOGIN_LINK,
                                             MainPageLocators.REGISTER_LINK]

    PAGES = ['index', 'features', 'pricing', 'reviews', 'login', 'register']

    @pytest.mark.smoke
    @pytest.mark.parametrize('word', PAGES)
    def test_page_response(self, driver, word: str):
        r = requests.get(self.LINK)
        assert r.status_code == 200
        assert word in r.text

    @pytest.mark.parametrize('locator', PAGES_LOCATORS)
    def test_guest_should_see_some_link(self, driver, locator: tuple):
        page = MainPage(driver, self.LINK)
        page.open()
        page.should_be_element(locator)

    @pytest.mark.parametrize('page_name, link', list(zip(PAGES, PAGES_LOCATORS)))
    def test_guest_can_go_to_link_page(self, driver, page_name: str, link: tuple):
        page = MainPage(driver, self.LINK)
        page.open()
        page.go_to_some_page(link)
        test_page = BasePage(driver, driver.current_url)
        test_page.should_be_some_page(page_name)
