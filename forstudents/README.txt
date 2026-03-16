In order to connect to this challenge, you will need to download the app.py and the index.html that are linked from the leaderboard page.

After you have downloaded them, you will need to sign up for a free ngrok account. Go to ngrok.com. Sign up. Copy your authtoken.

ngrok is used to expose your local dev site to the world. In order for my app to see yours, you must do this.

After you have copied your authtoken. Make sure that ngrok client is installed on your os:

- brew install ngrok (or)
- sudo apt install ngrok

Then you can do 'ngrok config add-authtoken $YOUR_AUTHTOKEN'.

Then you can 'ngrok http 5000' (assuming your app is running at port 5000)

Finally, edit the downloaded index.html so that fetch requests are NOT hitting localhost, they should go to your new ngrok endpoint.  

Something like 'https://ungeneralizing-sporangial-irwin.ngrok-free.dev/'.  Note, you don't have to put port 5000 there because the ngrok command already knows this.

Now you can register your team on the website and it will let you know if you have completed the challenges.
