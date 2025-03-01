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
