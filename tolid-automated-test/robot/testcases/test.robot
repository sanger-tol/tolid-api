*** Settings ***
Suite Setup  Common - Open Browser
Suite Teardown  Close All Browsers
Resource  ../imports.robot


*** Variables ***
${URL}  http://tolid-test.lan


*** Test Cases ***
Navigate to the Index Page
    Go to  ${URL}

    Maximize Browser Window
    Capture Page Screenshot
