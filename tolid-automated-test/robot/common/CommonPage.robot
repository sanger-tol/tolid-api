# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

*** Settings ***
Resource            ../imports.robot

*** Keywords ***
Common - Open Browser
    Common - Setup Webdriver
    Maximize Browser Window
