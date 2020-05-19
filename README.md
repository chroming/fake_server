# fake_server

A fake server than catch all route and response success message or whatever data you defined.

## Usage

`python -m fake_server Success!`

Then you can access whatever route in 'http://127.0.0.1:5000', and then get response text 'Success!'.

all arguments:

`python -m fake_server TEXT -f FILE_PATH -fc FILE_PATH -p 8000`

**SERVER ARGUMENTS**
+ -p --port: Server port, default 80.

**RESPONSE ARGUMENTS**
You can only choice one argument for response.
+ TEXT: Return text, default Success.
+ -f --file FILE_PATH: Return file as attachment.
+ -fc --file_context FILE_PATH: Return file context.


## Why you need this?

When you notice some software send your private data to their server(like: http://data.old_server.com), and 
the software need success response from server(like: {"result": "success"}), what can you do?
Now ,with fake_server, you can do like this:

1. Add this line to your hosts file (Linux/macOS: /etc/hosts, Windows: C:\Windows\System32\Drivers\etc\hosts)
`127.0.0.1 data.old_server.com`

2. Start fake server:
python -m fake_server '{"result": "success"}'

Then all data send to data.old_server.com will now send to your own compute, and software will get normal response as before! 