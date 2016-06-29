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
'description' => 'Osserva le caratteristiche del personaggio selezionato',
'keywords' => 'Gioco, ruolo, gdr, fantasy, dadi',
'author' => 'Mattia Biggeri, Tommaso Padovan, Diego Baratto, Paolo Bonato',
'language' => 'italian it'},
-style =>{'src' => '../PopStyle.css'},			# Link al CSS
-author => 'paolo.bonato.12@gmail.com');				# Mail all'autore

#################		header		#################

print $page->div({-class => 'sbarra'}), "\n";

print $page->div({-id => 'header'}, h1("Populon"), img({-class => 'head', -src => "../img/titolo.png", -alt => "Populon"}), a({-class => 'saltamenu', -href => '#saltamenu'}, "Salta il menu di navigazione")), "\n";

#################		nav		#################

print $page->div({-class => 'nav'}, ul({-class => 'navbar'},
li({-class => 'button link', -onclick => 'location.href="../Home.html";'}, a({-href => '../Home.html', -class => 'link'},"Home")),
li({-class => 'button link', -onclick => 'location.href="../IlMondoDiGioco.html";'}, a({-href => '../IlMondoDiGioco.html', -class => 'link'},"Il mondo di gioco")),
li({-class => 'button link', -onclick => 'location.href="../cgi-bin/personaggi.cgi";'}, a({-href => '../cgi-bin/personaggi.cgi', -class => 'link'},"Personaggi")),
li({-class => 'button link', -onclick => 'location.href="../cgi-bin/Notizie.cgi";'}, a({-href => '../cgi-bin/Notizie.cgi', -class => 'link'},"Notizie")),
li({-class => 'button link', -onclick => 'location.href="../Chi.html";'}, a({-href => '../Chi.html', -class => 'link'},"Chi siamo")))), "\n"; 

print $page->div({-class => 'breadcrumbs'}, a({-name => 'saltamenu'}), strong("Ti trovi in: "), a({-href => 'personaggi.cgi'}, "Personaggi"), "&gt &gt Dettagli Personaggio"), "\n";


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