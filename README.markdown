Bongos
===
######An Operation Management Web Platform for SA.



You can use the demo at: [bongos.saipanno.com](http://bongos.saipanno.com)



# Summary

* 服务器资产管理
* 操作系统自动部署
* 服务器自动化操作
* 后台管理界面



# Deploy and Run

* Download source: `git clone https://github.com/saipanno/Bongos.git`
* Create virtualenv environment: `virtualenv --never-download --distribute Bongos/env`
* Activate environment: `source Bongos/env/bin/activate`
* Install python library: `pip install -r requirements.txt`
* Install system tools: `yum install ipmitool redis`
* Initialization database: `python manage.py init_db`
* Create **setting.py** from template and Update: `cp settings.example.py settings.py`
* Create **supervisord.conf** from template and Update: `cp supervisord.example.conf supervisord.conf`
* Start redis: `service redis start`
* Start frontend and backend process: `supervisord -c Bongos/supervisord.conf`



# License

Bongos is released under the **MIT** license