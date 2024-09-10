.PHONY: start-ngrok
start-ngrok:
	@if [ -f ngrok.pid ]; then $(MAKE) stop-ngrok; fi; \
	ngrok http 8000 &>/dev/null & echo $$! > ngrok.pid && sleep 1 && \
	NGROK_URL=$$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url') && \
	echo "Updating .env with new BASE_URL: $$NGROK_URL" && \
	sed -i '' "s|^BASE_URL=.*|BASE_URL=$$NGROK_URL|" .env

stop-ngrok:
	@kill `cat ngrok.pid` && rm ngrok.pid && echo "ngrok stopped"
