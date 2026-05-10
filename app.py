#!/usr/bin/env python3
"""
Simulador Fee-Based Â· Nobel Capital
Deploy em qualquer plataforma Python (Render, Railway, Fly.io)
"""
import os, json, urllib.request, urllib.error
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(os.environ.get("PORT", 8181))
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
