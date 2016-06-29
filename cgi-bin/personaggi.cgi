#!"C:\xampp\perl\bin\perl.exe"
use CGI;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use HTTP::Request::Common qw(POST);
use HTTP::Request::Common qw(GET);
use XML::LibXML;

require funzioni;

my $page = CGI->new;					#creazione oggetto CGI
my $admin = getSession();

my $file = '../database/characters.xml';		#salvo il percorso del file xml

my $admin = getSession();

my $parser = XML::LibXML->new();		#creazione oggetto parser
my $doc = $parser->parse_file($file);	#apertura file e lettura input
my $root= $doc->getDocumentElement;		#estrazione elemento radice

my @characters = $root->findnodes("character");	#array dei nodi personaggio, inizzializzato con tutti i nodi. Successivamente va filtrato e usato per l'output

############## filtra per nome ##############
my $nome = $page->param('nome');								#prendo il parametro dall'url
if($nome){													#se il parametro è vuoto non lo considero
	@temp = ();												#inizializzo un array temporaneo nel quale mettere i personaggi corrispondenti
		foreach(@characters){								#scorro l'array delle notizie
			$value = lc $_->findnodes("name");				#salvo il valore del nodo (trasformato in lower case)
			$search = lc $nome;								#trasformo in lower case il parametro di ricerca
			if($value =~ /$search/){push @temp,$_;};		#se il nodo contiene la stringa cercata la inserisco nell'array temporaneo
		};
	@characters=@temp;										#l'array dei personaggi è stato filtrato
}
############## filtra per razza ##############
my $razza = $page->param('razza');							#prendo il parametro dall'url
if($razza){													#se il parametro è vuoto non lo considero
	@temp = ();												#inizializzo un array temporaneo nel quale mettere i personaggi corrispondenti
		foreach(@characters){								#scorro l'array delle notizie eventualmente filtrato
			$value = lc $_->findnodes("race"); 				#salvo il valore del nodo
			$search = lc $razza;							#trasformo in lower case il parametro di ricerca
			if($value =~ /$search/){push @temp,$_;};		#se il nodo contiene la stringa cercata la inserisco nell'array temporaneo
		};
	@characters=@temp;										#l'array dei personaggi è stato filtrato
}

print $page->header,
$page->start_html( # inizio pagina HTML
-title => 'Populon',									# Qui va il titolo
-dtd=>[ '-//W3C//DTD XHTML 1.0 Strict//EN',				# DTD
'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'
],
-lang =>'it',											# Lingua del documento
-meta => {'title' => 'Populon',							# Tutti i meta
'description' => 'Non sono le sole terre a costituire Populon, ci sono infiniti abitanti tutti diversi. Vieni a conoscere i frutti della fantasia dei nostri utenti e condividi i tuoi!',
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
li({-class => 'button current'}, span("I Personaggi")),
li({-class => 'button link', -onclick => 'location.href="../cgi-bin/Notizie.cgi";'}, a({-href => '../cgi-bin/Notizie.cgi', -class => 'link'},"Notizie")),
li({-class => 'button link', -onclick => 'location.href="../Chi.html";'}, a({-href => '../Chi.html', -class => 'link'},"Chi siamo")))), "\n"; 

print $page->div({-class => 'breadcrumbs'}, a({-name => 'saltamenu'}), strong("Ti trovi in: "), "Personaggi"), "\n";


#################		content		#################

print "<div class='content'>";
#genero l'array contenete i link per la paginazione delle notizie
my $totNotizie=0;
foreach(@characters) {$totNotizie+=1;}

my $notiziePerPagina=10;		#<------------ 	QUI SI IMPOSTA IL NUMERO MASSIMO DI NOTIZIE PER OGNI PAGINA


#salvo in $from e in $to i numeri delle notizie che devono essere visualizzate
my $from=$page->param('from');
my $to=$page->param('to');
if (!$from) {$from=1;}
if (!$to) {
	if ($totNotizie<$notiziePerPagina) {$to=$totNotizie}
	else {$to=$notiziePerPagina;}
}


my @arrLink=();					# l'array contenente i link per navigare tra le pagine

my $urlAttuale=CGI->new->url()."?nome=".$page->param('nome')."&amp;razza=".$page->param('razza');

if ($totNotizie<$notiziePerPagina) {$notiziePrimaPagina=$totNotizie}
else {$notiziePrimaPagina=$notiziePerPagina;}
push @arrLink,"<a href='".$urlAttuale."&amp;from=1&amp;to=$notiziePrimaPagina'>Prima pagina</a>";
my $c=1;
while ($c<=$totNotizie) {
	if ($c!=$from) {
		if ($c+$notiziePerPagina-1 <= $totNotizie) {
			my $str="<a href='".$urlAttuale."&amp;from=$c&amp;to=".($c+$notiziePerPagina-1)."'>".$c.'-'.($c+$notiziePerPagina-1)."</a>";
			push @arrLink,$str;
		}
		else {
			my $str="<a href='".$urlAttuale."&amp;from=$c&amp;to=$totNotizie'>".$c.'-'.$totNotizie."</a>";
			push @arrLink,$str;
		}
	} else {
		if ($c+$notiziePerPagina-1 <= $totNotizie) {
			my $str=$c.'-'.($c+$notiziePerPagina-1);
			push @arrLink,$str;
		}
		else {
			my $str=$c.'-'.$totNotizie;
			push @arrLink,$str;
		}
	}
	$c+=$notiziePerPagina;
}
$c-=$notiziePerPagina;
push @arrLink,"<a href='".$urlAttuale."&amp;from=$c&amp;to=$totNotizie'>Ultima pagina</a>";

# spengo il link alla pagina attuale nella barretta di navigazione
foreach(@arrLink) {

}

print "<h2> I Vostri Personaggi </h2>";
print "<h3>Filtro personaggi</h3>";
print "<form action='aggiungiPersonaggio.cgi' method='post'>";
print "<p><input type='submit' value='Compila la tua scheda'/></p>";
print "</form>";
print "<form action='personaggi.cgi' method='get'>";
print "<p>Nome: <input name='nome' type='text'/></p>";
print "<p>Razza: <select name='razza'>",
	"<option value=''>Tutti</option>",
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
print "<p><input type='submit' value='Filtra'/></p>";
print "</form>";

print " | ";
foreach(@arrLink) {
	print;
	print " | ";
}

## Output dei personaggi ##
my $i=1;
foreach(@characters){									#scorro l'array dei personaggi
	if ($from <= $i and $i <= $to ) {
		print "<div class='news'>";
		my $nome = $_->findnodes("name");					#salvo il valore del nodo nome
		print "<h3>",$nome,"</h3>";
		my $razza = $_->findnodes("race");					#salvo il valore del nodo razza
		print "<p><span class='charTag'>Razza:</span><span class='charValue'>",$razza,"</span></p>";
	
		my $id=$_->findnodes('@id');
		print "<a href='dettagliPersonaggio.cgi?id=$id'>Pi&ugrave; dettagli...</a>";
		if($admin) {
			print "<a href='process_deletePersonaggio.cgi?id=$id'>Cancella</a>";
		}
		print "</div>";
	}
	$i+=1;
}

print " | ";
foreach(@arrLink) {
	print;
	print " | ";
}

print "<a href='#header' class='goup'>Vai a inizio pagina</a>
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
