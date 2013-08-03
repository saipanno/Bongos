Bongos
===
######An Operation Management Web Platform for SA.



You can use the demo at: [bongos.saipanno.com](http://bongos.saipanno.com)



# Summary

* Asset Management
* Group-based Permission Management. Accurate to Resource Access and Feature Uses.
* Fabric-based. Support External Variables and Output Record.
* Full-featured Dashboard. Support Resources CRUD.



# Deploy and Run

* Download source: `git clone https://github.com/saipanno/Bongos.git`
* Into the project directory： `cd Bongos`
* Create virtualenv environment: `virtualenv --never-download --distribute env`
* Activate environment: `source env/bin/activate`
* Install python library: `pip install -r requirements.txt`
* Install system tools: `yum install ipmitool redis`
* Update **setting.py**.
* Update **supervisord.conf** if necessary.
* Init database: `python manage.py init_db`
* Init permission: `python manage.py init_user`
* Start redis server: `service redis start`
* Start supervisord: `supervisord -c supervisord.conf`



# License

Bongos is released under the **MIT** license