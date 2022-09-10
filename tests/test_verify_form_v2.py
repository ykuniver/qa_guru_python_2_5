import json
import os
from pathlib import Path

from selene.support.shared import browser
from selene import have, command, by
from selene.support.shared.jquery_style import ss


def given_opened_form():
    browser.open('/automation-practice-form')
    (
        ss('[id^=google_ads][id$=container__]').with_(timeout=10)
        .should(have.size_greater_than_or_equal(2))
        .perform(command.js.remove)
    )


def test_verify_form():

    # Reading input values

    script_dir = os.path.dirname(os.path.abspath(__file__))
    params_file = os.path.join(script_dir, 'param.json')

    with open(params_file) as json_file:
        data = json.load(json_file)

    name = data['name']
    last_name = data['last_name']
    email = data['email']
    user_number = data['user_number']
    gender = data['gender']
    birth_day, birth_month, birth_year = data['date_of_birth'].split(" ")
    subjects = data['subjects']
    current_address = data['current_address']
    hobby = data['hobby']
    state_and_city = data['state_and_city']

    picture = data['picture_file']
    picture_file = os.path.join(Path(script_dir).parent.absolute(), "resources", picture)

    # Handling the URL and the ads

    given_opened_form()

    # Filling the form

    # firstName, lastName, userEmail, gender, userNumber

    browser.element('[id="firstName"]').type(name)
    browser.element('[id="lastName"]').type(last_name)
    browser.element('[id="userEmail"]').type(email)
    browser.element('[id="gender-radio-1"]').double_click()
    browser.element('[id="userNumber"]').type(user_number)

    gender_xpath = "//input[@name='gender']/following-sibling::label[contains(text(),'" + gender + "')]"
    browser.element(by.xpath(gender_xpath)).click()

    # birthday

    browser.element('#dateOfBirthInput').click()
    browser.element(by.css('.react-datepicker__month-select')).send_keys(birth_month).click().press_enter()
    browser.element(by.css('.react-datepicker__year-select')).send_keys(birth_year).click().press_enter()
    browser.element('#subjectsInput').perform(command.js.scroll_into_view)
    day_locator = ".react-datepicker__day--0" + birth_day
    browser.element(by.css(day_locator)).double_click()

    # subjects

    browser.element('#subjectsInput').perform(command.js.scroll_into_view)
    browser.element('#subjectsInput').type(subjects).press_enter()

    # current address

    browser.element('[id=currentAddress]').type(current_address)

    # hobby

    hobby_xpath = "//label[contains(.,'" + hobby + "')]"
    browser.element(by.xpath(hobby_xpath)).click()

    # picture

    browser.element('[id="uploadPicture"]').send_keys(picture_file)

    # state and city

    browser.element('#state').perform(command.js.scroll_into_view)
    browser.element('#state').click()
    browser.element('#react-select-3-option-2').click()

    browser.element(by.xpath("//div[@id='city']/div/div")).click()
    browser.element('#react-select-4-option-0').click()

    # submitting the form

    browser.element('#submit').perform(command.js.click)

    # Verification

    student_name = name + " " + last_name
    date_of_birth = birth_day + " " + birth_month + "," + birth_year

    info = {'Student Name': student_name, 'Student Email': email, 'Mobile': user_number, 'Gender': gender,
            'Date of Birth': date_of_birth, 'Subjects': subjects, 'Hobbies': hobby, 'Picture': picture,
            'Address': current_address, 'State and City': state_and_city}

    for label, value in info.items():
        locator = "//td[contains(text(),'" + label + "')]//following-sibling::td[1]"
        browser.element(by.xpath(locator)).should(have.text(value))

