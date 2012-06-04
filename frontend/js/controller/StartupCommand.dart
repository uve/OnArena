#library('StartupCommand');
#import('../puremvc/puremvc.dart');
#import('dart:html');

class StartupCommand extends MVCSimpleCommand implements ICommand
{
    void execute(INotification notification)
    {
        //facade.registerProxy( new DataProxy() );

        //facade.registerMediator( new ApplicationMediator( notification.getBody() as App ) );

        print('hello');
    }
}