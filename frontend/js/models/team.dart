#library('team');

#import('dart:html');
#import('base.dart');
#import('tournament.dart');
#source('../views/team.dart');

interface TeamInterface extends BaseInterface {

    TournamentInterface tournament_id;

    String about;
    String captain;
    String coach;
    String contacts;

    String manager;
    String photo_big;
    String photo_original;
    String photo_small;
    String ranking;
    String rating;

    String sponsor_about;
    String sponsor_address;
    String sponsor_contact;
    String sponsor_email;
    String sponsor_name;
    String sponsor_url;

}



class Team extends Base {

    String class_name = "team";

    Team() {

    }

    read(TeamInterface data) {


         TeamView team_item = new TeamView(data);


         document.query('#main-content').nodes.clear();
         document.query('#main-content').nodes.add(team_item.root);
    }

}

