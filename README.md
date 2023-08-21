# CRLF Injection Vulnerability Lab
## Introduction
This lab is designed to demonstrate a **CRLF (Carriage Return Line Feed)** Injection vulnerability. 
CRLF Injection allows an attacker to inject a CRLF sequence into an HTTP request or response. 
This can lead to a variety of attacks such as HTTP header injection, HTTP response splitting, and others.

## Vulnerability
#### What is CRLF Injection?
CRLF stands for **"Carriage Return Line Feed"** and is typically represented by the character sequence ` \r\n ` . In HTTP headers, CRLF is used to denote the end of a header line. When an application does not properly sanitize user input, an attacker may inject their own headers or manipulate the HTTP response.

## Exploation
Here, `%0D%0A` is the URL-encoded form of CRLF and results in a new HTTP header `Set-Cookie: The_Cookie_We_Adding_With_CRLF=value_Of_The_Cookie_From_CRLF` being added to the request.
#### Payload For Example
``` 
curl -I http://127.0.0.1:8080?userInput=value%0D%0ASet-Cookie:%20The_Cookie_We_Adding_With_CRLF=value_Of_The_Cookie_From_CRLF 
```

#### Impact
+ Split HTTP responses to inject malicious content.
+ Set arbitrary cookies.
+ In some cases even an XSS attack.


## Mitigation
#### Input Validation
One way to mitigate **CRLF Injection** vulnerabilities is by sanitizing user inputs to ensure they do not contain CRLF sequences. For instance, using regular expressions to remove or replace `"\r"` or `"\n"` can be effective.

**Step 1: At our server replace lines 21-24 with the following**
```
#Prepare the HTTP response without user input
response_body = "<html><body><h1>CRLF LAB BY Niv Roda</h1></body></html>"
#response_headers = f"HTTP/1.1 200 OK\r\nContent-Length: {len(response_body)}\r\n"
sanitized_input = re.sub(r'[\r\n]', '', userInput) # (Fix 1) regex to find \r\n in user input.
```



**Step 2: At our server replace lines 26-28 with the following**
```
if userInput:
    response_headers += f"Custom-Header: {userInput}\r\n"
    #response_headers += f"Custom-Header: {sanitized_input}\r\n" # (Fix step 2) This will append the sanitized input and not the vulnerable one.
```

### Before fix:
```
C:\Users\User>curl -I http://127.0.0.1:8080?userInput=value%0D%0ASet-Cookie:%20The_Cookie_We_Adding_With_CRLF=value_Of_The_Cookie_From_CRLF
HTTP/1.1 200 OK
Content-Length: 48
Custom-Header: value
Set-Cookie: The_Cookie_We_Adding_With_CRLF=value_Of_The_Cookie_From_CRLF
```

### After fix:
```
C:\Users\User>curl -I http://127.0.0.1:8080?userInput=value%0D%0ASet-Cookie:%20The_Cookie_We_Adding_With_CRLF=value_Of_The_Cookie_From_CRLF
HTTP/1.1 200 OK
Content-Length: 48
Custom-Header: valueSet-Cookie: The_Cookie_We_Adding_With_CRLF=value_Of_The_Cookie_From_CRLF
```
