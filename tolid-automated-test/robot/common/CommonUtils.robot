# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

*** Settings ***
Resource            ../imports.robot

*** Keywords ***
Common - Setup Webdriver
    ${options} =  Evaluate  sys.modules['selenium.webdriver'].ChromeOptions()  sys, selenium.webdriver
    Call Method  ${options}  add_argument  disable_gpu
    ${options} =  Call Method  ${options}  to_capabilities

    ${driver}  Create Webdriver  Remote  command_executor=http://tolid-selenium-chrome:4444/wd/hub  desired_capabilities=${options}

    [Return]  ${driver}
