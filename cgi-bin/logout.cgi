#!"C:\xampp\perl\bin\perl.exe"
use CGI::Session;
use CGI;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

require funzioni;

my $page = CGI->new;						#creazione oggetto CGI
destroySession();							#distruggo la sessione
print $page->redirect("/populon/Home.html");	#reindirizzo alla home