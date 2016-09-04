#!"C:\xampp\perl\bin\perl.exe"
use CGI;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use HTTP::Request::Common qw(POST);
use HTTP::Request::Common qw(GET);

require funzioni;

my $page = CGI->new;					#creazione oggetto CGI


my $admin = getSession();
if(!$admin){
	print $page->redirect("/populon/restricted.html");
}

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
  <a href=\"Notizie\"> Notizie </a>
  &gt; &gt; Inserimento Notizia
</div>
";

#################		content		#################

my $titolo = $page->param('titolo');
my $data= $page->param('data');
my $ora= $page->param('ora');
my $luogo= $page->param('luogo');
my $descrizione= $page->param('descrizione');
my $id= $page->param('id');

my $esito = undef;

if(!$titolo){$esito = "Operazione annullata: Manca un titolo"}
if($data && !($data =~ /^\d\d\d\d-\d\d-\d\d$/)){$esito = "Operazione annullata: La data non rispetta il corretto formato";}
if($ora && !($ora =~ /^\d\d:\d\d:\d\d$/)){$esito = "Operazione annullata: L'ora non rispetta il corretto formato"}

if(!$esito){
	# Se l'id è impostato la notizia che si vuole inserire è una modifica ad una precedente
	# In caso elimino la vecchia notizia (Controllo anche il titolo perchè se la notizia inserita non è valida la prima viene cancellata comunque)
	if($id and $titolo){eliminaNotizia($id);};
	# Aggiungo la nuova notizia
	$esito = nuovaNotizia($titolo,$data,$ora,$luogo,$descrizione,$id);
}

print "<div class='content'>";
print "<h2> $esito </h2>";
print "<form action='Notizie.cgi' method='post'>";
print "<p><input type='submit' value='Continua'/></p>";
print "</form>";

print "<a href='#header' class='goup'>Vai a inizio pagina</a></div>";

print "<div id='footer'>Contatti: populon&#64;gmail.com
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
			<form action='logout.cgi' method='post'>
				<p><input value='Logout' type='submit' /></p>
			</form>
		</div>
	</div>
	</div>";
	
print $page->end_html, "\n"; # fine pagina HTML
