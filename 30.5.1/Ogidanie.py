import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Setting import VAlid_Password, Valid_Email
from selenium import webdriver

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Firefox()



   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends.skillfactory.ru/login')

   # Вводим email
   pytest.driver.find_element(By.ID, 'email').send_keys(Valid_Email)

   # Вводим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys(VAlid_Password)

   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

   yield

   pytest.driver.quit()

def test_show_all_pets():

   # Открываем страницу все питомцы.
   pytest.driver.find_element(By.CSS_SELECTOR, 'a[href="/"]').click()

   # Настраиваем неявные ожидания:
   pytest.driver.implicitly_wait(10)

   # Проверяем, что мы оказались на главной странице (все питомцы)
   assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

   # Ищем на странице все фотографии, имена, породу и возраст питомцев:
   images = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
   names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
   descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

   # Проверяем, что на странице есть фотографии питомцев, имена, порода и возраст питомцев не пустые:
   for i in range(len(names)):
      assert images[i].get_attribute('src') != ''
      assert names[i].text != ''
      assert descriptions[i].text != ''
      assert ', ' in descriptions[i]
      parts = descriptions[i].text.split(", ")
      assert len(parts[0]) > 0
      assert len(parts[1]) > 0

def test_show_my_pets():
   # Открываем страницу мои питомцы.
   pytest.driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()

   wait = WebDriverWait(pytest.driver, 10)


   # Проверяем, что мы оказались на  странице пользователя, ожидая, что в течение 10с на странице есть тег h2 с тименем пользователя "Vasya"
   assert wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'h2'), 'Vasya'))

   # Ищем в теле таблицы все строки с полными данными питомцев (имя, порода, возраст):
   css_locator = 'tbody>tr'
   data_my_pets = pytest.driver.find_elements(By.CSS_SELECTOR, css_locator)

   # Ожидаем, что данные всех питомцев, найденных локатором css_locator = 'tbody>tr', видны на странице:
   for i in range(len(data_my_pets)):
      assert wait.until(EC.visibility_of(data_my_pets[i]))

   # Ищем в таблицt все фотографии питомцев, ожидаея, что все загруженные фото, видны на странице:
   image_my_pets = pytest.driver.find_elements(By.CSS_SELECTOR, 'img[style="max-width: 100px; max-height: 100px;"]')
   for i in range(len(image_my_pets)):
      if image_my_pets[i].get_attribute('src') != '':
         assert wait.until(EC.visibility_of(image_my_pets[i]))

   # Ищем в таблице все данные возраста питомцев, ожидая увидеть их на странице:
   age_my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[3]')
   for i in range(len(age_my_pets)):
      assert wait.until(EC.visibility_of(age_my_pets[i]))

   # Ищем в таблице все породы питомцев, ожидая увидеть их на странице:
   type_my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[2]')
   for i in range(len(type_my_pets)):
      assert wait.until(EC.visibility_of(type_my_pets[i]))


   # Ищем в таблице все имена питомцев. ожидая увидеть их на странице:
   name_my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[1]')
   for i in range(len(name_my_pets)):
      assert wait.until(EC.visibility_of(name_my_pets[i]))