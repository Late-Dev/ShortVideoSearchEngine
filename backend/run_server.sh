if [[ $IS_PROD == "true" ]]; then
  uvicorn main:app --host 0.0.0.0 --port=8000 --workers=4 --ssl-keyfile=/certs/key.pem --ssl-certfile=/certs/cert.pem
else
  echo "SSL NOT WORKING"
  uvicorn main:app --host 0.0.0.0 --port=8000 --workers=4
fi
