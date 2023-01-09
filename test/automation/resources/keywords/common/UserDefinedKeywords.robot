# SPDX-FileCopyrightText: 2022 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

*** Settings ***
# Library  Selenium2Library
# Variables  ./Webelements.py
# Resource  ../page/HomePage.robot


*** Keywords ***

ToLID Login with Saved Elixir Account
    HomePage.Click Login Link
    Sleep  2s
    LoginPage.Click Elixir Login Button
    Sleep  2s

ToLID Login with Institute Account
    HomePage.Click Login Link
    Sleep  2s
    LoginPage.Click Elixir Login Button
    Sleep  2s
#    LoginPage.Click Sign In using Another Institute or Account
    Sleep  2s
    LoginPage.Input Institute Name
    Sleep  2s
    LoginPage.Select Institute Name
    Sleep  2s
    LoginPage.Enter Institute Username
    Sleep  2s
    LoginPage.Enter Institute Password
    Sleep  2s
    LoginPage.Click Institute Login Button
    Sleep  2s
#    LoginPage.Verify Institute Login

Verify Logout from ToLID Portal
    ToLID Login with Institute Account
    Sleep  2s
    AdminHomePage.Click Logout Button
    Sleep  2s
    Page Should Contain  Tree of Life Identifiers
    
ToLID Login with Google Account
    HomePage.Click Login Link
    Sleep  2s
    LoginPage.Click Elixir Login Button
    Sleep  2s
    # LoginPage.Click Sign In using Another Institute or Account
    Sleep  2s
    LoginPage.Click Google Login Button
    Sleep  2s
#    LoginPage.Login with Gmail Account
    LoginPage.Login with Google Account