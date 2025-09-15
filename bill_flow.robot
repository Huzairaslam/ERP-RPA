*** Settings ***
Library    SeleniumLibrary
Resource   locators.robot
Resource   billvalue.robot
Resource   data.robot

*** Tasks ***
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
    Sleep    3s
    # Page Should Contain    ${SUCCESS_TEXT}

Create Sales Invoice
    [Documentation]    Fill and submit Purchase Bill form after login

    # Parse API data before filling form
    Parse API Response

    Go To    ${BILL_URL}
    Wait Until Element Is Visible    ${NEWBTN}    20s
    Click Element    ${NEWBTN}

    # Fill invoice number (from API)
    Wait Until Element Is Visible   ${INVOICENUMBER}    5s
    Input Text    ${INVOICENUMBER}    ${invoice_number}

    # Fill document date (from API)
    Wait Until Element Is Visible   ${DOCDATE}    5s
    Input Text    ${DOCDATE}    ${doc_date}

    # Fill vendor order number (using po_number)
    Wait Until Element Is Visible   ${VENDORNUMBER}    5s
    Input Text    ${VENDORNUMBER}    ${vendor_number}

    # Fill delivery address (customer_address)
    Wait Until Element Is Visible   ${DELIVERYADDRESS}    5s
    Input Text    ${DELIVERYADDRESS}    ${delivery_address}

    # Select vendor name (company_name)
    Wait Until Element Is Visible   ${VENDORNAME}    5s
    Input Text    ${VENDORNAME}    ${vendor_name}

    # Select purchase order
    Wait Until Element Is Visible   ${PURCHASEORDER}    5s
    # Input Text    ${PURCHASEORDER}    ${po_number}

    # Submit the form
    Wait Until Element Is Visible    ${SUBMITBTN}    5s
    Click Element    ${SUBMITBTN}

    Sleep    2s
    Log To Console    ✅ Sales Invoice Created Successfully with API Data