function Controller() {
    this.titolo = "Titolo della ricetta";
    this.fotoPortate = {
        'Primo': 'images/Primo.jpg',
        'Secondo': 'images/Secondo.jpg',
        'Contorno': 'images/Contorno.jpg',
        'Dolce': 'images/Dolce.jpg',
    };
    this.portate = Object.keys(this.fotoPortate);
    this.portata = this.portate[0];
    console.log(this.portata);
    
    this.tempo = 30;
    this.mesi = ['gen', 'feb', 'mar', 'apr', 'mag', 'giu', 'lug', 'ago', 'set', 'ott', 'nov', 'dic'];
    
    this.mesiSelezionati = {}
    for (m in this.mesi) {
        this.mesiSelezionati[this.mesi[m]] = true;
    }
    console.log(this.mesiSelezionati);
    
    this.periodi = {
        'Primavera': ['mar', 'apr', 'mag'],
        'Estate': ['giu', 'lug', 'ago'],
        'Autunno': ['set', 'ott', 'nov'],
        'Inverno': ['dic', 'gen', 'feb'],
        'Tutti': this.mesi,
        'Niente': [],
    };
    this.nomiPeriodi = Object.keys(this.periodi);
    
    this.SetMesi = function SetMesi(periodo) {
        console.log(periodo);
        if (! (periodo in this.periodi))
            periodo = 'Tutti';
        for (m in this.mesi) {
            var daAggiungere = this.periodi[periodo].includes(this.mesi[m]);
            console.log(this.mesi[m], daAggiungere);
            this.mesiSelezionati[this.mesi[m]] = daAggiungere;
        }
    };
    
    this.parti = [
        {
            'nome': 'parte principale',
            'ingredienti': [
                {
                    'nome': '',
                    'principale': false,
                },
                {
                    'nome': '',
                    'principale': true,
                },
            ],
            'procedura': '',
        },
    ];
    this.TogliIngrediente = function TogliIngrediente(parte, ingrediente) {
        console.log(parte, ingrediente);
        var index = parte['ingredienti'].indexOf(ingrediente);
        if (index > -1) {
            parte['ingredienti'].splice(index, 1);
        }
    };
    this.AggiungiIngrediente = function AggiungiIngrediente(parte) {
        console.log(parte);
        parte['ingredienti'].push({
            'nome': '',
            'principale': false,
        });
    };
    this.TogliVariante = function TogliVariante(parte, variante) {
        var index = parte['varianti'].indexOf(variante);
        if (index > -1) {
            parte['varianti'].splice(index, 1);
        }
    };
    this.AggiungiVariante = function AggiungiVariante(parte) {
        parte['varianti'] = parte['varianti'] || [];
        parte['varianti'].push({
            'ingredienti': [],
            'procedura': '',
        });
    };
    this.TogliParte = function TogliParte(parte) {
        var index = this.parti.indexOf(parte);
        if (index > -1) {
            this.parti.splice(index, 1);
        }
    };
    this.AggiungiParte = function AggiungiParte() {
        this.parti.push({
            'nome': 'parte secondaria',
            'ingredienti': [
                {
                    'nome': '',
                    'principale': false,
                }
            ],
            'procedura': '',
        });
    };
}

angular
    .module('recipes', [])
    .controller('Controller', Controller);
