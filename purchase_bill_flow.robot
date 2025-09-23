
*** Settings ***
Library    SeleniumLibrary
# Library    RPA/lib/python3.10/site-packages/Browser/browser.py
Resource   locators.robot
# Resource   purchasebillvalue.robot
# Resource   purchaseordervalue.robot
Resource   data.robot
Resource   apiResponse.robot

*** Keywords ***
Type Slowly
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
    Sleep    3s

Locating To Purchase Order Form
    Wait Until Element Is Visible    ${PurchaseBtn}    5s
    Click Element    ${PurchaseBtn}
    Wait Until Element Is Visible    ${PurchaseBillBtn}    5s
    Click Element    ${PurchaseBillBtn}
    Wait Until Element Is Visible    ${PurchaseBillbtn2}    5s
    Click Element    ${PurchaseBillbtn2}
    Sleep    5s
    

Purchase Bill Form
    Wait Until Element Is Visible    ${NEWBTN}    5s
    Click Element    ${NEWBTN}
    Fetch API Data
    # PO NUMBER
    Wait Until Element Is Visible    ${PurchaseOrderNumber}
    Click Element      ${PurchaseOrderNumber}    # focus the input
    Type Slowly        ${PurchaseOrderNumber}    ${COMPANY}    0.2s
    Wait Until Element Is Visible    ${FirstOptionPO}    5s
    Click Element    ${FirstOptionPO}
    # VENDOR NUMBER
    Wait Until Element Is Visible    ${VendorNumber}    3s
    Click Element    ${VendorNumber}
    Input Text    ${VendorNumber}    ${INVOICE}
    # DELIVERY ADDRESS
    Wait Until Element Is Visible    ${DeliveryAddressPO}    3s
    Click Element    ${DeliveryAddressPO}    
    Input Text    ${DeliveryAddressPO}    Karachi,Gulshan-3-iqbal,Block-2,Imtiaz-Super-Market
    # ADD SKU BUTTON
    Wait Until Element Is Visible    ${AddDetailPB}
    Click Element    ${AddDetailPB}
    PRODUCTS INFORMATION
    Sleep    1s
    # SKU NAME 
    Wait Until Element Is Visible    ${SKUNAME}
    Click Element    ${SKUNAME}
    Input Text    ${SKUNAME}    ${SKU}
    Wait Until Element Is Visible    ${SKUVALUEPB}    3s
    Click Element    ${SKUVALUEPB}
    # SKU QUANTITY 
    Wait Until Element Is Visible    ${SKUQUANTITY}
    Click Element    ${SKUQUANTITY}
    Input Text    ${SKUQUANTITY}    ${QUANTITY}
    # SKU RATE 
    Wait Until Element Is Visible    ${SKUPBRATE}
    Click Element    ${SKUPBRATE}
    Input Text    ${SKUPBRATE}    ${RATE}
    # SKU TOTAL RATE 
    # Scroll Element Into View    ${SKUPBAMT}
    # Wait Until Element Is Visible    ${SKUPBAMT}
    # Click Element    ${SKUPBAMT}
    # Input Text    ${SKUPBAMT}    100000
    # FORM ADD BUTTON 
    Scroll Element Into View    ${ADDBTN}
    Wait Until Element Is Visible    ${ADDBTN}
    Click Element    ${ADDBTN}