# Cryptr with Flask API

## 02 - Add your Cryptr credentials

🛠️️ Create your configuration file with the variables that you obtained previously (you can retrieve them in your Cryptr application). Don't forget to replace `YOUR_DOMAIN` with your own domain:

```bash
echo "CRYPTR_AUDIENCE='http://localhost:8081'
CRYPTR_BASE_URL='https://auth.cryptr.eu'
CRYPTR_TENANT_DOMAIN='YOUR_DOMAIN'" >> config.py
```

Note: __If you are from the EU, you must add `https://auth.cryptr.eu/` in the `CRYPTR_BASE_URL` variable, and if you are from the US, you must add `https://auth.cryptr.us/` in the same variable.__

[Next](https://github.com/cryptr-examples/cryptr-flask-api-sample/tree/03-validate-access-tokens)
