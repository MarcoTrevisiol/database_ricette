angular
    .module('recipes')
    .controller('Controller', ['ModelliFactory', 'ApiRicetteFactory', 'NormalizzaDosiFactory', '$timeout', '$log', Controller]);


function Controller(ModelliFactory, ApiRicetteFactory, NormalizzaDosiFactory, $timeout, $log) {
    var vm = this;
    vm.ricetta = {};
    vm.ricetta.titolo = "Titolo della ricetta";
    vm.dosi = 4;
    vm.fotoPortate = ApiRicetteFactory.GetPortate();
    vm.portate = Object.keys(vm.fotoPortate);
    vm.ricetta.portata = vm.portate[0];
    
    vm.ricetta.tempo = 'PT30M';
    
    vm.periodi = ApiRicetteFactory.GetPeriodi();
    vm.nomiPeriodi = Object.keys(vm.periodi);
    vm.categorie = '';
    vm.mesi = vm.periodi['Tutti'];
    
    vm.mesiSelezionati = {}
    for (m in vm.mesi) {
        vm.mesiSelezionati[vm.mesi[m]] = true;
    }
    $log.log(vm.mesiSelezionati);
    
    vm.SetMesi = function (periodo) {
        $log.log(periodo);
        if ( !(periodo in vm.periodi) )
            periodo = 'Tutti';
        for (m in vm.mesi) {
            var daAggiungere = vm.periodi[periodo].includes(vm.mesi[m]);
            $log.log(vm.mesi[m], daAggiungere);
            vm.mesiSelezionati[vm.mesi[m]] = daAggiungere;
        }
    };
    
    vm.ricetta.parti = [ModelliFactory.Modello('partePrincipale')];
    
    vm.Togli = function (contenitore, oggetto) {
        var index = contenitore.indexOf(oggetto);
        if (index > -1) {
            contenitore.splice(index, 1);
        }
    };
    vm.Aggiungi = function (contenitore, modello) {
        contenitore.push(ModelliFactory.Modello(modello));
    };
    
    vm.Muovi = function (contenitore, oggetto, direzione) {
        var index = contenitore.indexOf(oggetto);
        if (index > -1) {
            $log.log(contenitore, oggetto, direzione, index);
            if (index == 0 && direzione == -1)
                return;
            if (index == contenitore.length-1 && direzione == 1)
                return;
            contenitore.splice(index, 1);
            contenitore.splice(index + direzione, 0, oggetto);
        }
    };
    
    vm.EPrimo = function (contenitore, oggetto) {
        return contenitore.indexOf(oggetto) == 0;
    };
    vm.EUltimo = function (contenitore, oggetto) {
        return contenitore.indexOf(oggetto) == contenitore.length-1;
    };
    
    vm.MandaRichiesta = function () {
        vm.ricetta['periodo'] = [];
        for (m in vm.mesi) {
            if (vm.mesiSelezionati[vm.mesi[m]])
                vm.ricetta['periodo'].push(vm.mesi[m]);
        }
        vm.ricetta['categorie'] = vm.categorie.split(/[,;.:]/).filter(value => value != '');
        
        NormalizzaDosiFactory.Normalizza(vm.ricetta, vm.dosi);
        $log.log(vm.ricetta);
        ApiRicetteFactory.PostRicetta(vm.ricetta)
            .then(function (response) {
                NormalizzaDosiFactory.Normalizza(vm.ricetta, 1/vm.dosi);
                vm.posto = {
                    status: response.status,
                    codice: response.data.codice,
                    messaggio: response.data.messaggio,
                }
                $timeout(function () { vm.posto.status = 0; }, 10000);
            });
    };
};
