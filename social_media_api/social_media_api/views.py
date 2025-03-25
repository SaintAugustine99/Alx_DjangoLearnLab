"""
Views for the main project.
"""
from django.http import HttpResponse

def home(request):
    """Home page view for the API."""
    html = """
    <html>
        <head>
            <title>Social Media API</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                h1 { color: #333; }
                ul { line-height: 1.6; }
                code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }
            </style>
        </head>
        <body>
            <h1>Social Media API</h1>
            <p>Welcome to the Social Media API. Below are the available endpoints:</p>
            <ul>
                <li><a href="/admin/">Admin Interface</a> - For site administration</li>
                <li><a href="/api/accounts/register/">Register</a> - Create a new user account</li>
                <li><a href="/api/accounts/login/">Login</a> - Get authentication token</li>
                <li><a href="/api/accounts/profile/">Profile</a> - View/update your profile (requires authentication)</li>
            </ul>
            <p>For API documentation, check the README.md file.</p>
        </body>
    </html>
    """
    return HttpResponse(html)