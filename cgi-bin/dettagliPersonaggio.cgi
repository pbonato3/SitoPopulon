#!"C:\xampp\perl\bin\perl.exe"
use CGI;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use HTTP::Request::Common qw(POST);
use HTTP::Request::Common qw(GET);

require funzioni;

my $page = CGI->new;					#creazione oggetto CGI

my $admin = getSession();

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
<meta name="author" content="Mattia Biggeri, Tommaso Padovan, Diego Baratto, Paolo Bonato" />
<meta name="title" content="Populon" />
<meta name="description" content="I personaggi nel dettaglio" />
<link rel="stylesheet" type="text/css" href="../PopStyle.css" />
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<meta http-equiv="Content-Script-Type" content="text/javascript"/>
</head>
<body>
';

#################		header		#################

print "<div class=\"sbarra\" >\n";

print $page->div({-id => 'header'}, h1("Populon"), img({-class => 'head', -src => "../img/titolo.png", -alt => "Populon"}), a({-class => 'saltamenu', -href => '#saltamenu'}, "Salta il menu di navigazione")), "\n";

#################		nav		#################

print $page->div({-class => 'nav'}, ul({-class => 'navbar'},
li({-class => 'button link', -onclick => 'location.href="../Home.html";'}, a({-href => '../Home.html', -class => 'link'},"Home")),
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
  <a href=\"personaggi.cgi\"> Personaggi </a>
  &gt; &gt; Dettagli Personaggio
</div>
";

#################		content		#################

my $ID=$page->param('id');
my $personaggio=trovaPersonaggio($ID);

my $nome=$personaggio->findnodes('name');
my $razza=$personaggio->findnodes('race');
my $sesso=$personaggio->findnodes('sex');
my $eta=$personaggio->findnodes('age');
my $puntiCorpo=$personaggio->findnodes('body/@value');
my @abilitaCorpo=$personaggio->findnodes('body/ability');
my $puntiMente=$personaggio->findnodes('mind/@value');
my @abilitaMente=$personaggio->findnodes('mind/ability');
my $puntiHeart=$personaggio->findnodes('heart/@value');
my @abilitaHeart=$personaggio->findnodes('heart/ability');
my $biografia=$personaggio->findnodes('bio');

print<<END;
<div class='content'>
END

print"
	<div class='scheda'>
		<h3>$nome</h3>";
		print "<p><span class='schedaTag'>Razza: </span><span class='schedaValue'>$razza</span></p>";
		print "<p><span class='schedaTag'>Sesso: </span><span class='schedaValue'>$sesso</span></p>";
		print "<p><span class='schedaTag'>Et&agrave;: </span><span class='schedaValue'>$eta</span></p>";
		print "<p><span class='schedaTag'>Punti Corpo: </span><span class='schedaValue'>$puntiCorpo</span></p>";
		foreach(@abilitaCorpo){
			my $nomeAbilita = $_->findnodes('@name');
			my $livelloAbilita = $_->findnodes('@level');
			print "<p><span class='abilita'><span class='schedaTag'>$nomeAbilita</span>   Livello $livelloAbilita</span></p>";
		}
		print "<p><span class='schedaTag'>Punti Mente: </span><span class='schedaValue'>$puntiMente</span></p>";
		foreach(@abilitaMente){
			my $nomeAbilita = $_->findnodes('@name');
			my $livelloAbilita = $_->findnodes('@level');
			print "<p><span class='abilita'><span class='schedaTag'>$nomeAbilita</span>   Livello $livelloAbilita</span></p>";
		}
		print "<p><span class='schedaTag'>Punti Spirito: </span><span class='schedaValue'>$puntiHeart</span></p>";
		foreach(@abilitaHeart){
			my $nomeAbilita = $_->findnodes('@name');
			my $livelloAbilita = $_->findnodes('@level');
			print "<p><span class='abilita'><span class='schedaTag'>$nomeAbilita</span>   Livello $livelloAbilita</span></p>";
		}
		
print "</div><div class='bio'><h4>Biografia:</h4><p>".$biografia."</p></div>";
print "<form action='personaggi.cgi' method='post'><p><input type='submit' value='Indietro' /></p></form><a href='#header' class='goup'>Vai a inizio pagina</a>
</div>";

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
			<form action='logout.cgi' method='post'>
				<p><input value='Logout' type='submit' /></p>
			</form>
		</div>
	</div>
	</div>";

print $page->end_html, "\n"; # fine pagina HTML