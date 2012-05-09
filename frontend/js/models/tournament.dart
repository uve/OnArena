#import('dart:html');
#import('base.dart');

//#source('../views/team.dart');

interface TournamentInterface extends BaseInterface {
    
    
}


class Tournament extends Base {

    String class_name = "tournament"; 

    Team() {
     
    }   
  
    read(Map data) {
         
         /*                         
         TeamView team_item = new TeamView(data);
         
         document.query('#main-content').nodes.clear();
         document.query('#main-content').nodes.add(team_item.root);
         */
    }
              
}

