#!"C:\xampp\perl\bin\perl.exe"
use CGI::Session;
use CGI;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use HTTP::Request::Common qw(POST);
use HTTP::Request::Common qw(GET);
use XML::LibXML;

require funzioni;

my $page = CGI->new;					#creazione oggetto CGI

my $nome_utente= getSession();

if(!$nome_utente){		#qualcuno sta facendo il furbo
	print $page->redirect("/populon/restricted.html");
}

print $page->header();
print $page->start_html( # inizio pagina HTML
-title => 'Populon',									# Qui va il titolo
-dtd=>[ '-//W3C//DTD XHTML 1.0 Strict//EN',				# DTD
'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'
],
-lang =>'it',											# Lingua del documento
-meta => {'title' => 'Populon',							# Tutti i meta
'description' => 'Area amministratori',
'keywords' => 'Gioco, ruolo, gdr, fantasy, dadi',
'author' => 'Mattia Biggeri, Tommaso Padovan, Diego Baratto, Paolo Bonato',
'language' => 'italian it'},
-style =>{'src' => '/populon/PopStyle.css'},			# Link al CSS
-author => 'paolo.bonato.12@gmail.com');				# Mail all'autore

#################		header		#################

print $page->div({-id => 'header'}, h1("Populon"), img({-src => "/populon/img/titolo.png"})), "\n";

#################		nav		#################

print $page->div({-id => 'nav'}, ul(
li(a({-href => '/populon/Home.html'},"Il mondo di gioco")),
li(a({-href => '/populon/IlMondoDiGioco.html'},"Il mondo di gioco")),
li(a({-href => '/populon/IPersonaggi.html'},"I personaggi")),
li(a({-href => '/populon/cgi-bin/Notizie.cgi'},"Notizie")),
li(a({-href => '/populon/Chi.html'},"Chi Siamo")))), "\n"; 

#################		content		#################

print "<div id='content'>";

if($nome_utente){											#se questo è vero la sessione è corretta
	print "<h2>Benvenuto $nome_utente</h2>";
	print "<form action='ScriviNotizia.cgi' method='post'>";
	print "</p><input type='submit' value='Scrivi Una Notizia'/></p>";
	print "</form>";
	print "<form action='logout.cgi' method='post'>";
	print "</p><input type='submit' value='Logout'/></p>";
	print "</form>";
	
}
else{														#questo perchè non si sa mai
	print "IMPOSTORE";							
};

print "</div>";

	
print $page->end_html, "\n"; # fine pagina HTML
