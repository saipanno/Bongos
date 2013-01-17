BRISEIS设计
===

# 功能设计

## 功能列表

    1.机架展示
    2.服务器管理
    3.自动化操作
        
# URL设计

### 首页

`www.briseisapp.com`

### 机架展示

`www.briseisapp.com/rack`

### 服务器管理

`www.briseisapp.com/server` 显示服务器列表

### 自动化操作

#### 操作说明

交互式的,更好用户体验的操作平台.支持操作单类型:测试状态,远程执行

*    状态检测当前支持PING,SSH以及SOCKET测试

*    远程执行当前支持预定义操作,自定义操作以及模板操作

#### URL设计

`www.briseisapp.com/operate` 操作单列表

`www.briseisapp.com/operate/{id}` 显示操作单细节

`www.briseisapp.com/operate/create` 创建操作单

### 个人管理

`www.briseisapp.com/setting` 显示,修改个人信息


# 应用布局设计