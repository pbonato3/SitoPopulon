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
my $esito = undef;						#inizializzo le variabili esito
my $usn;								#ed username

my $logged = getSession();						#provo a prendere la sessione
if(!$logged){									#qui se non esiste nessuna sessione
	$usn= $page->param('username');				#salvo i parametri username
	my $psw= $page->param('password');			#e password
	$esito= createSession($usn,$psw);			#chiamo la funzione che crea una sessione e mi ritorna una valore vero o falso che indica l'esito della creazione
	if(!$esito){								#qui le credenziali sono sbagliate
		print $page->header();					#mi serve uno header
	};
}
else{											#qui se invece esisteva già una sessione
	destroySession();							#distruggo la sessione precedente
	$usn= $page->param('username');				#salvo i parametri username
	my $psw= $page->param('password');			#e password
	$esito= createSession($usn,$psw);			#chiamo la funzione che crea una sessione e mi ritorna una valore vero o falso che indica l'esito della creazione
	if(!$esito){								#qui le credenziali sono sbagliate
		print $page->header();					#mi serve uno header
	};
};


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

print $page->div({-id => 'header'}, h1("Populon"), img({-src => "/populon/img/titolo.png", -alt => "Populon"})), "\n";

#################		nav		#################

print $page->div({-id => 'nav'}, ul(
li(a({-href => '/populon/Home.html'},"Home")),
li(a({-href => '/populon/IlMondoDiGioco.html'},"Il mondo di gioco")),
li(a({-href => '/populon/IPersonaggi.html'},"I personaggi")),
li(a({-href => '/populon/cgi-bin/Notizie.cgi'},"Notizie")),
li(a({-href => '/populon/Chi.html'},"Chi Siamo")))), "\n"; 

#################		content		#################

print "<div id='content'>";

if($esito){
	print "<h2>Login avvenuto con successo</h2>";
	print "<h3>Benvenuto $usn</h3>";
	print "<form action='/populon/Home.html' method='post'>";
	print "<p><input type='submit' value='Continua'/></p>";
	print "</form>";
}
else{														#altrimenti le credenziali non erano valide
	print "<h2>Login fallito</h2>";
	print "<form action='/populon/Home.html' method='post'>";
	print "</p><input type='submit' value='Indietro'/></p>";
	print "</form>";
};

print "</div>";
	
print $page->end_html, "\n"; # fine pagina HTML