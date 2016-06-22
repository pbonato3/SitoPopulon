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

print $page->div({-id => 'header'}, h1("Populon"), img({-src => "/populon/img/titolo.png", -alt => "Populon"})), "\n";

#################		nav		#################

print $page->div({-id => 'nav'}, ul(
li(a({-href => '/populon/Home.html'},"Home")),
li(a({-href => '/populon/IlMondoDiGioco.html'},"Il mondo di gioco")),
li(a({-href => '/populon/IPersonaggi.html'},"I personaggi")),
li(a({-href => 'Notizie.cgi'},"Notizie")),
li(a({-href => '/populon/Chi.html'},"Chi Siamo")))), "\n"; 

#################		content		#################

print "<div id='content'>";
print "<h2> Aggiungi una notizia </h2>";
print<<END;
		<form action="InserimentoNotizia.cgi" method="post" enctype='multipart/form-data'>
			<div class='news'>
				<p><span class='newsTag'>Titolo:</span><span class='newsValue'>
					<input type="text" name="titolo" />
				</span></p>
				<p><span class='newsTag'>Data:</span><span class='newsValue'>
					<input type="date" name="data" />
				</span></p>
				<p><span class='newsTag'>Ora:</span><span class='newsValue'>
					<input type="time" name="ora" />
				</span></p>
				<p><span class='newsTag'>Luogo:</span><span class='newsValue'>
					<input type="text" name="luogo" />
				</span></p>
				<span class='newsTag'>Descrizione:</span><p class='newsValue'>
					<textarea name="descrizione" rows="7" cols="50"></textarea>
				</p>
				<input type="submit" value="Aggiungi" />
			</div>
		</form>
END
print "</div>";

	
print $page->end_html, "\n"; # fine pagina HTML
