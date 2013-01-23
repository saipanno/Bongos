BRISEIS设计
===

# 功能设计

## 功能列表

* 自动化操作
        
# URL设计

### 首页

`http://briseis.saipanno.com`

### 机架展示

`http://briseis.saipanno.com/rack`

### 服务器管理

`http://briseis.saipanno.com/server`


### 自动化操作

#### 操作说明

并发自动化远程执行及状态测试工具.支持如下几种操作:

* SSH状态测试
* PING状态测试
* 预定义操作
* 自定义操作

#### URL设计

`http://briseis.saipanno.com/detect`         检测单列表

`http://briseis.saipanno.com/detect/{id}`    显示操作单细节

`http://briseis.saipanno.com/detect/create`  创建标准操作单,默认为`/check/create/ping`任务

`http://briseis.saipanno.com/detect/create/ssh`  创建SSH联通性测试任务

`http://briseis.saipanno.com/detect/create/ping`    创建PING联通性任务

`http://briseis.saipanno.com/operate` 操作单列表

`http://briseis.saipanno.com/operate/{id}` 显示操作单细节

`http://briseis.saipanno.com/operate/create` 创建标准操作单,默认为`/operate/create/default`任务

`http://briseis.saipanno.com/operate/create/define`   创建标准操作单

`http://briseis.saipanno.com/operate/create/custom`   创建自定义操作单


### 个人管理

`http://briseis.saipanno.com/setting` 显示,修改个人信息


# 应用布局设计