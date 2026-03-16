### Running

It appears that campus blocks cloudflare tunnels, so use ngrok

- brew install ngrok
- go to ngrok dashboard and copy auth token
- ngrok http 5000 (assuming your app is running on 5000)
