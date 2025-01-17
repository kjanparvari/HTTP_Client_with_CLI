# Console HTTP Client Tool  

A simple console-based HTTP client tool developed for the **Computer Networks course** at **Amirkabir University of Technology (AUT)**. This tool allows users to interact with HTTP servers via command-line arguments, making it a lightweight and flexible utility for testing and exploration.  

## Features  
- **GET and POST Requests**: Supports basic HTTP methods.  
- **Optional Arguments**:  
  - Custom headers.  
  - Request payloads for POST.  
  - Timeout settings.  
- **Response Handling**: Displays response status, headers, and body.  

## Technology Stack  
- **Programming Language**: Python  

## Usage  
This tool supports various command-line arguments for interacting with HTTP servers.  

### Arguments  

| Argument      | Description                                      | Example                          |
|---------------|--------------------------------------------------|----------------------------------|
| `url`         | The URL to send the HTTP request to.             | `http://example.com`            |
| `-M`, `--method` | The HTTP method to use (e.g., GET, POST).        | `-M POST`                       |
| `-H`, `--headers` | Add custom headers (can be used multiple times). | `-H "Authorization: Bearer <token>"` |
| `-Q`, `--queries` | Add query parameters (can be used multiple times). | `-Q "key=value"`                |
| `-D`, `--data`   | Add a raw body to the request.                  | `-D "raw body content"`         |
| `-J`, `--json`   | Add a JSON payload to the request.              | `-J '{"key": "value"}'`         |
| `-F`, `--file`   | Send the contents of a file as the request body. | `-F "file.txt"`                 |
| `-T`, `--timeout`| Set a timeout for the request in seconds.       | `-T 10`                         |

### Example Commands  

#### GET Request  
```bash
python main.py http://example.com -M GET
```
POST Request with JSON Body
```bash
python main.py http://example.com -M POST -J '{"key": "value"}'
```

## Purpose  
This project demonstrates the implementation of an HTTP client, providing insights into HTTP protocols, request/response mechanics, and practical command-line tool development.

## Acknowledgements  
This project was developed as part of the **Computer Networks course** at **Amirkabir University of Technology (AUT)**.  

## License  
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.  
