# Pof Web Server

Web server to obfuscate Python scripts using pof.

Simple server written in Python with flask, and using HTMX for user interaction with Pygment for Python syntax highlight.

Two endpoints are presented, one simple HTTP API to send raw Python sources and receive raw outputs, and one to get HTML formatted output for use with a webpage to show the highlighted code.

## Usage

Build:

```bash
podman build -f Dockerfile -t pofserver
```

Run:

```bash
podman run --rm -p 5000:5000 pofserver
```

Test:

```bash
curl localhost:5000 -X POST -d 'print("Hello, world!")'
```

Or visit [localhost:5000](http://localhost:5000).

## TODO

- Add favicon.
- Add link to Github repo and Pypi.
