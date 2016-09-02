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


print '
<!DOCTYPE html
	PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
	 "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="it" xml:lang="it">
<head>
<title>Populon</title>
<link rev="made" href="mailto:paolo.bonato.12%40gmail.com" />
<meta name="keywords" content="Gioco, ruolo, gdr, fantasy, dadi" />
<meta name="language" content="italian it" />
<meta name="author" content="Riservato agli amministratori!" />
<meta name="title" content="Populon" />
<meta name="description" content="Compila la tua scheda online" />
<link rel="stylesheet" type="text/css" href="../PopStyle.css" />
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<meta http-equiv="Content-Script-Type" content="text/javascript"/>
</head>
<body onload=\'clearRedundant()\'>
';

#################		header		#################

print "<div class=\"sbarra\" >\n";

print $page->div({-id => 'header'}, h1("Populon"), img({-class => 'head', -src => "../img/titolo.png", -alt => "Populon"}), a({-class => 'saltamenu', -href => '#saltamenu'}, "Salta il menu di navigazione")), "\n";

#################		nav		#################

print $page->div({-class => 'nav'}, ul({-class => 'navbar'},
li({-class => 'button link', -onclick => 'location.href="../index.html";'}, a({-href => '../index.html', -class => 'link'},"Home")),
li({-class => 'button link', -onclick => 'location.href="../IlMondoDiGioco.html";'}, a({-href => '../IlMondoDiGioco.html', -class => 'link'},"Il mondo di gioco")),
li({-class => 'button link', -onclick => 'location.href="../cgi-bin/personaggi.cgi";'}, a({-href => '../cgi-bin/personaggi.cgi', -class => 'link'},"Personaggi")),
li({-class => 'button link', -onclick => 'location.href="../cgi-bin/Notizie.cgi";'}, a({-href => '../cgi-bin/Notizie.cgi', -class => 'link'},"Notizie")),
li({-class => 'button link', -onclick => 'location.href="../Chi.html";'}, a({-href => '../Chi.html', -class => 'link'},"Chi siamo")))), "\n"; 

print "
<div class=\"breadcrumbs\">
 <a name=\"saltamenu\"></a>
  <strong>
    Ti trovi in:
  </strong>
  Area Amministratori
</div>
";


#################		content		#################

print "<div class='content'>";

if($esito){
	print "<h2>Login avvenuto con successo</h2>";
	print "<h3>Benvenuto $usn</h3>";
	print "<form action='../index.html' method='post'>";
	print "<p><input type='submit' value='Continua'/></p>";
	print "</form>";
}
else{														#altrimenti le credenziali non erano valide
	print "<h2>Login fallito</h2>";
	print "<form action='../index.html' method='post'>";
	print "</p><input type='submit' value='Indietro'/></p>";
	print "</form>";
};

print "<a href='#header' class='goup'>Vai a inizio pagina</a></div>";
	
print "<div id='footer'>Contatti: populon(at)gmail.com
		<div class='login'>
			<span>Login Amministratori</span>
			<form action='login.cgi' method='post'>
				<p>Username:
					<input name='username' type='text' />
					Password:
					<input name='password' type='password' />
					<input value='Login' type='submit' />
				</p>
			</form>
			<form action='cgi-bin/logout.cgi' method='post'>
				<p><input value='Logout' type='submit' /></p>
			</form>
		</div>
	</div>
	</div>";	

print $page->end_html, "\n"; # fine pagina HTML