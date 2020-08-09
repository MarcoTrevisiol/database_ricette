(function() {
    'use strict';

    angular
        .module('recipes')
        .controller('EditorController', EditorController);

    EditorController.$inject = ['RicettaFactory', 'ModelliFactory', 'ApiRicetteFactory', '$log'];
        
    function EditorController(RicettaFactory, ModelliFactory, ApiRicetteFactory, $log) {
        var vm = this;
        vm.ricetta = RicettaFactory;
        vm.fotoPortate = ApiRicetteFactory.GetPortate();
        vm.portate = Object.keys(vm.fotoPortate);
        vm.ricetta.portata = vm.portate[0];
        
        vm.periodi = ApiRicetteFactory.GetPeriodi();
        vm.nomiPeriodi = Object.keys(vm.periodi);
        vm.categorie = '';
        vm.mesi = vm.periodi['Tutti'];
        
        vm.mesiSelezionati = {}
        vm.SetMesi = SetMesi;

        vm.ricetta.parti = [ModelliFactory.Modello('partePrincipale')];
        vm.Togli = Togli;
        vm.Aggiungi = Aggiungi;
        vm.Muovi = Muovi;
        vm.EPrimo = EPrimo;
        vm.EUltimo = EUltimo;

        
        Activate();
        
        
        function Activate () {
                for (var m in vm.mesi) {
                vm.mesiSelezionati[vm.mesi[m]] = true;
            }
            $log.log(vm.mesiSelezionati);
            
            vm.ricetta.Carica = Carica;
        };
        
        
        function SetMesi(periodo) {
            $log.log(periodo);
            if ( !(periodo in vm.periodi) )
                periodo = 'Tutti';
            for (m in vm.mesi) {
                var daAggiungere = vm.periodi[periodo].includes(vm.mesi[m]);
                $log.log(vm.mesi[m], daAggiungere);
                vm.mesiSelezionati[vm.mesi[m]] = daAggiungere;
            }
        };
        
        
        function Togli(contenitore, oggetto) {
            var index = contenitore.indexOf(oggetto);
            if (index > -1) {
                contenitore.splice(index, 1);
            }
        };
        
        function Aggiungi(contenitore, modello) {
            contenitore.push(ModelliFactory.Modello(modello));
        };
        
        function Muovi(contenitore, oggetto, direzione) {
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
        
        
        function EPrimo(contenitore, oggetto) {
            return contenitore.indexOf(oggetto) == 0;
        };
        
        function EUltimo(contenitore, oggetto) {
            return contenitore.indexOf(oggetto) == contenitore.length-1;
        };
        
        
        function Carica() {
                vm.ricetta['periodo'] = [];
                for (m in vm.mesi) {
                    if (vm.mesiSelezionati[vm.mesi[m]])
                        vm.ricetta['periodo'].push(vm.mesi[m]);
                }
                vm.ricetta['categorie'] = vm.categorie.split(/[,;.:]/).filter(value => value != '');
        };
    };
})();
