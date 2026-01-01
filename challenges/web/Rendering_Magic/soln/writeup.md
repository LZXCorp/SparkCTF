This is a simple SSTI injection challenge

1. Enter an SSTI payload into the input field and read flag.txt to get the flag
2. https://github.com/payloadbox/ssti-payloads can be used for pre-existing payloads ( {{config.__class__.__init__.__globals__['os'].popen('cat flag.txt').read()}} works when I tested)
