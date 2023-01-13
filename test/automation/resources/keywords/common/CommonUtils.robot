# SPDX-FileCopyrightText: 2022 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

*** Settings ***
# Library  Selenium2Library

*** Variables ***

*** Keywords ***
Start Testcase
    Open Browser  ${url.${env}}  ${browser}
    Page Should Contain  What are ToLIDs?
    Maximize Browser Window
    Sleep  2s

Common - Setup Webdriver
    ${options} =  Evaluate  sys.modules['selenium.webdriver'].ChromeOptions()  sys, selenium.webdriver
    Call Method  ${options}  add_argument  disable_gpu
    ${options} =  Call Method  ${options}  to_capabilities

    ${driver}  Create Webdriver  Remote  command_executor=http://tolid-chrome:4444/wd/hub  desired_capabilities=${options}

    [Return]  ${driver}


