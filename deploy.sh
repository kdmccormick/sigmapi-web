# This script will deploy the latest code to production.
# This script does NOT apply migrations. Do those yourself carefully.
HOME=/home/sigmapiwpi
DJANGOAPP=SigmaPi
STATIC=static

DEPLOY_UTILS=$HOME/deploy
REPO=$DEPLOY_UTILS/sigmapi-web-repo
PROD=$HOME/webapps

PROD_PYTHON_WEBAPP=$PROD/sigma_pi_web_2
PROD_STATIC_WEBAPP=$PROD/sigma_pi_web_static

ENV_SETTINGS_DIR=SigmaPi
ENV_SETTINGS_FNAME=environment_settings.py

PYTHON=python3.6
DJANGO_LIB=Django-1.11.4-py3.6.egg/django
PIP=pip3.6

echo "Copying REPO $REPO/$DJANGOAPP TO PROD $PROD_PYTHON_WEBAPP/$DJANGOAPP";
cp -rf $REPO/$DJANGOAPP $PROD_PYTHON_WEBAPP;
echo "";

echo "Copying REPO $REPO/$DJANGOAPP/$STATIC TO PROD $PROD_STATIC_WEBAPP";
rm -rf $PROD_STATIC_WEBAPP/*;
rm -rf $PROD_PYTHON_WEBAPP/$DJANGOAPP/$STATIC;
cp -rf $REPO/$DJANGOAPP/$STATIC/* $PROD_STATIC_WEBAPP;
echo "";

echo "Copying admin panel static files.";
cp -r $PROD_PYTHON_WEBAPP/lib/$PYTHON/$DJANGO_LIB/contrib/admin/static/admin $PROD_STATIC_WEBAPP/;
echo "";

echo "Copying production environment settings file:"
rm -rf $PROD_PYTHON_WEBAPP/$DJANGOAPP/$ENV_SETTINGS_DIR/$ENV_SETTINGS_FNAME;
cp $DEPLOY_UTILS/$ENV_SETTINGS_FNAME $PROD_PYTHON_WEBAPP/$DJANGOAPP/$ENV_SETTINGS_DIR/$ENV_SETTINGS_FNAME;
echo "";

echo "Installing Python dependencies:";
pip3.6 install --user -r $PROD_PYTHON_WEBAPP/$DJANGOAPP/requirements.txt;
echo "";

echo "Restarting server...";
$PROD_PYTHON_WEBAPP/apache2/bin/restart;
echo ""

echo "Server restarted.";
