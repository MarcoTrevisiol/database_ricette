(function() {
    'use strict';
    
    angular
        .module('recipes')
        .controller('EditRecipeController', EditRecipeController);

    EditRecipeController.$inject = ['ricettaPrepService', 'RicettaFactory', 'NormalizzaDosiFactory', 'ApiRicetteFactory', '$timeout', '$log'];

    function EditRecipeController(ricettaPrepService, RicettaFactory, NormalizzaDosiFactory, ApiRicetteFactory, $timeout, $log) {
        var vm = this;
        vm.MandaRichiesta = MandaRichiesta;
        vm.posto = {status: 0};
        
        activate();
        
        function activate() {
            RicettaFactory.ricetta = ricettaPrepService.data;
            NormalizzaDosiFactory.Normalizza(RicettaFactory.ricetta, 1/RicettaFactory.dosi);
        };
        
        
        function MandaRichiesta() {
            RicettaFactory.Carica();
            
            NormalizzaDosiFactory.Normalizza(RicettaFactory.ricetta, RicettaFactory.dosi);
            $log.log(RicettaFactory);
            ApiRicetteFactory.UpdateRicetta(RicettaFactory.ricetta.id, RicettaFactory.ricetta)
                .then(function (response) {
                    NormalizzaDosiFactory.Normalizza(RicettaFactory.ricetta, 1/RicettaFactory.dosi);
                    vm.posto = {
                        status: response.status,
                        codice: response.data.codice,
                        messaggio: response.data.messaggio,
                    }
                    $timeout(function () { vm.posto.status = 0; }, 10000);
                });
        };

    };
})();
