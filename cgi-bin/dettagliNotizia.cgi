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

print $page->div({-id => 'header'}, h1("Populon"), img({-src => "/populon/img/titolo.png", -alt => "Populon"})), "\n";

#################		nav		#################

print $page->div({-id => 'nav'}, ul(
li(a({-href => '/populon/Home.html'},"Home")),
li(a({-href => '/populon/IlMondoDiGioco.html'},"Il mondo di gioco")),
li(a({-href => '/populon/IPersonaggi.html'},"I personaggi")),
li(a({-href => 'Notizie.cgi'},"Notizie")),
li(a({-href => '/populon/Chi.html'},"Chi Siamo")))), "\n"; 


#################		content		#################

$ID=$page->param('id');
$notizia=trovaNotizia($ID);

$titolo=$notizia->findnodes('titolo');
$data=$notizia->findnodes('data');
$ora=$notizia->findnodes('ora');
$luogo=$notizia->findnodes('luogo');
$descrizione=$notizia->findnodes('descrizione');
$titolo=$titolo->string_value();
$data=$data->string_value();
$ora=$ora->string_value();
$luogo=$luogo->string_value();
$descrizione=$descrizione->string_value();


print<<END;
<div id='content'>
<h2> Notizie </h2>
END


if(!$admin){
print"
	<div class='news'>
		<h3>$titolo</h3>";
		if($data){ print "<p><span class='newsTag'>Data:</span><span class='newsValue'>$data</span></p>";}
		if($ora){ print "<p><span class='newsTag'>Ora:</span><span class='newsValue'>$ora</span></p>";}
		if($luogo){ print "<p><span class='newsTag'>Luogo:</span><span class='newsValue'>$luogo</span></p>";}
		if($descrizione){ print "<span class='newsTag'>Descrizione:</span><p class='newsValue'>$descrizione</p>";}
print	"</div>
	</div>";

} else {
print<<END;
		<form action="InserimentoNotizia.cgi" method="post">
			<div class='news'>
				<p><span class='newsTag'>Titolo:</span><span class='newsValue'>
					<input type="text" name="titolo" value="$titolo" />
				</span></p>
				<p><span class='newsTag'>Data:</span><span class='newsValue'>
					<input type="text" name="data" value="$data" /> (YYYY-MM-DD)
				</span></p>
				<p><span class='newsTag'>Ora:</span><span class='newsValue'>
					<input type="text" name="ora" value="$ora" /> (HH:MM:SS)
				</span></p>
				<p><span class='newsTag'>Luogo:</span><span class='newsValue'>
					<input type="text" name="luogo" value="$luogo" />
				</span></p>
				<span class='newsTag'>Descrizione:</span><p class='newsValue'>
					<textarea name="descrizione" rows="7" cols="50">$descrizione</textarea>
				</p>
				<input type="hidden" name="id" value="$ID" />
				<input type="submit" value="Applica i Cambiamenti" />
			</div>
		</form>
	</div>
END
};














print $page->end_html, "\n"; # fine pagina HTML