"""Содержит тесты главной страницы"""

import allure
import pytest

from tests.ui_tests.pages.main_page import MainPage
from tests.ui_tests.src.config import PagesData


class TestMainPage:
    """Тесты основной функциональности"""

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Guest can go to all the links")
    @pytest.mark.parametrize('page, locator', PagesData.pages_list, ids=PagesData.endpoints)
    def test_guest_can_go_to_all_the_links(self, main_page: MainPage, page: str, locator: tuple):
        """Проверяет работоспособность всех страниц, доступных на главной странице """

        main_page.find_and_click_element(locator)
        current_url = main_page.driver.current_url
        assert page in current_url, f"Страница {page} не открылась"
