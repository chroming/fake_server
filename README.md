# fake_server

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
