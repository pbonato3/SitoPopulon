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
'description' => 'Risultati operazioni',
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

print "<div id='content'>";
print "<h2> $esito </h2>";
print "<form action='/populon/cgi-bin/Notizie.cgi' method='post'>";
print "<p><input type='submit' value='Continua'/></p>";
print "</form>";

print "</div>";

	
print $page->end_html, "\n"; # fine pagina HTML
