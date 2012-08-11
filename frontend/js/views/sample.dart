// Generated Dart class from HTML template.
// DO NOT EDIT.

class FriendEntry {
  Map<String, Object> _scopes;
  Element _fragment;

  var age;

  FriendEntry(this.age) : _scopes = new Map<String, Object>() {
    // Insure stylesheet for template exist in the document.
    add_sample_templatesStyles();

    _fragment = new DocumentFragment();
    var e0 = new Element.html('<li></li>');
    _fragment.elements.add(e0);
  }

  Element get root() => _fragment;

  // Injection functions:
  // Each functions:

  // With functions:

  // CSS for this template.
  static final String stylesheet = "";
  String safeHTML(String html) {
    // TODO(terry): Escaping for XSS vulnerabilities TBD.
    return html;
  }
}


// Inject all templates stylesheet once into the head.
bool sample_stylesheet_added = false;
void add_sample_templatesStyles() {
  if (!sample_stylesheet_added) {
    StringBuffer styles = new StringBuffer();

    // All templates stylesheet.
    styles.add(FriendEntry.stylesheet);

    sample_stylesheet_added = true;
    document.head.elements.add(new Element.html('<style>${styles.toString()}</style>'));
  }
}
