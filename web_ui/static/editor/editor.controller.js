(function() {
    'use strict';

    angular
        .module('recipes')
        .controller('EditorController', EditorController);

    EditorController.$inject = ['RicettaFactory', 'ModelliFactory', 'ApiRicetteFactory', '$log'];
        
    function EditorController(RicettaFactory, ModelliFactory, ApiRicetteFactory, $log) {
        var vm = this;
        vm.ricettaHandle = RicettaFactory;
        vm.ricetta = RicettaFactory.ricetta;
        vm.fotoPortate = ApiRicetteFactory.GetPortate();
        vm.portate = Object.keys(vm.fotoPortate);
        
        vm.periodi = ApiRicetteFactory.GetPeriodi();
        vm.nomiPeriodi = Object.keys(vm.periodi);
        vm.categorie = '';
        vm.mesi = vm.periodi['Tutti'];
        
        vm.SetMesi = SetMesi;
        
        vm.ingredienti = ApiRicetteFactory.GetListaIngredienti();

        vm.Togli = Togli;
        vm.Aggiungi = Aggiungi;
        vm.Muovi = Muovi;
        vm.EPrimo = EPrimo;
        vm.EUltimo = EUltimo;
        vm.Toggle = Toggle;

        
        Activate();
        
        
        function Activate () {
            $log.log('caricamento editor');
            vm.ricettaHandle.Carica = Carica;
            $log.log(vm.ricettaHandle);

            vm.categorie = vm.ricetta['categorie'].join();
            
            if (!(vm.ricetta.hasOwnProperty('portata')) || vm.ricetta.portata == '') {
                vm.ricetta.portata = vm.portate[0];
            }
        }
        
        
        function SetMesi(periodo) {
            $log.log(periodo);
            if ( !(periodo in vm.periodi) )
                periodo = 'Tutti';
            vm.ricetta['periodo'] = vm.periodi[periodo];
        }
        
        
        function Carica() {
            vm.ricetta['categorie'] = vm.categorie.split(/[,;.:]/).filter(value => value != '');
        }
        
        
        function Toggle(m) {
            if (! (Togli(vm.ricetta['periodo'], m)) ) {
                vm.ricetta['periodo'].push(m);
            }
        }
        
        
        function Aggiungi(contenitore, modello) {
            contenitore.push(ModelliFactory.Modello(modello));
        }
    }
    
    
    function Togli(contenitore, oggetto) {
        var index = contenitore.indexOf(oggetto);
        if (index > -1) {
            contenitore.splice(index, 1);
        }
        return index > -1;
    }
    
    function Muovi(contenitore, oggetto, direzione) {
        var index = contenitore.indexOf(oggetto);
        if (index > -1) {
            if (index == 0 && direzione == -1)
                return;
            if (index == contenitore.length-1 && direzione == 1)
                return;
            contenitore.splice(index, 1);
            contenitore.splice(index + direzione, 0, oggetto);
        }
    }
    
    
    function EPrimo(contenitore, oggetto) {
        return contenitore.indexOf(oggetto) == 0;
    }
    
    function EUltimo(contenitore, oggetto) {
        return contenitore.indexOf(oggetto) == contenitore.length-1;
    }
    

})();
