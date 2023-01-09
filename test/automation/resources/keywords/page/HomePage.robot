# SPDX-FileCopyrightText: 2022 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

*** Settings ***
Resource  ../../imports.robot

*** Variables ***

*** Keywords ***
# Click Search
#     Press Keys  ${HomePageSearchButton}  RETURN

# Click Use the API
#     Press Keys  ${HomePageApiButton}  RETURN

# Click Login Link
#    Press Keys  ${HomePageLoginLink}  RETURN

Click On Homepage Portal Logo
    Click Element  ${PortalLogo}
    Page Should Contain  What are ToLIDs?

Verify Homepage Text
    Page Should Contain  Tree of Life Identifiers
    Page Should Contain  How did you make the ToLIDs?

    