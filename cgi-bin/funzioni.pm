use XML::LibXML;


######### Inserimento nuova notizia ########
sub nuovaNotizia{
	my $file = '../database/news.xml';		#salvo il percorso del file xml
	my $parser = XML::LibXML->new();		#creazione oggetto parser
	my $doc = $parser->parse_file($file);	#apertura file e lettura input
	my $root= $doc->getDocumentElement;		#estrazione elemento radice

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