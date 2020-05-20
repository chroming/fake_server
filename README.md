A fake server than catch all path and response success message or whatever data you defined.

## Usage

`python -m fake_server Success!`

Then you can access whatever path in 'http://127.0.0.1' (such as http://127.0.0.1/simple/a/b/c), and then get response text 'Success!'.

All arguments:

`python -m fake_server -t TEXT -f FILE_PATH -fc FILE_PATH -b 127.0.0.1:80`

**SERVER ARGUMENTS**

+ -b --bind: Server bind host and port, default 127.0.0.1:80, if you what listen on all interface just use 0.0.0.0:80
+ -p --port: Server bind port, same as port in --bind

**RESPONSE ARGUMENTS**

You can only choice one argument for response

+ -t --text: Return text, default Success
+ -f --file FILE_PATH: Return file as attachment
+ -fc --file_content FILE_PATH: Return file content


## Why you need this?

When you notice some software send your private data to their server(like: http://data.old_server.com ), and 
the software need success response from server(like: {"result": "success"}), what can you do?
Now ,with fake_server, you can do like this:

1. Add this line to your hosts file (Linux/macOS: /etc/hosts, Windows: C:\Windows\System32\Drivers\etc\hosts)

`127.0.0.1 data.old_server.com`

2. Start fake server:
python -m fake_server '{"result": "success"}'

Then all data send to data.old_server.com will now send to your own compute, and software will get normal response as before! 

## TODO

+ ~~To real command line tool as fake-server;~~
+ Support https