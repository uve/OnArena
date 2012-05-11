//#import('puremvc/puremvc.dart');
#import('dart:html');
#import('models/team.dart');

void main() {

  //new Team().get('1005');


  document.query('#a1004').on.click.add((e) => review('1004'));
  document.query('#a1005').on.click.add((e) => review('1005'));

}



void review(var item_id) {

  new Team().get(item_id);

}

