# SPDX-FileCopyrightText: 2022 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

*** Settings ***
Resource  ../../imports.robot

*** Variables ***

*** Keywords ***

Click On Homepage Portal Logo
    Click Element  ${PortalLogo}
    Page Should Contain  What are ToLIDs?

Verify Homepage Text
    Page Should Contain  Tree of Life Identifiers
    Page Should Contain  How did you make the ToLIDs?

Click on Homepage Search Button
    Click Element  ${HomepageSearch}
    Sleep  5s
    Page Should Contain  Search on ToLID prefix
    