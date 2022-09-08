import json

from selene.support.shared import browser
from selene import have, command, be, by
from selene.support.shared.jquery_style import s, ss


def given_opened_form():
    browser.open('/automation-practice-form')
    (
        ss('[id^=google_ads][id$=container__]').with_(timeout=10)
        .should(have.size_greater_than_or_equal(2))
        .perform(command.js.remove)
    )


def test_verify_form():

    # Reading input values

    with open('param.json') as json_file:
        data = json.load(json_file)

    name = data['name']
    last_name = data['last_name']
    email = data['email']
    user_number = data['user_number']
    birth_day, birth_month, birth_year = data['date_of_birth'].split(" ")
    subjects = data['subjects']
    current_address = data['current_address']
    hobby = data['hobby']
    path_to_file = data['path_to_file']
    state_and_city = data['state_and_city']

    # Handling the URL and the ads

    given_opened_form()

    # Filling the form

    browser.element('[id="firstName"]').type(name)
    browser.element('[id="lastName"]').type(last_name)
    browser.element('[id="userEmail"]').type(email)
    browser.element('[id="gender-radio-1"]').double_click()

    browser.element('#dateOfBirthInput').click()

    browser.element(by.css('.react-datepicker__month-select')).send_keys(birth_month).click().press_enter()

    browser.element(by.css('.react-datepicker__year-select')).send_keys(birth_year).click().press_enter()
    browser.element('#subjectsInput').perform(command.js.scroll_into_view)

    day_locator = ".react-datepicker__day--0" + birth_day
    browser.element(by.css(day_locator)).double_click()

    browser.element('#subjectsInput').perform(command.js.scroll_into_view)
    browser.element('#subjectsInput').type(subjects).press_enter()

    browser.element('[id=currentAddress]').type(current_address)

    hobby_xpath = "//label[contains(.,'" + hobby + "')]"
    browser.element(by.xpath(hobby_xpath)).click()

    browser.element('[id="uploadPicture"]').send_keys(path_to_file)

    browser.element('#state').perform(command.js.scroll_into_view)
    browser.element('#state').click()
    browser.element('#react-select-3-option-2').click()

    browser.element(by.xpath("//div[@id='city']/div/div")).click()
    browser.element('#react-select-4-option-0').click()

    browser.element('[id="userNumber"]').type(user_number).press_enter()

    # Verification

    browser.element('[id=example-modal-sizes-title-lg]').should((have.text("Thanks for submitting the form")))
    browser.element('[class=table-responsive]').should((have.text(name)))
    browser.element('[class=table-responsive]').should((have.text(last_name)))
    browser.element('[class=table-responsive]').should((have.text(email)))

    # browser.element('[class=table-responsive').should((have.text(user_number)))
    browser.element(by.xpath("//td[contains(text(),'Mobile')]//following-sibling::td[1]")).should((have.text(user_number)))

    date_of_birth = birth_day + " " + birth_month + "," + birth_year
    browser.element('[class=table-responsive').should((have.text(date_of_birth)))

    browser.element('[class=table-responsive').should((have.text(subjects)))
    browser.element('[class=table-responsive').should((have.text(current_address)))
    browser.element('[class=table-responsive').should((have.text(hobby)))
    browser.element('[class=table-responsive').should((have.text(state_and_city)))

    file_name = path_to_file.split('\\')[-1]
    browser.element('[class=table-responsive').should((have.text(file_name)))

#   Obsolete
#   browser.element('#state').perform(command.js.scroll_into_view)
#   browser.element('#state').click()
#   browser.element('#react-select-4-option-4').double_click()
#   browser.element('[#subjectsContainer > div]').type(subjects)
#   browser.element('[id="hobbies-checkbox-1"]').double_click()
#   browser.execute_script(f's = document.getElementById("dateOfBirthInput"); s.value = "{date_of_birth}"')
#   browser.execute_script("const ke = new KeyboardEvent('keydown', { bubbles: true, cancelable: true, keyCode: 13 "
#                           "}); document.body.dispatchEvent(ke);")
