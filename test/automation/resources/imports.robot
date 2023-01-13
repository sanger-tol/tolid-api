# SPDX-FileCopyrightText: 2022 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

*** Settings ***
# config
# Variables         ../resources/config_${env}.yaml
# Variables         ../resources/config_dev.yaml

# library
Library           SeleniumLibrary
Library           String
Library           OperatingSystem
Library           Collections
Library           Process
Library           DateTime

# Python sources
# Library            ./pythonlibs/http_utils.py
# Library            ./pythonlibs/excel_dms_asg.py
# Library            ./pythonlibs/database/DatabaseLibrary/

# elements
Resource          ../resources/keywords/common/CommonUtils.robot
Resource          ../resources/keywords/page/CommonPage.robot
Resource          ../resources/keywords/page/HomePage.robot
Resource          ../resources/elements/HomePage.robot
