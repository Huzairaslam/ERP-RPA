*** Variables ***
${USERNAME_ID}    xpath=//input[@placeholder='Email']
${PASSWORD_ID}    xpath=//input[@placeholder='Password']
${LOGIN_BTN}      xpath=//button[@type='submit'][.//span[normalize-space(.)='Log in']]
${SUCCESS_TEXT}   Dashboard



# Purchase Order Screen Locators
${PurchaseBtn}    xpath=//span[normalize-space()='Purchase']
${PurchaseOrderBtn}    xpath=//span[normalize-space()='Purchase Order']
${PurchaseBtn2}    xpath=//a[normalize-space()='Purchase Order - Topsun Chemicals - Topsun-1']
${PurchaseBillBtn}    xpath=//span[normalize-space()='Bill']
${PurchaseBillbtn2}    xpath=//a[normalize-space()='Purchase Bill - Topsun Chemicals - Topsun-1']

${NEWBTN}    xpath://*[normalize-space(.)="New/Clear"]
${VendorNamePO}    xpath://input[@placeholder="Search by Customer name,Code,Address,Area"]
${DocDate}    xpath=(//input[@class='k-input-inner'])[2]
${MobileNUmber}    xpath=//input[@id='jv-manager_mobileNumber']   
${SpecialInst}    xpath=//textarea[@id='jv-manager_specialInstructions']
${PoDeliveryAddress}    xpath=//input[@id='jv-manager_deliveryAddress']
${FullName}    xpath=//input[@id='jv-manager_contactPersonFullName']
# ${ExpDate}    xpath=(//input[@class='k-input-inner'])[3]
${ExpDate}    xpath=//span[contains(@class,'k-datepicker')]//button[contains(@class,'k-icon-button')]
${AddDetailPO}    xpath://*[normalize-space(.)="Add Product Detail"]
${SKUNAME}    xpath://input[@placeholder="Select SKU"]
${SKUVALUE}    xpath=//span[normalize-space()='BAG SOIL BOOSTER 50KG (SP)']
${FirstOption}    xpath=//span[normalize-space()='THE FLEX SHOP (MALIK FAHEEM DGK)(100674)']
${SKUPACK}    xpath://input[@placeholder="Select SKU Packing"]
# ${SKUPACKVALUE}    xpath=
${SKUQUANTITY}    xpath=//input[@placeholder="Quantity"]
${SKURATE}    xpath=//input[@placeholder="Agreed Rate"]
${SKUTOTALRATE}    xpath=//input[@placeholder="totalAmount"]
${ADDBTN}    xpath://*[normalize-space(.)="Add"]
${Expirydate}    xpath=//td[.//span[text()='11'] and contains(@class,'k-calendar-date')]


${PurchaseOrderNumber}    xpath://input[@placeholder="Type Vendor Name/ PO# to search open purchase Order"]
${FirstOptionPO}    xpath=//span[contains(text(), concat("PO #:42 / Customer:THE FLEX SHOP (MALIK FAHEEM DGK", ")"))]
${VendorNumber}    xpath=//input[@id='voucher-master_customerOrderNumber']
${DeliveryAddressPO}    xpath=//input[@id='voucher-master_deliveryAddress']


${SKUVALUEPB}    xpath=//span[normalize-space()='CYLINDER INSAF SEED BAGS 5KG']
${AddDetailPB}   xpath=//div[normalize-space(text())="Add Detail"]
${SKUPBRATE}    xpath=//input[@placeholder="Rate"]
${SKUPBAMT}    xpath=//input[@placeholder="Amount"]
${SKU-PB-DIS-PER}    xpath=//input[@placeholder="Discount Percentage"]
${SKU-PB-DIS-AMT}    xpath=//input[@placeholder="Discount Amount"]
${SKU-PB-VALUE-TAX}    xpath=//input[@placeholder="Value Exclusive Tax"]
${SKU-PB-TAX-PER}    xpah=//input[@placeholder="Tax Percentage"]
${SKU-PB-TOTAL-AMT}    xpath=//input[@placeholder="Total Amount"]
