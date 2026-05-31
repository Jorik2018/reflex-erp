poetry run reflex run


oc set env deployment/reflex-erp-git \
  API_URL=https://reflex-erp-git-epinedo-dev.apps.rm3.7wse.p1.openshiftapps.com \
  DEPLOY_URL=https://reflex-erp-git-epinedo-dev.apps.rm3.7wse.p1.openshiftapps.com