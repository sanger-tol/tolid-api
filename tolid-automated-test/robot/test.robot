*** Settings ***
Library  SeleniumLibrary
Suite Teardown  Close All Browsers


*** Variables ***
${URL}  http://tolid-test.lan


*** Test Cases ***
Create the Webdriver for Remote Chrome
    ${options} =  Evaluate  sys.modules['selenium.webdriver'].ChromeOptions()  sys, selenium.webdriver
    Call Method  ${options}  add_argument  disable_gpu
    ${options} =  Call Method  ${options}  to_capabilities

    Create Webdriver  Remote  command_executor=http://tolid-selenium-chrome:4444/wd/hub  desired_capabilities=${options}

    Go to  ${URL}

    Maximize Browser Window
    Capture Page Screenshot
