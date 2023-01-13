# SPDX-FileCopyrightText: 2022 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

*** Settings ***
Documentation  ToLID Basic Home Page Login and Search
Resource  ../resources/imports.robot

Suite Setup    Run Keywords  Open Browser using Webdriver
# Suite Setup  CommonUtils.Start Testcase
Suite Teardown    Close Browser

# robot -d results --include Admin -v ENV:QA -v browser:chrome Tests/Web/ToLID_web_Tests.robot

*** Variables ***


*** Test Cases ***
TC_1.1 - User should be able to access portal homepage
    [Documentation]  This test case verifies the accessability of the portal
    [Tags]  test_007

    sleep   5s
    Navigate To Homepage
    Validate Homepage Text
