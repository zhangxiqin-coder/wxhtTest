*** Settings ***
Documentation    房间管理页面测试 - Robot Framework 示例
Library           SeleniumLibrary
Resource          ../resources/common_keywords.robot


*** Variables ***
${ROOMS_URL}      https://fangdong.fun/rooms
${BROWSER}        Chrome


*** Test Cases ***
TC001_RoomsPageLoads
    [Documentation]    房间页面加载测试
    Open Browser To Rooms Page
    Verify Page Title Contains    房间管理
    [Teardown]    Close Browser


TC002_AddRoomButtonVisible
    [Documentation]    添加房间按钮可见性测试
    Open Browser To Rooms Page
    Wait And Click    //button[contains(text(), '添加房间')]
    Wait Until Element Is Visible    //div[@class='el-dialog__header']
    [Teardown]    Close Browser


TC003_RoomTableHasData
    [Documentation]    房间表格数据测试
    Open Browser To Rooms Page
    Wait For Element    //table[@class='el-table__header-wrapper']
    ${rows}    Get Element Count    //tr[contains(@class, 'el-table__row')]
    Should Be True    ${rows} > 0
    [Teardown]    Close Browser


*** Keywords ***
Open Browser To Rooms Page
    Open Browser    ${ROOMS_URL}    ${BROWSER}
    Maximize Browser Window
    Wait For Page Load


Close Browser
    Close All Browsers