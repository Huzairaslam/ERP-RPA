
*** Settings ***
Library    SeleniumLibrary
Resource   locators.robot
Resource   purchaseordervalue.robot
Resource   data.robot

*** Keywords ***
Type Slowly
# Typing Slowly that prevents some errors
    [Arguments]    ${locator}    ${text}    ${delay}=0.2s
    ${chars}=    Convert To List    ${text}
    FOR    ${char}    IN    @{chars}
        Press Key    ${locator}    ${char}
        Sleep        ${delay}
    END

*** Tasks ***
Login To Website
    [Documentation]    Open website and log in
    Open Browser    ${URL}    ${BROWSER}
    Sleep   5s
    # Execute JavaScript    document.body.style.zoom="50%"
    Maximize Browser Window
    ${size}=    Execute JavaScript    return [window.screen.availWidth, window.screen.availHeight];
    ${width}=   Evaluate    int(${size[0]} * 0.5)
    ${height}=  Evaluate    int(${size[1]} * 0.5)
    Set Window Size    ${width}    ${height}
    Maximize Browser Window

    Wait Until Element Is Visible    ${USERNAME_ID}    10s
    Input Text    ${USERNAME_ID}    ${USERNAME}
    Wait Until Element Is Visible    ${PASSWORD_ID}    10s
    Input Text    ${PASSWORD_ID}    ${PASSWORD}
    Wait Until Element Is Visible    ${LOGIN_BTN}    10s
    Click Button    ${LOGIN_BTN}
    Sleep    2s

Locating To Purchase Order Form
    Wait Until Element Is Visible    ${PurchaseBtn}    5s
    Click Element    ${PurchaseBtn}
    Wait Until Element Is Visible    ${PurchaseOrderBtn}    5s
    Click Element    ${PurchaseOrderBtn}
    Wait Until Element Is Visible    ${PurchaseBtn2}    5s
    Click Element    ${PurchaseBtn2}
    Sleep    2s
Purchase Order Form
    Wait Until Element Is Visible    ${NEWBTN}    5s
    Click Element    ${NEWBTN}

    Wait Until Element Is Visible    ${PoDeliveryAddress}    5s
    Click Element    ${PoDeliveryAddress}
    Input Text    ${PoDeliveryAddress}    Karachi 
    Wait Until Element Is Visible    ${MobileNUmber}    5s
    Click Element    ${MobileNUmber}
    Input Text    ${MobileNUmber}    03211234567
    Wait Until Element Is Visible    ${FullName}    5s
    Click Element    ${FullName}
    Input Text    ${FullName}    huzair

    # Wait Until Element Is Visible    ${ExpDate}    10s
    # Click Element    ${ExpDate}
    # Wait Until Element Is Visible    ${Expirydate}    5s
    # Click Element    ${Expirydate}

    Wait Until Element Is Visible    ${SpecialInst}    5s
    Click Element    ${SpecialInst}
    Input Text    ${SpecialInst}    hello 123
    Wait Until Element Is Visible    ${VendorNamePO}
    Click Element      ${VendorNamePO}    # focus the input
    Type Slowly        ${VendorNamePO}    Flex    0.2s
    Wait Until Element Is Visible    ${FirstOption}    5s
    Click Element    ${FirstOption}
    Wait Until Element Is Visible    ${AddDetailPO}
    Click Element    ${AddDetailPO}
    
    Wait Until Element Is Visible    ${SKUNAME}    5s
    Click Element    ${SKUNAME}
    Input Text    ${SKUNAME}    OIL
    Sleep    2s
    Wait Until Element Is Visible    ${SKUVALUE}
    Click Element    ${SKUVALUE}

    Wait Until Element Is Visible    ${SKUQUANTITY}
    Click Element    ${SKUQUANTITY}
    Input Text    ${SKUQUANTITY}    100

    Wait Until Element Is Visible    ${SKURATE}
    Click Element    ${SKURATE}
    Input Text    ${SKURATE}    1000

    Wait Until Element Is Visible    ${SKUTOTALRATE}
    Click Element    ${SKUTOTALRATE}
    Input Text    ${SKUTOTALRATE}    100000

    Wait Until Element Is Visible    ${ADDBTN}
    Click Element    ${ADDBTN}