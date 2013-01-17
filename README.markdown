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

`www.briseisapp.com/server`

### 状态查询

#### 操作说明

并发状态检测工具.支持如下三种检查类型类型:

* SSH状态测试
* PING状态测试
* SOCKET状态测试

#### URL设计

`www.briseisapp.com/check`         检测单列表

`www.briseisapp.com/check/{id}`    显示操作单细节

`www.briseisapp.com/check/create`  创建标准操作单,默认为`/check/create/ping`任务

`www.briseisapp.com/check/create/ssh`  创建SSH联通性测试任务

`www.briseisapp.com/check/create/ping`    创建PING联通性任务

`www.briseisapp.com/check/create/socket`    创建SOCKET联通性任务

### 自动化操作

#### 操作说明

并发自动化远程执行工具.支持如下三种操作类型:

* 预定义操作
* 自定义操作
* 从模板创建自定义操作

#### URL设计

`www.briseisapp.com/operate` 操作单列表

`www.briseisapp.com/operate/{id}` 显示操作单细节

`www.briseisapp.com/operate/create`          创建标准操作单,默认为`/operate/create/default`任务

`www.briseisapp.com/operate/create/define`   创建标准操作单

`www.briseisapp.com/operate/create/custom`   创建自定义操作单

`www.briseisapp.com/operate/create/template` 从模板创建自定义操作单


### 个人管理

`www.briseisapp.com/setting` 显示,修改个人信息


# 应用布局设计