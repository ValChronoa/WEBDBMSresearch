from pyngrok import ngrok

print(ngrok.connect(5000, 'http').public_url)