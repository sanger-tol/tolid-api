# SPDX-FileCopyrightText: 2022 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

*** Settings ***
Resource  ../../imports.robot

*** Variables ***
# Note: We need to add path for browser drivers in the bash profile and save browser drivers to that location
# ${browser}  safari  chrome  firefox  opera
# ${env}  dev  staging  production
# &{url}  dev=http://localhost:3002  staging=https://id-staging.tol.sanger.ac.uk  production=https://id.tol.sanger.ac.uk
&{url}  dev=http://localhost:3002 

*** Keywords ***
Start Testcase
    # Open Browser  ${url.${env}}  ${browser}
    Open Browser  ${url}
    Page Should Contain  What are ToLIDs?
    Maximize Browser Window
    Sleep  2s

# Finish Testcase
#     Close Browser

# Insert Testing Data
#     Log  I am setting up test data

# Cleanup Testing Data
#     Log  I am cleaning up test data

Setup WebDriver
    ${driver}  Get Variable Value  ${headless}
    ${driver}  Run Keyword If  "${driver}" == "${None}"
    # ...        Create Webdriver    ${browser}    executable_path=${driverPath}
    ...        Create Webdriver    Chrome    executable_path=/Users/am66/homebrew/bin/chromedriver
    ...        ELSE 
    # ...        Run Keyword  Setup Headless ${browser} WebDriver
    ...        Run Keyword  Setup Headless Chrome WebDriver
    [Return]  ${driver}

# Common - Setup Headless Firefox WebDriver
#     ${firefox options} =     Evaluate    sys.modules['selenium.webdriver'].firefox.webdriver.Options()    sys, selenium.webdriver
#     Call Method    ${firefox options}   add_argument    -headless
#     ${driver}  Create Webdriver    ${browser}    firefox_options=${firefox options}  executable_path=${driverPath}
#     Set Window Size  1920  1080
#     [Return]  ${driver}

Setup Headless Chrome WebDriver
    ${chrome options} =     Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium.webdriver
    Call Method    ${chrome options}   add_argument    headless
    Call Method    ${chrome options}   add_argument    disable-gpu
    Call Method    ${chrome options}   add_argument    --no-sandbox
    ${driver}  Create Webdriver    Chrome    chrome_options=${chrome options}  executable_path=${driverPath}
    Set Window Size    1920    1080
    [Return]  ${driver}