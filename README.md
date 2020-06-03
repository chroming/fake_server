A fake server than catch all path and response success message or whatever data you defined.

## Usage

`fake-server -t Success!`

Then you can access whatever path in 'http://127.0.0.1' (such as http://127.0.0.1/simple/a/b/c), and then get response text 'Success!'.

If you what to bind to https (normally with port 443), you should create local_server.key and local_server.crt first like this:

`openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout local_server.key -out local_server.crt -subj "/C=CN/ST=SH/L=SH/O=GH/OU=GH/CN=*"`

All arguments:

`fake-server -t TEXT [-f FILE_PATH| -fc FILE_PATH] -b 127.0.0.1:80 -s -sk /tmp/local_server.key -sc /tmp/local_server.key`

**SERVER ARGUMENTS**

+ -b --bind *IP:PORT*: Server bind host and port, default 127.0.0.1:80, if you what listen on all interface just use 0.0.0.0:80
+ -p --port *PORT*: Server bind port, same as port in --bind
+ -s --https: Server with https or not
+ -sk --server_key *FILE_PATH*: Server key file path
+ -sc --server_crt *FILE_PATH*: Server cert file path

**RESPONSE ARGUMENTS**

You can only choice one argument for response

+ -t --text *TEXT*: Return text, default Success
+ -f --file *FILE_PATH*: Return file as attachment
+ -fc --file_content *FILE_PATH*: Return file content

## Q&A
### Why I need this?

When you notice some software send your private data to their server(like: http://data.old_server.com ), and 
the software need success response from server(like: {"result": "success"}) otherwise it will not work, what can you do?
Now ,with fake-server, you can do like this:

1. Add this line to your hosts file (Linux/macOS: /etc/hosts, Windows: C:\Windows\System32\Drivers\etc\hosts)

`127.0.0.1 data.old_server.com`

2. Start fake server:
fake-server '{"result": "success"}'

Then all data send to data.old_server.com will now send to your own compute, and software will get normal response as before! 

### Run with `[ERROR] Retrying in 1 second in...` in my macOS ?

For macOS user who what to bind to port less than 1024(include default http 80 and https 443 port)

macOS has a limit that you can't bind to port less than 1024 without sudo,

if macOS version >= 10.14, you can bind to 0.0.0.0 without root, so fake-server will bind to 0.0.0.0 in macOS by default.