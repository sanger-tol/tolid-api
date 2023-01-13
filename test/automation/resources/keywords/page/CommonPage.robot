# SPDX-FileCopyrightText: 2022 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

*** Settings ***
Resource  ../../../resources/imports.robot


*** Variables ***
# ${current_role}    NONE
# ${current_project}    NONE
# ${token_id}   NONE

*** Keywords ***
Open Browser using Webdriver
    Setup WebDriver
    ${is_headless}  Get Variable Value  ${headless}  ${False}
    Run Keyword If  '${is_headless}' == '${True}'
    ...              Set Window Size  2560  1440
    ...              ELSE
    ...              Maximize Browser Window

Navigate To Homepage
    sleep   5s
    Click On Homepage Portal Logo

Validate Homepage Text
    Verify Homepage Text