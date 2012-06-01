#library('ApplicationFacade');
#import('dart:html');
#import('puremvc/puremvc.dart');

#import('controller/StartupCommand.dart');


class ApplicationFacade/* extends MVCFacade implements IFacade */{

  final String NAME = "ApplicationFacade";


  final String STARTUP = "startup";

  IFacade facade;

  ApplicationFacade()
  {

    facade = MVCFacade.getInstance( NAME );

    ICommand command = new StartupCommand();

    //facade.registerCommand(STARTUP, command.execute);

    //write ("Facade created for ${NAME}.");

  }



  void startup(var stage)
  {
    facade.sendNotification( STARTUP );

    print(stage);

  }

  void start()
  {
    //String multitonKey = "Test Core";
    String dataPoint1 = "Hello";
    String dataPoint2 = "World";
    String proxyName = "DataProxy";
    List<String> retrievedObject;
    String badJuju = "";

    try {
      // Get a Facade



      /*
      ICommand command = new StartupCommand();


      facade.registerCommand(STARTUP, command);

      write ("Registered.");

      */

      //ICommand command = new MVCSimpleCommand( startup2, StartupCommand );

      /*
      // Create some data
      List<String> dataObject = new List<String>();
      write ("Data Object (List&ltString&gt) created.");
      dataObject.add(dataPoint1);
      write ("Data point added '${dataPoint1}'.");
      dataObject.add(dataPoint2);
      write ("Data point added '${dataPoint2}'.");

      // Register a Proxy to hold the data
      IProxy proxy = new MVCProxy( proxyName, dataObject );
      write( "Proxy '${proxyName}' created with for Data Object.");
      facade.registerProxy( proxy );
      write ("Proxy '${proxyName}' registered with Model, via Facade.");

      // Now retrieve the Proxy
      IProxy retrievedProxy = facade.retrieveProxy( proxyName );
      write ("Proxy '${proxyName}' retrieved from Model, via Facade.");

      // And get the data
      retrievedObject = retrievedProxy.getData();
      write ("Data Object (List&ltString&gt) retrieved from ${proxyName}");
      write("Data Object (List&ltString&gt) Length: " + retrievedObject.length );
      write("Contents: ${retrievedObject[0]} ${retrievedObject[1]}");

      */
      // Prove errors will be reported
      // throw "Fungers! I've got jelly in my ears!";

    } catch (var e) {
      // Catch any error
      badJuju = e.toString();

    } finally {
      // Report final status
      if ( badJuju.length == 0 && retrievedObject != null
           && retrievedObject[0] == dataPoint1
           && retrievedObject[1] == dataPoint2 ){
        write( "<P/><B>Science!</B> PureMVC is purring like a kitten. Take her out for a spin!");
      } else {
        write( "<P/><B>Claptrap!</B> Someone's thrown a spanner in the works.");
        if( badJuju.length>0 ) write( "<B>Bad juju reported:</B> ${badJuju}");
      }
    }

  }

  void write(String message) {
    // the HTML library defines a global "document" variable
    document.query('#main-content').innerHTML = document.query('#main-content').innerHTML + "<br/>" + message;
  }
}


/*
class ApplicationFacade
{
    String NAME = 'ApplicationFacade';
    String STARTUP = 'ApplicationFacadeStartUp';



    public static function getInstance():ApplicationFacade
    {
        return (instance ? instance : new ApplicationFacade()) as ApplicationFacade;
    }

    override protected function initializeController():void
    {
        super.initializeController();

        registerCommand( STARTUP, StartupCommand );

        registerCommand( URLsView.DATA_GET, DataCommand );
        registerCommand( ImagesView.DATA_GET, DataCommand );
    }

    public function startup(stage:Object):void
    {
        sendNotification( STARTUP,  stage );
    }

    override public function sendNotification(notificationName:String, body:Object=null, type:String=null):void
    {
        trace( 'Sent ' + notificationName );

        notifyObservers( new Notification( notificationName, body, type ) );
    }


}
*/
