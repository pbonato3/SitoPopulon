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

$log_only=0;									#parametro speciale per il primo accesso
$cookie = $page->cookie('MY-COOKIE');			#provo a prendere il cookie
if(!$cookie){									#se non c'è il cookie
	my $usn= $page->param('username');				#salvo i parametri username
	my $psw= $page->param('password');				#e password
	$log_only=createSession($usn,$psw);				#chiamo la funzione che crea una sessione e mi ritorna il nome dell'amministratore
	if(!$log_only){										#qui le credenziali sono sbagliate
		print $page->header();
	};
}
else{											#qui se il cookie era già presente
	print $page->header();
};


print $page->start_html( # inizio pagina HTML
-title => 'Populon',									# Qui va il titolo
-dtd=>[ '-//W3C//DTD XHTML 1.0 Strict//EN',				# DTD
'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'
],
-lang =>'it',											# Lingua del documento
-meta => {'title' => 'Populon',							# Tutti i meta
'description' => 'Gioco di ruolo di...',
'keywords' => 'Gioco, ruolo, gdr, fantasy, dadi',
'author' => 'Mattia Biggeri, Tommaso Padovan, Diego Baratto, Paolo Bonato',
'language' => 'italian it'},
-style =>{'src' => '/populon/PopStyle.css'},			# Link al CSS
-author => 'paolo.bonato.12@gmail.com');				# Mail all'autore

#################		header		#################

print $page->div({-id => 'header'}, h1("Populon"), img({-src => "/populon/img/titolo.png"})), "\n";

#################		nav		#################

print $page->div({-id => 'nav'}, ul(
li(span("Home")),
li(a({-href => '/populon/IlMondoDiGioco.html'},"Il mondo di gioco")),
li(a({-href => '/populon/IPersonaggi.html'},"I personaggi")),
li(a({-href => '/populon/cgi-bin/Notizie.cgi'},"Notizie")),
li(a({-href => '/populon/Chi.html'},"Chi Siamo")))), "\n"; 

#################		content		#################

print "<div id='content'>";

if($log_only){
	print "<h2>Benvenuto $log_only</h2>";
	print "<form action='ScriviNotizia.cgi' method='get' enctype='multipart/form-data'>";
	print "</p><input type='submit' value='Scrivi Una Notizia'/></p>";
	print "</form>";
}
else{
	$session=CGI::Session->load(undef,$cookie) or die $!;		#provo a recuperare la sessione
	$nome_utente=$session->param('admin');						#salvo il parametro admin della sessione
	if($nome_utente){											#se questo è vero la sessione è corretta
		print "<h2>Benvenuto $nome_utente</h2>";
		print "<form action='ScriviNotizia.cgi' method='get' enctype='multipart/form-data'>";
		print "</p><input type='submit' value='Scrivi Una Notizia'/></p>";
		print "</form>";
	}
	else{														#altrimenti le credenziali non erano valide
		print "IMPOSTORE";							
	};
};



print "</div>";

	
print $page->end_html, "\n"; # fine pagina HTML
