# eqs-services

## Steps to run
```
virtualenv env-eqs-services
source env-eqs-services/bin/activate

git clone https://github.com/eucalyptus/DeploymentManager.git
cd DeploymentManager
python setup.py install
cd ..

pip install jenkinsapi Flask
git clone https://github.com/shaon/eqs-services.git eqa_services
cd eqa_services
python app.py
```
