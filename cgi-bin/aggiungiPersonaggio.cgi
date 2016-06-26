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
'description' => 'Compila sul sito la tua scheda e falla conoscere a tutti!',
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
li(a({-href => '/populon/cgi-bin/personaggi.cgi'},"I personaggi")),
li(a({-href => '/populon/cgi-bin/Notizie.cgi'},"Notizie")),
li(a({-href => '/populon/Chi.html'},"Chi Siamo")))), "\n"; 

#################		content		#################
#massimo numero di abilità
my $max = 10;

print "<div id='content'>";
print "<h2> Compila la tua scheda </h2>";

print "<div class='scheda'>";
# form per l'input dei dati di un personaggio
	print "<form action='inserimentoPersonaggio.cgi' method='post' enctype='multipart/form-data'>";
	# Insermento nome
	print "<p>Nome: <input name='nome' type='text'/></p>";
	# Inserimento razza
	print "<p>Razza: <select name='razza'>",
		"<option value='Akquor'>Akquor</option>",
		"<option value='Elfo'>Elfo</option>",
		"<option value='Mustelan'>Mustelan</option>",
		"<option value='Nano'>Nano</option>",
		"<option value='Spyrian'>Spyrian</option>",
		"<option value='Tesserian'>Tesserian</option>",
		"<option value='Troll'>Troll</option>",
		"<option value='Umano'>Umano</option>",
		"<option value='Ur-Aluk'>Ur-Aluk</option>",
		"</select></p>";
	# Inserimento sesso
	print "<p>Sesso: <input type='radio' name='sesso' value='M' checked='checked' /> M",
		"<input type='radio' name='gender' value='F' /> F </p>";
	# Inserimento età
	print "<p>Et&agrave;: <input name='eta' type='text' /></p>";
	# Inserimento punti corpo
	print "<p>Punti corpo: <input name='corpo' type='text' /></p>";
		print "<div class='elencoFormAbilita'>";
		for(my $i=0; $i < $max; $i++){
			print "<p>Abilit&agrave;: <input name='name_c$i' type='text' />";
			print "Livello: <select name='value_c$i'>";
			for(my $j=1; $j<=5; $j++){
				print"<option value=\"$j\">$j</option>";
			}
			print "</select></p>";
		}
		print "</div>";
	# Inserimento punti mente
	print "<p>Punti mente: <input name='mente' type='text' /></p>";
		print "<div class='elencoFormAbilita'>";
		for(my $i=0; $i < $max; $i++){
			print "<p>Abilit&agrave;: <input name='name_m$i' type='text' />";
			print "Livello: <select name='value_m$i'>";
			for(my $j=1; $j<=5; $j++){
				print"<option value=\"$j\">$j</option>";
			}
			print "</select></p>";
		}
		print "</div>";
	# Inserimento punti spirito
	print "<p>Punti spirito: <input name='spirito' type='text'/></p>";
		print "<div class='elencoFormAbilita'>";
		for(my $i=0; $i < $max; $i++){
			print "<p>Abilit&agrave;: <input name='name_s$i' type='text' />";
			print "Livello: <select name='value_s$i'>";
			for(my $j=1; $j<=5; $j++){
				print"<option value=\"$j\">$j</option>";
			}
			print "</select></p>";
		}
		print "</div>";
	# Inserimento biografia
	print "<p>Biografia: </p><p><textarea name='bio' rows='10' cols='50'></textarea></p>";
	print "<p><input type='submit' value='Conferma'/></p>";
	print "</form>";
print "</div></div>";

	
print $page->end_html, "\n"; # fine pagina HTML
