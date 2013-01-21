BRISEIS设计
===

# 功能设计

## 功能列表

    1.机架展示
    2.服务器管理
    3.自动化操作
        
# URL设计

### 首页

`http://briseis.saipanno.com`

### 机架展示

`http://briseis.saipanno.com/rack`

### 服务器管理

`http://briseis.saipanno.com/server`

### 状态查询

#### 操作说明

并发状态检测工具.支持如下三种检查类型类型:

* SSH状态测试
* PING状态测试
* SOCKET状态测试

#### URL设计

`http://briseis.saipanno.com/check`         检测单列表

`http://briseis.saipanno.com/check/{id}`    显示操作单细节

`http://briseis.saipanno.com/check/create`  创建标准操作单,默认为`/check/create/ping`任务

`http://briseis.saipanno.com/check/create/ssh`  创建SSH联通性测试任务

`http://briseis.saipanno.com/check/create/ping`    创建PING联通性任务

### 自动化操作

#### 操作说明

并发自动化远程执行工具.支持如下三种操作类型:

* 预定义操作
* 自定义操作
* 从模板创建自定义操作

#### URL设计

`http://briseis.saipanno.com/operate` 操作单列表

`http://briseis.saipanno.com/operate/{id}` 显示操作单细节

`http://briseis.saipanno.com/operate/create` 创建标准操作单,默认为`/operate/create/default`任务

`http://briseis.saipanno.com/operate/create/define`   创建标准操作单

`http://briseis.saipanno.com/operate/create/custom`   创建自定义操作单


### 个人管理

`http://briseis.saipanno.com/setting` 显示,修改个人信息


# 应用布局设计