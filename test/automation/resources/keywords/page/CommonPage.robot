# SPDX-FileCopyrightText: 2022 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

*** Settings ***
Resource  ../../../Resources/imports.robot


*** Variables ***
# ${current_role}    NONE
# ${current_project}    NONE
# ${token_id}   NONE

*** Keywords ***
# Open Browser
#     Setup WebDriver
#     ${is_headless}  Get Variable Value  ${headless}  ${False}
#     Run Keyword If  '${is_headless}' == '${True}'
#     ...              Set Window Size  2560  1440
#     ...              ELSE
#     ...              Maximize Browser Window


# Login Sts Portal
#     Go To            ${sts_portal_url}
#     Click On Element                     ${btn_login}
#     Click On Element           ${btn_login_orcid}
#     Input Text To Element              ${input_username}   ${valid_user_name}
#     Input Text To Element          ${input_password}   ${valid_password}
#     Click On Element           ${orcid_submit_btn}
#     #Common - Wait Until Loading Finish
#     wait until page contains element            ${sts_sidebar}   timeout=30s
#     Dashboard page - Switch Project    ALL

Navigate To Homepage
    Click On Homepage Portal Logo

Validate Homepage Text
    Verify Homepage Text