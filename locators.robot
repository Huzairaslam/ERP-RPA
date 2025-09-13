*** Variables ***
${USERNAME_ID}    id=login_email
${PASSWORD_ID}    id=login_password
${LOGIN_BTN}      xpath=//button[@type='submit'][.//span[normalize-space(.)='Log in']]
${SUCCESS_TEXT}   Dashboard

# Navigation to PO (from Playwright recording)
${MENU_PURCHASE}     xpath=//li[@class='ant-menu-submenu ant-menu-submenu-vertical ant-menu-submenu-open ant-menu-submenu-active']//span[@aria-label='dollar']//*[name()='svg']
${MENU_BILL}         xpath=//div[@class='ant-menu-submenu ant-menu-submenu-popup ant-menu ant-menu-dark css-os2fvf ant-menu-submenu-placement-rightTop']//li[2]//div[1]
${LINK_PURCHASE_BILL}    xpath=//a[normalize-space()='Purchase Bill - Topsun Chemicals - Topsun-1']

# --- Invoice / PO Form Fields ---
${INVOICE_TYPE}          id=jv-manager_invoiceType
${INVOICE_NAME}          id=jv-manager_invoiceName
${INVOICE_NAME_PRINT}    id=jv-manager_invoiceNameForPrint
${DOC_NUMBER}            id=jv-manager_docNumberPrefix
${COMPANY_LOCATION}      id=:r6l:
${BUSINESS_UNIT}         id=:r6m:
${HOURS}                 id=jv-manager_lockAfterHours
${TERMS}                 id=jv-manager_termAndCondition

# --- Accounts Dropdowns ---
${TAX_ACC}               id=:r6n:
${DISCOUNT_ACC}          id=:r6o:
${FED_ACC}               id=:r6p:
${FREIGHT_ACC}           id=:r6q:
${SED_ACC}               id=:r6r:
${STOCKSTORE_ACC}        id=:r6s:
${CASHBOOK_ACC}          id=:r6t:
${SGS_ACC}               id=:r6u:
${SALES_ACC}             id=:r6v:



#Purchase Bill Screen Locators
${NEWBTN}       xpath=//button[.//span[normalize-space(text())='New/Clear']]
${INVOICENUMBER}        xpath=//input[@placeholder='Enter Invoice Number']
${DOCDATE}      xpath=//input[@role="combobox" and contains(@class,"k-input-inner")]
${VENDORNUMBER}     xpath=//input[@id='voucher-master_customerOrderNumber']
${DELIVERYADDRESS}      xpath=//input[@id='voucher-master_deliveryAddress']
${VENDORNAME}    xpath=//span[contains(@class,"k-combobox")]//input[@placeholder="Type here to search Vendor"]
${PURCHASEORDER}    xpath=//span[contains(@class,"k-combobox")]//input[@placeholder="Type Vendor Name/ PO# to search open purchase Order"]
${ADDDETAIL}        xpath=//div[@type='primary']
${SUBMITBTN}        xpath=//span[normalize-space()='Add']