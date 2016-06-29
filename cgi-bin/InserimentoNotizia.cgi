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
'description' => 'Stiamo inserendo la nuova notizia',
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

print $page->div({-class => 'breadcrumbs'}, a({-name => 'saltamenu'}), strong("Ti trovi in: "), a({-href => 'Notizie.cgi'}, "Notizie"), "&gt &gt Inserimento Notizia"), "\n";

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
