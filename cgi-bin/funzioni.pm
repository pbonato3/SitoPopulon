#!"C:\xampp\perl\bin\perl.exe"
use CGI::Session;
use CGI::Cookie;
use CGI;
use XML::LibXML;
use Encode qw(decode encode);

######### Creare la sessione ########
sub createSession{
	my $cgi = CGI->new;
	my $file = '../database/admin.xml';		#salvo il percorso del file xml
	my $parser = XML::LibXML->new();		#creazione oggetto parser
	my $doc = $parser->parse_file($file);	#apertura file e lettura input
	my $root = $doc->getDocumentElement;		#estrazione elemento radice
	
	my $admin = $root->findnodes("admin[username='$_[0]' and password='$_[1]']");
	if($admin){
		$session=CGI::Session->new();
		$session->param('admin',$_[0]);
		$sid=$session->id();
		my $cookie = $cgi->cookie(
			-name=>'MY-COOKIE',
			-value=>$sid,
			-expires=>'+1h',
			-path=>'/');
		print $cgi->header( -cookie=>$cookie );	#invio il cookie al client
		return $_[0];
	};
	return 0;
};

######### prendere la sessione ########
sub getSession{
	my $cgi = CGI->new;
	$cookie = $cgi->cookie('MY-COOKIE');			#provo a prendere il cookie
	$session=CGI::Session->load(undef,$cookie) or die $!;
	if ($session->is_expired || $session->is_empty ) {
		return undef;
	} else {
		my $utente = $session->param('admin');
		return $utente;
	};
};


######### Inserimento nuova notizia ########
sub nuovaNotizia{
	my $file = '../database/news.xml';		#salvo il percorso del file xml
	my $parser = XML::LibXML->new();		#creazione oggetto parser
	my $doc = $parser->parse_file($file);	#apertura file e lettura input
	my $root= $doc->getDocumentElement;		#estrazione elemento radice

	foreach (@_) {										#magia, non toccare, che va.
		$_=encode('UTF-8', $_, Encode::FB_CROAK);		#serve a codificare tutte le stringhe in input in UTF8 (accenti)
	}
	
	#creo una stringa con un nuovo elemento
	if(!$_[0]){$esito="Operazione fallita: Il titolo &egrave obbligatorio"; return $esito;}
	else{
		$nuovo="\n<notizia>";
		$nuovo.="\n<titolo>".$_[0]."</titolo>";
		if($_[1]){$nuovo.="\n<data>".$_[1]."</data>";};
		if($_[2]){$nuovo.="\n<ora>".$_[2]."</ora>";};
		if($_[3]){$nuovo.="\n<luogo>".$_[3]."</luogo>";};
		if($_[4]){$nuovo.="\n<descrizione>".$_[4]."</descrizione>";};
		$nuovo.="\n</notizia>";

		$frammento = $parser->parse_balanced_chunk($nuovo);	#controllo la buona formazione e creo un nodo
		$root->insertBefore($frammento,$root->firstChild);	#inserisco un nuovo in testa alla lista (prima del primo figlio)
		open OUT, ">$file";			#apro l'output sul file xml
		print OUT $doc->toString;	#stampo sul file il documento parsato
		
		$esito="Operazione completata";
		return $esito;
	};
	$esito = "operazione fallita";
	return $esito;
};


1	# NON toccare questo uno! deve stare in fondo alla pagina!