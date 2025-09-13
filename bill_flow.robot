*** Settings ***
Library    SeleniumLibrary
Resource   locators.robot
# Resource   dummydata.json
Resource   data.robot
*** Keywords ***
Create Sales Invoice
    [Documentation]    Fill and submit Sales Invoice form after login
   
    Go To    ${BILL_URL}
    Sleep   10s
    Wait Until Element Is Visible    ${NEWBTN}    10s
    Click Element    ${NEWBTN}

    # Fill invoice number
    Wait Until Element Is Visible   ${INVOICENUMBER}    5s
    Click Element 	${INVOICENUMBER} 
    Input Text    ${INVOICENUMBER}    INV-2025-001

    # Fill document date
    Wait Until Element Is Visible   ${DOCDATE}    5s
    Click Element 	${DOCDATE}
    Input Text    ${DOCDATE}    2025-09-12

    # Fill vendor order number
    Wait Until Element Is Visible   ${VENDORNUMBER}    5s
    Click Element 	${VENDORNUMBER}
    Input Text    ${VENDORNUMBER}    VEND-1234

    # Fill delivery address
    Wait Until Element Is Visible   ${DELIVERYADDRESS}    5s
    Click Element 	${DELIVERYADDRESS}
    Input Text    ${DELIVERYADDRESS}    Warehouse Karachi


    # Select vendor name (combobox)
    Wait Until Element Is Visible   ${VENDORNAME}    5s
    Click Element 	${VENDORNAME}
    Input Text    ${VENDORNAME}    Ali Traders
    # Keyboard Key    Enter

    # Select purchase order
    Wait Until Element Is Visible   ${PURCHASEORDER}    5s
    Click Element 	${PURCHASEORDER}
    Input Text    ${PURCHASEORDER}    PO-2025-009
    # Keyboard Key    Enter

    # Click add detail (e.g., line item)
    # Wait Until Element Is Visible   ${ADDDETAIL}    5s
    # Click    ${ADDDETAIL}
    # Sleep    1s

    # Submit the form
    Wait Until Element Is Visible    ${SUBMITBTN}    5s
    Click    ${SUBMITBTN}

    Sleep    2s
    Log To Console    Sales Invoice Created Successfully ✅
