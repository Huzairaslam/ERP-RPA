*** Settings ***
Library    SeleniumLibrary
Resource   locators.robot
Resource   dummydata.json

*** Keywords ***
Go To Purchase Order Screen
    Wait Until Element Is Visible 	 ${MENU_PURCHASE} 	 5s 	 
    SeleniumLibrary.Mouse Over    ${MENU_PURCHASE}
    Wait Until Element Is Visible 	 ${MENU_BILL} 	 5s 	 
    SeleniumLibrary.Mouse Over    ${MENU_BILL}
    Wait Until Element Is Visible 	 ${LINK_PURCHASE_BILL} 	 5s 	 
    Click Element    ${LINK_PURCHASE_BILL}

Fill Purchase Order Form
    [Arguments]    ${data}

    # --- Simple Input Fields ---
    Fill Text    ${INVOICE_TYPE}          ${data['invoice_type']}
    Fill Text    ${INVOICE_NAME}          ${data['invoice_name']}
    Fill Text    ${INVOICE_NAME_PRINT}    ${data['invoice_name_print']}
    Fill Text    ${DOC_NUMBER}            ${data['doc_number']}
    Fill Text    ${HOURS}                 ${data['hours']}
    Fill Text    ${TERMS}                 ${data['terms']}

    # --- Dropdown Inputs (type + Enter) ---
    Fill Dropdown Field    ${COMPANY_LOCATION}    ${data['company_location']}
    Fill Dropdown Field    ${BUSINESS_UNIT}       ${data['business_unit']}
    Fill Dropdown Field    ${TAX_ACC}             ${data['tax_acc']}
    Fill Dropdown Field    ${DISCOUNT_ACC}        ${data['discount_acc']}
    Fill Dropdown Field    ${FED_ACC}             ${data['fed_acc']}
    Fill Dropdown Field    ${FREIGHT_ACC}         ${data['freight_acc']}
    Fill Dropdown Field    ${SED_ACC}             ${data['sed_acc']}
    Fill Dropdown Field    ${STOCKSTORE_ACC}      ${data['stockstore_acc']}
    Fill Dropdown Field    ${CASHBOOK_ACC}        ${data['cashbook_acc']}
    Fill Dropdown Field    ${SGS_ACC}             ${data['sgs_acc']}
    Fill Dropdown Field    ${SALES_ACC}           ${data['sales_acc']}

Fill Dropdown Field
    [Arguments]    ${locator}    ${value}
    Click    ${locator}
    Fill Text    ${locator}    ${value}
    Keyboard Key    Enter
    Sleep    1s