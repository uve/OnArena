#import('dart:html');
#import('models/team.dart');


//#import('ApplicationFacade.dart');
// new ApplicationFacade().startup(0);

void main() {

  //print('hello');


  document.query('#a1004').on.click.add((e) => review('1004'));
  document.query('#a1005').on.click.add((e) => review('1005'));

  review('1004');

}

void review(var item_id) {
  new Team().get(item_id);
}



