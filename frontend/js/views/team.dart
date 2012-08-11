// Generated Dart class from HTML template.
// DO NOT EDIT.

class TeamView {
  Map<String, Object> _scopes;
  Element _fragment;

  TeamInterface data;
  var is_owner;

  TeamView(this.data, this.is_owner) : _scopes = new Map<String, Object>() {
    // Insure stylesheet for template exist in the document.
    add_team_templatesStyles();

    _fragment = new DocumentFragment();
    var e0 = new Element.html('<div id="caption"></div>');
    _fragment.elements.add(e0);
    var e1 = new Element.html('<div id="edit" class="aw-link"></div>');
    e0.elements.add(e1);
    var e2 = new Element.html('<h1>${inject_0()}</h1>');
    e0.elements.add(e2);
    var e3 = new Element.html('<ul id="path"></ul>');
    e0.elements.add(e3);
    var e4 = new Element.html('<li></li>');
    e3.elements.add(e4);
    var e5 = new Element.html('<a href="/#!/tournament/${data["tournament_id"]["id"]}/">${inject_1()}</a>');
    e4.elements.add(e5);
    var e6 = new Element.html('<li></li>');
    e3.elements.add(e6);
    var e7 = new Element.html('<a href="/#!/tournament/${data["tournament_id"]["id"]}/teams/">Teams</a>');
    e6.elements.add(e7);
    var e8 = new Element.html('<li id="current"></li>');
    e3.elements.add(e8);
    var e9 = new Element.html('<a href="/#!/team/${data["id"]}/">${inject_2()}</a>');
    e8.elements.add(e9);
    var e10 = new Element.html('<li></li>');
    e3.elements.add(e10);
    var e11 = new Element.html('<a href="/team/${data["id"]}/edit/">Edit</a>');
    e10.elements.add(e11);
    var e12 = new Element.html('<li>${inject_3()}</li>');
    e3.elements.add(e12);
    var e13 = new Element.html('<div class="block-7"></div>');
    _fragment.elements.add(e13);
    var e14 = new Element.html('<div class="team-photo-small"></div>');
    e13.elements.add(e14);
    var e15 = new Element.html('<a href="" id="single_image"></a>');
    e14.elements.add(e15);
    var e16 = new Element.html('<img alt="" src="${data["photo_small"]}" id="single_image_small"></img>');
    e15.elements.add(e16);
    var e17 = new Element.html('<div class="block-12-last"></div>');
    _fragment.elements.add(e17);
    var e18 = new Element.html('<div id="team-description"></div>');
    e17.elements.add(e18);
    var e19 = new Element.html('<p></p>');
    e18.elements.add(e19);
    var e20 = new Element.html('<label for="id_name">Team Name:</label>');
    e19.elements.add(e20);
    var e21 = new Element.html('<span name="name" id="id_name">${inject_4()}</span>');
    e19.elements.add(e21);
    var e22 = new Element.html('<div class="caption">All Players</div>');
    e17.elements.add(e22);
    var e23 = new Element.html('<div class="block-table"></div>');
    e17.elements.add(e23);
    var e24 = new Element.html('<table></table>');
    e23.elements.add(e24);
    var e25 = new Element.html('<thead></thead>');
    e24.elements.add(e25);
    var e26 = new Element.html('<tr></tr>');
    e25.elements.add(e26);
    var e27 = new Element.html('<td id="first"></td>');
    e26.elements.add(e27);
    var e28 = new Element.html('<td>Player</td>');
    e26.elements.add(e28);
    var e29 = new Element.html('<td>Rating</td>');
    e26.elements.add(e29);
    var e30 = new Element.html('<td class="match-overview-icons"></td>');
    e26.elements.add(e30);
    var e31 = new Element.html('<img src="http://commondatastorage.googleapis.com/cometip/images/yellow_card.png" height="28"></img>');
    e30.elements.add(e31);
    var e32 = new Element.html('<td class="match-overview-icons"></td>');
    e26.elements.add(e32);
    var e33 = new Element.html('<img src="http://commondatastorage.googleapis.com/cometip/images/red_card.png" height="28"></img>');
    e32.elements.add(e33);
    var e34 = new Element.html('<td class="match-overview-icons"></td>');
    e26.elements.add(e34);
    var e35 = new Element.html('<img src="http://commondatastorage.googleapis.com/cometip/images/soccer_ball.png" height="28"></img>');
    e34.elements.add(e35);
    var e36 = new Element.html('<tbody></tbody>');
    e24.elements.add(e36);
    var e37 = new Element.html('<div id="match-browse" class="default-block"></div>');
    _fragment.elements.add(e37);
  }

  Element get root() => _fragment;

  // Injection functions:
  String inject_0() {
    return safeHTML('${data["name"]}');
  }

  String inject_1() {
    return safeHTML('${data["tournament_id"]["name"]}');
  }

  String inject_2() {
    return safeHTML('${data["name"]}');
  }

  String inject_3() {
    return safeHTML('${is_owner}');
  }

  String inject_4() {
    return safeHTML('${data["name"]}');
  }

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
bool team_stylesheet_added = false;
void add_team_templatesStyles() {
  if (!team_stylesheet_added) {
    StringBuffer styles = new StringBuffer();

    // All templates stylesheet.
    styles.add(TeamView.stylesheet);

    team_stylesheet_added = true;
    document.head.elements.add(new Element.html('<style>${styles.toString()}</style>'));
  }
}
