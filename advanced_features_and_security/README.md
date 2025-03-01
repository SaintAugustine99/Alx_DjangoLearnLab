## Permissions and Groups Setup

### Custom Permissions

Custom permissions are defined in the `BlogPost` model to control actions such as viewing, creating, editing, and deleting blog posts.

### User Groups

Three user groups are set up:

1. **Editors**: Can create and edit blog posts.
2. **Viewers**: Can view blog posts.
3. **Admins**: Can view, create, edit, and delete blog posts.

### Enforcing Permissions in Views

Views are protected using the `@permission_required` decorator. For example, the edit view checks for the `can_edit` permission.


## Security Measures

### Secure Settings

- `DEBUG`: Set to `False` in production to prevent detailed error pages from being displayed.
- `SECURE_BROWSER_XSS_FILTER`: Enabled to prevent cross-site scripting attacks.
- `X_FRAME_OPTIONS`: Set to `DENY` to prevent clickjacking.
- `SECURE_CONTENT_TYPE_NOSNIFF`: Enabled to prevent MIME type sniffing.
- `CSRF_COOKIE_SECURE` and `SESSION_COOKIE_SECURE`: Ensures cookies are sent over HTTPS only.

### CSRF Protection

All forms include the CSRF token to protect against cross-site request forgery attacks.

### Safe Data Handling

Views are secured by using Django's ORM to prevent SQL injection and validating user inputs.
