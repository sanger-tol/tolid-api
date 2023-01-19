# SPDX-FileCopyrightText: 2022 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

*** Settings ***
Documentation  ToLID Basic Home Page Login and Search
Resource  ../../resources/imports.robot

Suite Setup  Common - Open Browser
# Suite Setup  CommonUtils.Start Testcase
Suite Teardown    Close Browser

# robot -d results --include Admin -v ENV:QA -v browser:chrome Tests/Web/ToLID_web_Tests.robot
# python3 ./run.py run --env dev --browser Chrome --test 'TC_1.1*' --output-path results --webdriver-path /Users/am66/Desktop/BrowserDrivers/chromedriver

*** Variables ***
${URL}  http://tolid.local


*** Test Cases ***
TC_Login_1.1 - User should be able to access portal homepage
    [Documentation]  This test case verifies the accessability of the portal
    [Tags]  test_007

    Go to  ${base_url}
    Navigate To Homepage
    Validate Homepage Text
    Sleep  5s
    Search a TolID

TC_Login_1.2 - User should be able to access portal homepage
    [Documentation]  This test case verifies the accessability of the portal
    [Tags]  test_007

    Go to  ${base_url}
    Navigate To Homepage
    Validate Homepage Text
    Sleep  5s
    Search a TolID
