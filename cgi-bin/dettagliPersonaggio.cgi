#!"C:\xampp\perl\bin\perl.exe"
use CGI;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use HTTP::Request::Common qw(POST);
use HTTP::Request::Common qw(GET);

require funzioni;

my $page = CGI->new;					#creazione oggetto CGI

my $admin = getSession();

print $page->header,
$page->start_html( # inizio pagina HTML
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
li(a({-href => '/populon/Home.html'},"Home")),
li(a({-href => '/populon/IlMondoDiGioco.html'},"Il mondo di gioco")),
li(span("I Personaggi")),
li(a({-href => '/populon/cgi-bin/Notizie.cgi'},"Notizie")),
li(a({-href => '/populon/Chi.html'},"Chi Siamo")))), "\n"; 


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
<div id='content'>
END

print"
	<div class='scheda'>
		<h3>$nome</h3>";
		print "<p><span class='schedaTag'>Razza: </span><span class='schedaValue'>$razza</span></p>";
		print "<p><span class='schedaTag'>Sesso: </span><span class='schedaValue'>$sesso</span></p>";
		print "<p><span class='schedaTag'>Et&agrave: </span><span class='schedaValue'>$eta</span></p>";
		print "<p><span class='schedaTag'>Punti Corpo: </span><span class='schedaValue'>$puntiCorpo</span></p>";
		foreach(@abilitaCorpo){
			my $nomeAbilita = $_->findnodes('@name');
			my $livelloAbilita = $_->findnodes('@level');
			print "<p><span class='abilita'>$nomeAbilita   Livello: $livelloAbilita</span></p>";
		}
		print "<p><span class='schedaTag'>Punti Mente: </span><span class='schedaValue'>$puntiMente</span></p>";
		foreach(@abilitaMente){
			my $nomeAbilita = $_->findnodes('@name');
			my $livelloAbilita = $_->findnodes('@level');
			print "<p><span class='abilita'>$nomeAbilita   Livello: $livelloAbilita</span></p>";
		}
		print "<p><span class='schedaTag'>Punti Spirito: </span><span class='schedaValue'>$puntiHeart</span></p>";
		foreach(@abilitaHeart){
			my $nomeAbilita = $_->findnodes('@name');
			my $livelloAbilita = $_->findnodes('@level');
			print "<p><span class='abilita'>$nomeAbilita   Livello: $livelloAbilita</span></p>";
		}
		
print "</div><div class='bio'><h4>Biografia:</h4><p>".$biografia."</p></div>";
print "<form action='personaggi.cgi' method='POST'><input type='submit' value='Indietro' /></form></div>";


print $page->end_html, "\n"; # fine pagina HTML