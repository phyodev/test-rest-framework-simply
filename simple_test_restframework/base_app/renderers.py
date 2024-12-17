from rest_framework.renderers import BrowsableAPIRenderer

class CustomBrowsableAPIRenderer(BrowsableAPIRenderer):
    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)
        context['jwt_token'] = None  # Add JWT token to the context (optional)
        return context

    def get_rendered_html_form(self, *args, **kwargs):
        # Get the rendered form from the parent method
        rendered_form = super().get_rendered_html_form(*args, **kwargs)

        # Ensure rendered_form is a string before concatenating
        if not rendered_form:
            rendered_form = ""  # Set it to an empty string if False

        rendered_form += """
            <form style="margin-top: 20px;">
                <label for="jwt-token">Enter JWT Token:</label>
                <input type="text" id="jwt-token" name="jwt-token" placeholder="JWT Token">
                <script>
                    // Store token in local storage and use it for subsequent requests
                    document.querySelector('#jwt-token').addEventListener('change', function(event) {
                        localStorage.setItem('jwtToken', event.target.value);
                    });
                    
                    // Pre-fill token input with saved token
                    const savedToken = localStorage.getItem('jwtToken');
                    if (savedToken) {
                        document.querySelector('#jwt-token').value = savedToken;
                    }

                    // Override fetch to include JWT in Authorization header
                    const originalFetch = window.fetch;
                    window.fetch = function(url, options = {}) {
                        const token = localStorage.getItem('jwtToken');
                        if (token) {
                            options.headers = options.headers || {};
                            options.headers['Authorization'] = 'Bearer ' + token;
                        }
                        return originalFetch(url, options);
                    };
                </script>
            </form>
        """
        return rendered_form
