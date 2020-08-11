(function() {
    'use strict';
    
    angular
        .module('recipes')
        .controller('EditRecipeController', EditRecipeController);

    EditRecipeController.$inject = ['ricettaPrepService', 'RicettaFactory', 'ApiRicetteFactory', '$timeout', '$log'];

    function EditRecipeController(ricettaPrepService, RicettaFactory, ApiRicetteFactory, $timeout, $log) {
        var vm = this;
        vm.MandaRichiesta = MandaRichiesta;
        vm.posto = {status: 0};
        
        activate();
        
        
        function activate() {
            RicettaFactory.ricetta = ricettaPrepService.data;
            RicettaFactory.Normalizza(RicettaFactory.ricetta, 1/RicettaFactory.dosi);
            for (var p in RicettaFactory.ricetta.parti) {
                var parte = RicettaFactory.ricetta.parti[p];
                if (! (parte.hasOwnProperty('varianti'))) {
                    parte['varianti'] = [];
                }
            }
        }
        
        
        function MandaRichiesta() {
            RicettaFactory.Carica();
            
            RicettaFactory.Normalizza(RicettaFactory.ricetta, RicettaFactory.dosi);
            $log.log(RicettaFactory);
            ApiRicetteFactory.UpdateRicetta(RicettaFactory.ricetta.id, RicettaFactory.ricetta)
                .then(Ricevi);
        }
        
        function Ricevi(response) {
            RicettaFactory.Normalizza(RicettaFactory.ricetta, 1/RicettaFactory.dosi);
            vm.posto = {
                status: response.status,
                codice: response.data.codice,
                messaggio: response.data.messaggio,
            }
            $timeout(function () { vm.posto.status = 0; }, 10000);
        }

    }
})();
