*** Settings ***
Library    SeleniumLibrary
Resource   locators.robot
Resource   data.robot
Resource   po_flow.robot
# Resource   invoice_flow.robot
# Resource   voucher_flow.robot
# Resource   grn_flow.robot
# Resource   bill_flow.robot

*** Keywords ***
Login To Website
    [Documentation]    Open website and log in
    Open Browser    ${URL}    ${BROWSER}
    Sleep   6s
    Maximize Browser Window
    Wait Until Element Is Visible    ${USERNAME_ID}    10s
    Input Text    ${USERNAME_ID}    ${USERNAME}
    Wait Until Element Is Visible    ${PASSWORD_ID}    10s
    Input Text    ${PASSWORD_ID}    ${PASSWORD}
    Wait Until Element Is Visible    ${LOGIN_BTN}    10s
    Click Button    ${LOGIN_BTN}
    # Run Keyword If    '${TEST STATUS}'=='FAIL'    Execute JavaScript    document.evaluate("//button[.//span[text()='Log in']]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()
    Sleep    3s
    Page Should Contain    ${SUCCESS_TEXT}


# Running The Flow
#     [Documentation]   If API name contains PO run this process
#     IF    '${name}' == 'PO' and int(${count}) > 0
#                 ${data}=    Get Process Data    ${endpoint}
#                 Go To Purchase Order Screen
#             ELSE IF    '${name}' == 'invoice' and int(${count}) > 0
#                 ${data}=    Get Process Data    ${endpoint}
#                 Go To Invoice Screen

*** Test Cases ***
RPA Login Bot
    Login To Website
    Go To Purchase Order Screen
