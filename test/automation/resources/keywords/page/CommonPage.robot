# SPDX-FileCopyrightText: 2022 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

*** Settings ***
Resource  ../../../resources/imports.robot


*** Variables ***

*** Keywords ***
Common - Open Browser
    Common - Setup Webdriver
    Maximize Browser Window

Navigate To Homepage
    Click On Homepage Portal Logo

Validate Homepage Text
    Verify Homepage Text

Search a TolID
    Click on Homepage Search Button